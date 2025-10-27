from fastapi import APIRouter, HTTPException
from core.agent.recipe_agent import recipe_agent, Preference

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.post("/generate")
async def generate_recipe_route(pref: Preference):
    try:
        recipe = await recipe_agent.generate_recipe(pref)
        return recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
