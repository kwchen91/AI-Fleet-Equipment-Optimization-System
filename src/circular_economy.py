# src/circular_economy.py
import random

def circular_recommendation(n=5):
    recs = []
    for i in range(n):
        health_score = random.randint(40, 100)
        if health_score > 80:
            action = "✅ Continue using"
        elif health_score > 60:
            action = "🔧 Refurbish/Maintain"
        else:
            action = "♻️ Recycle/Decommission"
        recs.append({"equipment_id": f"EQT{i+1}", "health_score": health_score, "recommendation": action})
    return recs

if __name__ == "__main__":
    print(circular_recommendation())
