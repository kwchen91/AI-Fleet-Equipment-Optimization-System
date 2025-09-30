# src/route_vrp.py

from typing import Dict, List, Tuple
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from .kpi import KPIWeights, normalize_weights

def _mock_nodes(n_customers=8, seed=42):
    rng = np.random.default_rng(seed)

    coords = [(0.0, 0.0)]
    coords += [(float(rng.uniform(-10, 10)), float(rng.uniform(-10, 10))) for _ in range(n_customers)]
    return coords  # index 0 = depot

def _euclid(a, b):
    return float(np.hypot(a[0]-b[0], a[1]-b[1]))

def _distance_matrix(coords):
    n = len(coords)
    mat = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                mat[i][j] = _euclid(coords[i], coords[j])
    return mat

def _congestion_matrix(n: int, base: float = 0.1, seed=42):
    rng = np.random.default_rng(seed)

    mat = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                mat[i][j] = float(np.clip(base + rng.uniform(0, 0.5), 0, 1.0))
    return mat

def optimize_route(
    use_mock: bool = True,
    coords: List[Tuple[float, float]] = None,
    vehicle_count: int = 1,
    emission_factor_kg_per_km: float = 0.25, 
    avg_speed_kmph: float = 40.0,
    weights: KPIWeights = KPIWeights(1,1,1,1)
):

    w = normalize_weights(weights)

    if use_mock or coords is None:
        coords = _mock_nodes(n_customers=8)

    n = len(coords)
    dist = _distance_matrix(coords)               # km
    cong = _congestion_matrix(n)                  # 0~1
    time_h = [[(dist[i][j] / avg_speed_kmph) for j in range(n)] for i in range(n)]  # hr
    co2   = [[dist[i][j] * emission_factor_kg_per_km for j in range(n)] for i in range(n)]


    manager = pywrapcp.RoutingIndexManager(n, vehicle_count, 0)  # depot=0
    routing = pywrapcp.RoutingModel(manager)

    def cost_cb(from_index, to_index):
        i, j = manager.IndexToNode(from_index), manager.IndexToNode(to_index)
        cost = (
            w.distance * dist[i][j] +
            w.time     * time_h[i][j] * 10.0 +  
            w.co2      * co2[i][j]    * 0.1 +  
            w.congestion * cong[i][j] * 10.0
        )
        return int(round(cost * 1000))

    transit_cb_index = routing.RegisterTransitCallback(cost_cb)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_cb_index)


    routing.AddDimension(transit_cb_index, 0, 10**9, True, "CostDim")

    search = pywrapcp.DefaultRoutingSearchParameters()
    search.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search.time_limit.FromSeconds(3)
    solution = routing.SolveWithParameters(search)

    if solution is None:
        return ["No feasible route"], {"distance_km":0,"time_hr":0,"co2_kg":0,"congestion":0}

    index = routing.Start(0)
    order = [0]
    total_dist, total_time, total_co2, total_cong = 0.0, 0.0, 0.0, 0.0
    while not routing.IsEnd(index):
        next_index = solution.Value(routing.NextVar(index))
        i, j = manager.IndexToNode(index), manager.IndexToNode(next_index)
        total_dist += dist[i][j]
        total_time += time_h[i][j]
        total_co2  += co2[i][j]
        total_cong += cong[i][j]
        order.append(j)
        index = next_index

    return (
        [f"N{node}" for node in order],  
        {
            "distance_km": round(total_dist, 2),
            "time_hr": round(total_time, 2),
            "co2_kg": round(total_co2, 2),
            "congestion_index": round(total_cong, 2)
        }
    )


