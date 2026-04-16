import redis
import requests
import time
import json
import random
import numpy as np

cache = redis.Redis(host='cache-redis', port=6379, db=0, decode_responses=True)
RESPONSE_GEN_URL = "http://response-gen:5000/query"

ZONAS = ["Z1", "Z2", "Z3", "Z4", "Z5"]
TIPOS = ["Q1", "Q2", "Q3", "Q5"]

# Configuración Zipf
a = 1.5
pesos = [1 / (i**a) for i in range(1, len(ZONAS) + 1)]
probs_zipf = [p / sum(pesos) for p in pesos]

def simulate_traffic(dist):
    zone = np.random.choice(ZONAS, p=probs_zipf) if dist == "zipf" else random.choice(ZONAS)
    q_type = random.choice(TIPOS)
    conf = random.choice([0.0, 0.5, 0.8])
    cache_key = f"{q_type}:{zone}:c={conf}"
    
    start = time.time()
    cached = cache.get(cache_key)
    
    if cached:
        latency = (time.time() - start) * 1000
        print(f"[{dist.upper()}] ✅ HIT {latency:.2f}ms")
        with open('metricas_experimento.csv', 'a') as f:
            f.write(f"{time.time()},{dist},{q_type},HIT,{latency:.2f}\n")
    else:
        print(f"[{dist.upper()}] ❌ MISS. Consultando...")
        try:
            resp = requests.post(RESPONSE_GEN_URL, json={"type": q_type, "zone_id": zone, "confidence_min": conf})
            cache.set(cache_key, json.dumps(resp.json()), ex=30)
            latency = (time.time() - start) * 1000
            print(f"   -> MISS resuelto en {latency:.2f}ms")
            with open('metricas_experimento.csv', 'a') as f:
                f.write(f"{time.time()},{dist},{q_type},MISS,{latency:.2f}\n")
        except:
            raise requests.exceptions.ConnectionError

if __name__ == "__main__":
    # CAMBIA AQUÍ PARA TUS PRUEBAS
    DIST = "zipf" 
    print(f"Iniciando tráfico: {DIST}")
    while True:
        try:
            simulate_traffic(DIST)
            time.sleep(1)
        except:
            print("⏳ Servidor cargando CSV...")
            time.sleep(3)