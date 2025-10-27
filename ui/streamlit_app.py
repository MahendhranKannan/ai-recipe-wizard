# ui/streamlit_app.py

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recipes/generate"  # your FastAPI endpoint

# Page Configuration
st.set_page_config(page_title="🍳 AI Recipe Wizard", layout="centered")
st.title("🍳 AI Recipe Wizard")
st.markdown("Generate intelligent recipes with AI — based on your preferences.")

# --- Input Form ---
with st.form("recipe_form"):
    cuisine = st.text_input("Cuisine (e.g., Italian, Indian, Mexican)", "")
    diet = st.selectbox("Diet Type", ["", "vegetarian", "vegan", "non-vegetarian", "keto", "pescatarian"])
    ingredients = st.text_area("Ingredients (comma separated)", "")
    servings = st.number_input("Servings", min_value=1, max_value=10, value=1)
    skill_level = st.selectbox("Skill Level", ["beginner", "intermediate", "expert"])
    
    submitted = st.form_submit_button("Generate Recipe")

# --- Call Backend ---
if submitted:
    if not ingredients.strip():
        st.warning("Please enter at least one ingredient.")
    else:
        payload = {
            "cuisine": cuisine or None,
            "diet": diet or None,
            "ingredients": [i.strip() for i in ingredients.split(",") if i.strip()],
            "servings": servings,
            "skill_level": skill_level
        }

        with st.spinner("Cooking something special... 🍲"):
            try:
                response = requests.post(API_URL, json=payload, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    recipe = data.get("recipe") or data  # depending on backend structure

                    st.subheader(recipe.get("title", "Untitled Recipe"))
                    st.markdown("### 🧂 Ingredients")
                    st.write("\n".join([f"- {ing}" for ing in recipe.get("ingredients", [])]))
                    st.markdown("### 👩‍🍳 Steps")
                    for idx, step in enumerate(recipe.get("steps", []), 1):
                        st.write(f"{idx}. {step}")
                    
                    if recipe.get("provenance"):
                        st.markdown("### 📚 Provenance / Inspirations")
                        st.write("\n".join([f"- {src}" for src in recipe.get("provenance", [])]))
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"Error contacting API: {str(e)}")
