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
