from fastapi import FastAPI
from services.api.app.routes import health, recipes

app = FastAPI(title="AI Recipe Wizard - MVP")

# Include routes
app.include_router(health.router)
app.include_router(recipes.router)
