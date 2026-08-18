from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request

from v1_core import ExperienceStore, RaphaelGateway, RaphaelRunner


DATA_DIR = Path(os.getenv("RAPHAEL_DATA_DIR", ".raphael"))
gateway = RaphaelGateway(
    RaphaelRunner(DATA_DIR / "runs"),
    ExperienceStore(DATA_DIR / "experience.db"),
)
app = FastAPI(title="Raphael Gateway", version="0.1.0")


def _authorize(request: Request) -> None:
    expected = os.getenv("RAPHAEL_GATEWAY_KEY", "raphael-local")
    supplied = request.headers.get("authorization", "").removeprefix("Bearer ")
    if supplied != expected:
        raise HTTPException(status_code=401, detail="Invalid gateway key")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/models")
def models(request: Request) -> dict[str, Any]:
    _authorize(request)
    return {"object": "list", "data": [{
        "id": "raphael", "object": "model", "created": 0,
        "owned_by": "ryu-ai-orchestra",
    }]}


@app.post("/v1/chat/completions")
async def chat_completions(request: Request) -> dict[str, Any]:
    _authorize(request)
    body = await request.json()
    if body.get("stream"):
        raise HTTPException(status_code=400, detail="V0 supports non-streaming requests only")
    prepared = gateway.prepare(body.get("messages", []))
    model_content = _call_upstream(list(prepared.messages))
    result = gateway.finalize(prepared, model_content)
    return {
        "id": f"chatcmpl-{uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "raphael",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": result.reply},
            "finish_reason": "stop",
        }],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "raphael": {"task_id": result.task_id, "status": result.status},
    }


def _call_upstream(messages: list[dict[str, Any]]) -> str:
    api_key = os.getenv("UPSTREAM_API_KEY", "").strip()
    if not api_key:
        return json.dumps({
            "reply": "AI APIはまだ有効化していません。設定後も全依頼はRaphael Gatewayの検査を通ります。",
            "status": "working", "evidence": {},
        }, ensure_ascii=False)
    base_url = os.getenv("UPSTREAM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    upstream_model = os.getenv("UPSTREAM_MODEL", "gpt-5-mini")
    payload = json.dumps({
        "model": upstream_model,
        "messages": messages,
        "stream": False,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")
    upstream_request = urllib.request.Request(
        f"{base_url}/chat/completions", data=payload, method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(upstream_request, timeout=120) as response:
            upstream = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise HTTPException(status_code=502, detail=f"Upstream model failed: {error}") from error
    try:
        return upstream["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise HTTPException(status_code=502, detail="Unexpected upstream response") from error
