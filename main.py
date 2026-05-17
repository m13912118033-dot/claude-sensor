from fastapi import FastAPI
from datetime import datetime
import json
import os

app = FastAPI()

# 记忆文件的存放路径
MEMORY_FILE = "events.json"

def load_events():
    """从文件里读取现有的记忆"""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_events(events_list):
    """把记忆稳稳地保存到文件里，防止断电失忆"""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(events_list, f, ensure_ascii=False, indent=4)

@app.get("/event")
def receive_event(type: str, value: str):
    # 每次有新事件，先读出旧的，再塞入新的
    current_events = load_events()
    
    event = {
        "type": type,
        "value": value,
        "time": datetime.now().isoformat()
    }
    current_events.append(event)
    save_events(current_events)
    
    print(f"收到并保存事件: {event}")
    return {"status": "ok"}

@app.get("/events")
def get_events():
    # 查账的时候，直接从文件里读出来展示
    return load_events()
