# src/kpi.py
from dataclasses import dataclass

@dataclass
class KPIWeights:
    distance: float = 1.0
    time: float = 1.0
    co2: float = 1.0
    congestion: float = 1.0

def normalize_weights(w: "KPIWeights") -> "KPIWeights":
    s = w.distance + w.time + w.co2 + w.congestion
    if s == 0:
        return KPIWeights(1,1,1,1)
    return KPIWeights(
        distance=w.distance/s,
        time=w.time/s,
        co2=w.co2/s,
        congestion=w.congestion/s
    )
