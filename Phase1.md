1. activate .venv
2. install requirements.txt
3. Create the below lean folder structure

ai_recipe_wizard/
│
├── services/
│   ├── api/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── routes/
│   │   │   │   ├── recipes.py
│   │   │   │   └── health.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   └── __init__.py
│
├── core/
│   ├── agent/
│   │   ├── recipe_agent.py
│   │   └── __init__.py
│   ├── memory/
│   │   ├── vector_store.py
│   │   └── __init__.py
│   └── config.py
│
├── requirements.txt
└── README.md

4. run the command,
pip install fastapi uvicorn openai chromadb python-dotenv

5. Create the file services/api/app/main.py, health.py and recipes.py with this simple version first

6. Run the Uvicorn,
> uvicorn services.api.app.main:app

Then test:

🩺 http://127.0.0.1:8000/health → {"status": "ok"}

🍲 http://127.0.0.1:8000/recipes/generate → {"message": "Recipe generation coming soon!"}

****************************************************************

🧠 Step 2 — Agent Logic Design
1️⃣ Purpose of the Recipe Agent

The Recipe Agent is the core “brain” of the MVP. Its responsibilities:
1. Input Parsing

Accept user preferences (diet, cuisine, ingredients, servings, skill level)

Validate input (ensure lists, optional fields, defaults)

2. Prompt Construction

Convert user input into a well-structured OpenAI prompt

Include instructions to return strict JSON:

{
  "title": "<recipe title>",
  "ingredients": ["item1", "item2", ...],
  "steps": ["step1", "step2", ...],
  "provenance": ["optional source or note"]
}


3. LLM Call

    Use OpenAI Chat API (gpt-4o-mini or gpt-4o)

    Async call from the agent

    Handle retries / errors

4. Response Parsing

    Extract JSON from LLM response

    Validate JSON fields

    Return structured RecipeOut object

5. Optional Persistence (MVP)

    Convert to database object and save via API route

    Store provenance or metadata if available

2️⃣ Interaction Flow Diagram
[Frontend Form] 
     │
     ▼
[API Route: /recipes/generate]
     │
     ▼
[Recipe Agent] ──► [Prompt Builder] ──► [OpenAI API] 
     │                      │
     │                      ▼
     │                 [LLM returns JSON-like text]
     ▼
[Agent JSON Parser / Validator]
     │
     ▼
[API Route returns structured JSON to frontend]


Each step is modular:

Prompt builder → can evolve into RAG later

JSON parser → can evolve into schema validation

Agent core → can later coordinate sub-agents (Verifier, Refiner)

3️⃣ Prompt Template (MVP)

Here’s a minimal but robust template to enforce JSON output:

You are an expert recipe generator. 

User preferences:
- Cuisine: {cuisine}
- Diet: {diet}
- Ingredients: {ingredients}
- Servings: {servings}
- Skill Level: {skill_level}

Instructions:
1. Generate one complete recipe.
2. Return **strict JSON only** with these fields:
{
  "title": "<recipe title>",
  "ingredients": ["item1", "item2", ...],
  "steps": ["step1", "step2", ...],
  "provenance": ["optional source or note"]
}
3. Ingredients must include user ingredients if possible.
4. Steps should be clear, concise, and ordered.
5. Do NOT include extra commentary or markdown.


{cuisine}, {diet}, etc. will be dynamically substituted in the agent.

The template can later evolve to include:

Nutritional info

RAG for prior recipes

User feedback refinement

4️⃣ Agent Function Skeleton

Methods / Functions:

Function	Purpose
generate_recipe(preferences)	Main function called by API route
_build_prompt(preferences)	Build structured prompt for LLM
_call_openai(prompt)	Async call to OpenAI API
_parse_response(response_text)	Extract valid JSON and return Recipe object

5️⃣ Why This Design is Modular

Separation of Concerns: API handles HTTP, Agent handles AI logic.

Easy to Extend: Later, you can add:

    Refiner agent (iterative improvement)

    Verifier agent (allergen / diet check)

    Vector DB retrieval (RAG)

Testable: Each function can be unit-tested independently:

    _build_prompt() → test string output

    _parse_response() → test JSON parsing

    _call_openai() → mock API call for CI

✅ After this design, the next step is implementing recipe_agent.py:

Create core/agent/recipe_agent.py

Implement:

    _build_prompt()

    _call_openai()

    _parse_response()

    generate_recipe()

Connect your API route /recipes/generate → Agent → Response