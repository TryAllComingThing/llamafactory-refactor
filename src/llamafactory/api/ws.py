# Copyright 2025 the LlamaFactory team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""WebSocket handlers for training monitoring and streaming chat."""

import asyncio
import json
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect, status

from .deps import get_engine_holder


async def handle_train_ws(websocket: WebSocket, run_id: str) -> None:
    r"""WebSocket endpoint for training monitoring.

    Pushes progress/log/loss/complete events to the connected client.
    """
    await websocket.accept()
    engine_holder = get_engine_holder()

    # Validate run_id
    if engine_holder.runner.current_run_id != run_id:
        await websocket.send_json({
            "type": "train:complete",
            "status": "error",
            "message": f"Run {run_id} not found or already finished.",
        })
        await websocket.close()
        return

    # Create a dedicated queue for this client
    queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
    engine_holder.runner.register_ws_queue(queue)

    try:
        while True:
            try:
                msg = await asyncio.wait_for(queue.get(), timeout=30.0)
                await websocket.send_json(msg)
                if msg.get("type") == "train:complete":
                    break
            except asyncio.TimeoutError:
                # Send heartbeat / keep-alive
                try:
                    await websocket.send_json({"type": "ping"})
                except Exception:
                    break
    except WebSocketDisconnect:
        pass
    finally:
        engine_holder.runner.unregister_ws_queue(queue)


async def handle_chat_ws(websocket: WebSocket) -> None:
    r"""WebSocket endpoint for streaming chat.

    Client sends:
        {"type": "chat:send", "messages": [...], "system": "...", "tools": "...",
         "max_new_tokens": 2048, "top_p": 0.9, "temperature": 0.6}

    Server sends:
        {"type": "chat:token", "text": "..."}
        {"type": "chat:done", "full_text": "..."}
    """
    await websocket.accept()
    engine_holder = get_engine_holder()

    if not engine_holder.is_model_loaded:
        await websocket.send_json({
            "type": "chat:error",
            "message": "No model loaded. POST /api/model/load first.",
        })
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            if data.get("type") != "chat:send":
                await websocket.send_json({
                    "type": "chat:error",
                    "message": f"Unknown message type: {data.get('type')}",
                })
                continue

            messages = data.get("messages", [])
            system = data.get("system")
            tools = data.get("tools")
            max_new_tokens = int(data.get("max_new_tokens", 2048))
            top_p = float(data.get("top_p", 0.9))
            temperature = float(data.get("temperature", 0.6))

            # Validate messages
            if not messages:
                await websocket.send_json({
                    "type": "chat:error",
                    "message": "Empty messages.",
                })
                continue

            try:
                full_text = ""
                async for token in engine_holder.stream_chat(
                    messages=messages,
                    system=system,
                    tools=tools,
                    max_new_tokens=max_new_tokens,
                    top_p=top_p,
                    temperature=temperature,
                ):
                    full_text += token
                    await websocket.send_json({
                        "type": "chat:token",
                        "text": token,
                    })

                await websocket.send_json({
                    "type": "chat:done",
                    "full_text": full_text,
                })
            except Exception as e:
                await websocket.send_json({
                    "type": "chat:error",
                    "message": f"Chat error: {str(e)}",
                })
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({
                "type": "chat:error",
                "message": f"Unexpected error: {str(e)}",
            })
        except Exception:
            pass
