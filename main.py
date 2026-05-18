from fastapi import FastAPI
from datetime import datetime
import json
import os

app = FastAPI()

FILE = "events.json"

def load():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

@app.get("/event")
def receive_event(type: str, value: str):
    events = load()
    events.append({
        "type": type,
        "value": value,
        "time": datetime.now().isoformat()
    })
    save(events)
    return {"status": "ok"}

@app.get("/events")
def get_events():
    return load()
