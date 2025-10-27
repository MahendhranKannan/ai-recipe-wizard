import json
from typing import List, Optional
from pydantic import BaseModel, Field
import httpx
from core.config import settings  # Assuming core/config.py holds OpenAI API key & model

# -----------------------------
# Pydantic Models
# -----------------------------

class Preference(BaseModel):
    cuisine: Optional[str] = None
    diet: Optional[str] = None
    ingredients: Optional[List[str]] = Field(default_factory=list)
    servings: Optional[int] = 1
    skill_level: Optional[str] = "beginner"

class RecipeOut(BaseModel):
    title: str
    ingredients: List[str]
    steps: List[str]
    provenance: Optional[List[str]] = None

# -----------------------------
# Recipe Agent
# -----------------------------

class RecipeAgent:
    def __init__(self, api_key: str = settings.openai_api_key, model: str = settings.openai_model):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"

    # Public function: called by API
    async def generate_recipe(self, preferences: Preference) -> RecipeOut:
        prompt = self._build_prompt(preferences)
        response_text = await self._call_openai(prompt)
        recipe = self._parse_response(response_text)
        return recipe

    # -----------------------------
    # Internal helpers
    # -----------------------------

    def _build_prompt(self, preferences: Preference) -> str:
        """
        Build a structured prompt for OpenAI with strict JSON instructions.
        """
        prompt = f"""
You are an expert recipe generator.

User preferences:
- Cuisine: {preferences.cuisine}
- Diet: {preferences.diet}
- Ingredients: {preferences.ingredients}
- Servings: {preferences.servings}
- Skill Level: {preferences.skill_level}

Instructions:
1. Generate one complete recipe.
2. Return strict JSON **only** with these fields:
{{
  "title": "<recipe title>",
  "ingredients": ["item1", "item2", ...],
  "steps": ["step1", "step2", ...],
  "provenance": ["optional source or note"]
}}
3. Ingredients must include user ingredients if possible.
4. Steps should be clear, concise, and ordered.
5. Do NOT include extra commentary or markdown.
"""
        return prompt

    async def _call_openai(self, prompt: str) -> str:
        """
        Async call to OpenAI Chat API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful recipe generator."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 800,
            "temperature": 0.8,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(self.base_url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"]

    def _parse_response(self, text: str) -> RecipeOut:
        """
        Extract JSON from the model response.
        """
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("No JSON found in model response.")
        json_text = text[start:end+1]
        parsed = json.loads(json_text)
        return RecipeOut(
            title=parsed.get("title", "Untitled Recipe"),
            ingredients=parsed.get("ingredients", []),
            steps=parsed.get("steps", []),
            provenance=parsed.get("provenance", None)
        )

# -----------------------------
# Single Agent Instance (for MVP)
# -----------------------------
recipe_agent = RecipeAgent()
