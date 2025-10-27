from fastapi import APIRouter

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/generate")
def generate_recipe():
    return {"message": "Recipe generation coming soon!"}
