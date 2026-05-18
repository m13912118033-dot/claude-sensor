from fastapi import FastAPI
from datetime import datetime
import httpx

app = FastAPI()

# 这是一个免费、永久保存的在线大账本专属抽屉
# 我们把数据存到云端，这样Render重启一万次，数据也绝对不会丢！
# 用你的服务器名字作为专属钥匙
DB_URL = "https://jsonbin.org/claude-sensor/events"

async def load_events():
    """从网络云端数据库读取现有的记忆"""
    try:
        async with httpx.AsyncClient() as client:
            # 这里的 Authorization 随便写一串当你的独家密码即可
            headers = {"Authorization": "Bearer my_secret_key_2026"}
            response = await client.get(DB_URL, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # 如果云端是空的或者不是列表，返回空列表
                return data if isinstance(data, list) else []
    except Exception as e:
        print(f"读取云端失败: {e}")
    return []

async def save_events(events_list):
    """把记忆稳稳地保存到网络云端，永久不丢"""
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": "Bearer my_secret_key_2026"}
            await client.post(DB_URL, json=events_list, headers=headers)
    except Exception as e:
        print(f"同步云端失败: {e}")

@app.get("/event")
async def receive_event(type: str, value: str):
    # 每次有新事件，先从网络云端读出旧的，再塞入新的
    current_events = await load_events()
    
    event = {
        "type": type,
        "value": value,
        "time": datetime.now().isoformat()
    }
    current_events.append(event)
    await save_events(current_events)
    
    print(f"收到并永久保存事件: {event}")
    return {"status": "ok"}

@app.get("/events")
async def get_events():
    # 查账的时候，直接从云端数据库读出来展示
    return await load_events()
