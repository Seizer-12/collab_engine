from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.services.connection import manager  # Import the instance
from app.schemas.message import EditorMessage
from app.core.database import SessionLocal
from app.crud.document import get_document, update_doc_content
import json


app = FastAPI()

@app.websocket("/ws/{doc_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, doc_id: int, user_id: str):
    # --- [UNCHANGED] ---
    await manager.connect(websocket, doc_id)
    
    # --- [NEW: INITIAL STATE LOAD] ---
    # We do this BEFORE the loop so the user sees text immediately
    db = SessionLocal()
    try:
        current_doc = get_document(db, doc_id)
        if current_doc:
            # Send ONLY to this specific websocket (not a broadcast)
            await websocket.send_json({
                "type": "INITIAL_STATE",
                "content": current_doc.content,
                "user_id": user_id
            })
            
        # --- [NEW: PRESENCE BROADCAST] ---
        # Tell everyone else that a new user is here
        await manager.broadcast(json.dumps({
            "type": "USER_JOINED",
            "user_id": user_id,
            "message": f"{user_id} joined the document"
        }), doc_id)
            
    finally:
        db.close()

    # --- [CONTINUE INTO LOOP: UNCHANGED LOGIC] ---
    try:
        while True:
            raw_data = await websocket.receive_text()
            data_dict = json.loads(raw_data)
            message = EditorMessage(**data_dict)
            
            if message.type == "EDIT":
                # We reuse our existing save-and-broadcast logic here
                db = SessionLocal()
                try:
                    update_doc_content(db, doc_id, message.content, user_id)
                    await manager.broadcast(message.json(), doc_id)
                finally:
                    db.close()

    except WebSocketDisconnect:
        manager.disconnect(websocket, doc_id)
        # --- [NEW: LEAVE PRESENCE] ---
        await manager.broadcast(json.dumps({
            "type": "USER_LEFT",
            "user_id": user_id
        }), doc_id)


