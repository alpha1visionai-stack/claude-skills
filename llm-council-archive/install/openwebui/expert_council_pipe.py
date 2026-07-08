"""
title: Expert Council
author: alpha1visionai
version: 1.0
"""
from pydantic import BaseModel, Field
from typing import Optional, Generator
import httpx
import asyncio
import json


class Pipe:
    class Valves(BaseModel):
        OPENROUTER_API_KEY: str = Field(
            default="",
            description="OpenRouter API Key"
        )
        BASE_URL: str = Field(
            default="https://openrouter.ai/api/v1",
            description="OpenRouter Base URL"
        )
        CHAIRMAN_MODEL: str = Field(
            default="anthropic/claude-opus-4.8",
            description="Vorsitzenden-Modell für Stage 3"
        )

    def __init__(self):
        self.valves = self.Valves()
        self.type = "manifold"

    def pipes(self):
        return [
            {"id": "council", "name": "🏛️ Expert Council"},
        ]

    async def pipe(self, body, __event_emitter__=None, __user__=None):
        council_models = [
            "openai/gpt-4o",
            "anthropic/claude-3.5-sonnet",
            "google/gemini-2.0-flash-001",
            "meta-llama/llama-3.1-70b-instruct",
            "mistralai/mistral-large-2407",
        ]
        question = body["messages"][-1]["content"]
        await self._emit_status(__event_emitter__, "Stage 1/3: 5 Berater befragen...")
        responses = await self._call_models_parallel(council_models, question, body["messages"][:-1])
        await self._emit_status(__event_emitter__, "Stage 2/3: Peer-Review läuft...")
        review_prompt = self._build_review_prompt(responses, question)
        reviews = await self._call_models_parallel(council_models, review_prompt, [])
        await self._emit_status(__event_emitter__, "Stage 3/3: Vorsitzender synthetisiert...")
        synthesis_prompt = self._build_synthesis_prompt(question, responses, reviews)
        final = await self._call_model(self.valves.CHAIRMAN_MODEL, synthesis_prompt, [])
        yield final

    async def _emit_status(self, emitter, message):
        if emitter:
            await emitter({"type": "status", "data": {"description": message, "done": False}})

    async def _call_model(self, model, prompt, context):
        headers = {"Authorization": f"Bearer {self.valves.OPENROUTER_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": model, "messages": [*context, {"role": "user", "content": prompt}], "max_tokens": 4096}
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(f"{self.valves.BASE_URL}/chat/completions", json=payload, headers=headers)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]

    async def _call_models_parallel(self, models, prompt, context):
        async def call(m):
            try:
                resp = await self._call_model(m, prompt, context)
                return {"model": m, "response": resp}
            except Exception as e:
                return {"model": m, "error": str(e)}
        return await asyncio.gather(*[call(m) for m in models])

    def _build_review_prompt(self, responses, question):
        valid = [r for r in responses if "error" not in r]
        answers = [f"--- Antwort {chr(65+i)} ---\n{r['response']}\n" for i, r in enumerate(valid)]
        return f"Frage: {question}\n\nBewerte die folgenden {len(answers)} Antworten anonym.\nVergib Ränge 1 (beste) bis {len(answers)} (schlechteste).\nBegründe kurz.\n\n" + "\n".join(answers)

    def _build_synthesis_prompt(self, question, responses, reviews):
        valid_responses = [r for r in responses if "error" not in r]
        valid_reviews = [r for r in reviews if "error" not in r]
        resp_text = "\n\n".join([f"**{r['model']}**:\n{r['response']}" for r in valid_responses])
        review_text = "\n\n".join([str(r) for r in valid_reviews])
        return f"## Originalfrage\n{question}\n\n## Antworten der 5 Berater\n{resp_text}\n\n## Anonyme Peer-Reviews\n{review_text}\n\nErstelle jetzt das strukturierte Urteil:\n1. Konsens: Wo sind sich alle einig?\n2. Dissens: Wo gibt es echte Meinungsverschiedenheiten?\n3. Blinde Flecken: Was wurde übersehen?\n4. Empfehlung: Konkrete Handlungsoption\n5. Erster Schritt: Was ist die unmittelbare Aktion?"
