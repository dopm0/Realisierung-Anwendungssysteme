import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from io import BytesIO
from zipfile import ZipFile

# === KONFIGURATION ===
FILTER_ID = 4169        # Day-Ahead-Marktpreis Deutschland/Luxemburg
REGION = "DE"
RESOLUTION = "quarterhour"
ZEITRAUM = 365
ZUKUNFT = 1

# Zeitraum: letztes Jahr
#end_date = datetime.now()
end_date = datetime.now() + timedelta(days=ZUKUNFT)
start_date = end_date - timedelta(days=ZEITRAUM)
start_ts = int(start_date.timestamp() * 1000)
end_ts = int(end_date.timestamp() * 1000)

# === BASIS-URL ===
base_url = "https://www.smard.de/app/chart_data"

# === 1. Index laden ===
index_url = f"{base_url}/{FILTER_ID}/{REGION}/index_{RESOLUTION}.json"
response = requests.get(index_url)
if not response.ok:
    raise Exception(f"Fehler beim Abrufen des Index: {response.status_code}")

# ZIP oder JSON
content = response.content
if content[:2] == b'PK':
    with ZipFile(BytesIO(content)) as zip_file:
        json_filename = zip_file.namelist()[0]
        with zip_file.open(json_filename) as f:
            index_data = json.load(f)
else:
    index_data = json.loads(content.decode("utf-8"))

# Zeitstempel als ms
raw_timestamps = index_data.get("timestamps", index_data)
timestamps = []
for ts in raw_timestamps:
    if isinstance(ts, pd.Timestamp):
        ts = int(ts.timestamp() * 1000)
    elif isinstance(ts, datetime):
        ts = int(ts.timestamp() * 1000)
    else:
        ts = int(ts)
    timestamps.append(ts)
timestamps = sorted(timestamps)

# Segmente bestimmen
segment_start_ts = max(ts for ts in timestamps if ts <= start_ts)
segment_end_ts = max(ts for ts in timestamps if ts <= end_ts)
segment_list = [ts for ts in timestamps if segment_start_ts <= ts <= segment_end_ts]

# === 2. Datenblöcke laden ===
all_data = []
unit = None
aggregation = None
description = None

for seg_ts in segment_list:
    data_url = f"{base_url}/{FILTER_ID}/{REGION}/{FILTER_ID}_{REGION}_{RESOLUTION}_{seg_ts}.json"
    resp = requests.get(data_url)
    if not resp.ok:
        print(f"⚠️ Fehler bei Segment {seg_ts}: {resp.status_code}")
        continue

    content = resp.content
    if content[:2] == b'PK':
        with ZipFile(BytesIO(content)) as zip_file:
            json_filename = zip_file.namelist()[0]
            with zip_file.open(json_filename) as f:
                raw_json = json.load(f)
    else:
        raw_json = json.loads(content.decode("utf-8"))

    # === Robuste Metadaten-Extraktion ===
    if unit is None:
        meta_source = raw_json.get("meta", raw_json.get("data", {}))
        unit = meta_source.get("unit", "€/MWh")
        aggregation = meta_source.get("aggregation", RESOLUTION)
        description = meta_source.get("description", "Day-Ahead-Marktpreis "+REGION)

    # Zeitreihe holen
    series = raw_json.get("series", list(raw_json.values())[0])
    all_data.extend(series)

# === 3. DataFrame erstellen ===
df = pd.DataFrame(all_data, columns=["timestamp", "price"])
df = df[(df["timestamp"] >= start_ts) & (df["timestamp"] <= end_ts)].copy()
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df = df.set_index("timestamp")

# === Metadaten-Spalten ===
df["Unit"] = unit
df["aggregation"] = aggregation
df["Source"] = "Smard.de"

# === Neue Spalte: prediction = True für künftige Zeitpunkte ===
df["prediction"] = df.index > datetime.now()

# === 4. Ausgabe ===
print("📊 METADATEN:")
print(f"📝 Beschreibung:  {description}")
print(f"📏 Einheit:       {unit}")
print(f"🕒 Aggregation:   {aggregation}\n")

#print(df.head(100))
print(df.tail(100))
print(f"\n✅ Erfolgreich geladen: {len(df)} Stundenwerte von {df.index.min()} bis {df.index.max()}")

# === Optional speichern ===
# df.to_csv("strompreise_mit_meta.csv")
