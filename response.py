from flask import Flask, request, jsonify
import statistics
import numpy as np
import csv

app = Flask(__name__)

# Bounding Boxes oficiales
BOUNDING_BOXES = {
    "Z1": {"lat_min": -33.445, "lat_max": -33.420, "lon_min": -70.640, "lon_max": -70.600},
    "Z2": {"lat_min": -33.420, "lat_max": -33.390, "lon_min": -70.600, "lon_max": -70.550},
    "Z3": {"lat_min": -33.530, "lat_max": -33.490, "lon_min": -70.790, "lon_max": -70.740},
    "Z4": {"lat_min": -33.470, "lat_max": -33.430, "lon_min": -70.670, "lon_max": -70.630},
    "Z5": {"lat_min": -33.470, "lat_max": -33.430, "lon_min": -70.810, "lon_max": -70.760}
}
zone_area_km2 = {"Z1": 14.4, "Z2": 99.4, "Z3": 53.5, "Z4": 23.2, "Z5": 19.7}
data = {"Z1": [], "Z2": [], "Z3": [], "Z4": [], "Z5": []}

def load_dataset():
    print("Cargando dataset real... esto tardará unos segundos.")
    # CAMBIA EL NOMBRE AQUÍ SI ES NECESARIO
    with open('open_buildings_v3_points_ne_110m_CHL.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                lat, lon = float(row['latitude']), float(row['longitude'])
                area, conf = float(row['area_in_meters']), float(row['confidence'])
                for zid, bbox in BOUNDING_BOXES.items():
                    if bbox["lat_min"] <= lat <= bbox["lat_max"] and bbox["lon_min"] <= lon <= bbox["lon_max"]:
                        data[zid].append({"area": area, "confidence": conf})
                        break
            except: continue
    print("Dataset cargado.")

@app.route('/query', methods=['POST'])
def handle_query():
    req = request.json
    q_type, zone, conf = req.get('type'), req.get('zone_id'), req.get('confidence_min', 0.0)
    
    if q_type == 'Q1': 
        res = sum(1 for r in data.get(zone, []) if r["confidence"] >= conf)
    elif q_type == 'Q2':
        areas = [r["area"] for r in data.get(zone, []) if r["confidence"] >= conf]
        res = {"avg": statistics.mean(areas) if areas else 0, "total": sum(areas)}
    elif q_type == 'Q3':
        res = len([r for r in data.get(zone, []) if r["confidence"] >= conf]) / zone_area_km2.get(zone, 1)
    elif q_type == 'Q5':
        scores = [r["confidence"] for r in data.get(zone, [])]
        counts, _ = np.histogram(scores, bins=5, range=(0, 1))
        res = counts.tolist()
    else: res = "OK"
    return jsonify({"result": res})

if __name__ == '__main__':
    load_dataset()
    app.run(host='0.0.0.0', port=5000)