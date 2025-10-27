# 🧠 AI Recipe Wizard — System Architecture

An **agent-based autonomous AI cooking assistant** that generates and refines recipes from user preferences such as **diet, cuisine, and ingredients**.

---

## 🏗️ High-Level Architecture Overview


---

## ⚙️ Core Components

### 1. **Frontend (Streamlit / Gradio)**
- User-facing interface for entering preferences and viewing results.
- Features:
  - Form for diet, cuisine, ingredients.
  - Display generated recipes, ingredient lists, and nutrition facts.
  - Rate/refine recipes interactively.
  - Optionally upload ingredient photos.
- Communicates with the FastAPI backend through REST endpoints.

---

### 2. **Backend API (FastAPI)**
- Central service layer that:
  - Exposes REST endpoints (`/generate`, `/refine`, `/search`).
  - Hosts the **Agent Orchestrator** that manages all reasoning steps.
  - Manages user profiles, recipe storage, and embeddings.
- Uses async I/O for scalability.

---

### 3. **Agent Orchestrator (Core Logic)**
A modular pipeline that handles reasoning and generation using multiple cooperating agents:

| Agent Role | Responsibility |
|-------------|----------------|
| **Planner** | Converts user intent into structured subtasks (e.g., retrieve → adapt → verify). |
| **Retriever** | Searches the Vector DB for similar recipes, prior user history, and inspiration context. |
| **Synthesizer** | Crafts and executes structured LLM prompts (OpenAI API) to generate recipes. |
| **Verifier** | Ensures constraints (dietary, allergen, nutritional balance) are satisfied. |
| **Refiner** | Incorporates user feedback and improves recipes over iterations. |

🧩 *This modular design allows easy extension — e.g., adding a shopping list generator or calorie optimizer later.*

---

### 4. **Vector Database (Chroma / FAISS)**
- Stores embeddings for:
  - Recipe content.
  - User preferences.
  - Prior interactions and feedback.
- Enables **Retrieval-Augmented Generation (RAG)** for grounding and consistency.
- Periodically re-embeds data for model upgrades.

---

### 5. **Relational Database (Postgres / SQLite)**
- Stores:
  - User profiles and preferences.
  - Generated and saved recipes.
  - Feedback and rating data.
- Links records with corresponding embeddings in the Vector DB.

---

### 6. **Object Storage (S3 / Local)**
- Stores:
  - Uploaded images (ingredients, results).
  - Exported recipe PDFs.
  - Analytical logs and backups.

---

### 7. **Background Workers (Celery / FastAPI BackgroundTasks)**
- Executes long-running and async jobs:
  - Re-embedding old recipes.
  - Generating exports.
  - Aggregating analytics or personalization updates.

---

### 8. **Monitoring & Observability**
- **Sentry / Prometheus / Logs** for:
  - LLM usage and cost monitoring.
  - Request latency.
  - Error tracking and prompt audit trails.

---

### 9. **CI/CD and Deployment**
- **Containerized** using Docker.
- **Automated tests & linting** via GitHub Actions.
- Deployable to **Cloud Run / Azure App Service / AWS ECS**.
- Configurable environment management through `.env` or `config.py`.

---

## 🔄 Data Flow Overview

**Data Flow (Step-by-Step):**

1. **User → Frontend:**  
   User submits preferences (diet, cuisine, ingredients) through the web interface.

2. **Frontend → FastAPI Backend:**  
   The UI sends a structured request to the FastAPI backend.

3. **Backend → Orchestrator:**  
   FastAPI receives the request and delegates it to the Agent Orchestrator.

4. **Orchestrator → Planner:**  
   The Orchestrator passes user goals to the Planner agent, which decomposes them into subtasks.

5. **Planner → Retriever:**  
   Subtasks from the Planner are given to the Retriever, which queries the Vector DB for relevant recipes and user history.

6. **Retriever → Synthesizer:**  
   The retrieved context and subtasks are supplied to the Synthesizer, which uses the LLM (OpenAI API) to generate a draft recipe.

7. **Synthesizer → Verifier:**  
   The draft recipe is handed to the Verifier to check for dietary, allergen, and nutritional constraints.

8. **Verifier → Refiner:**  
   Verification results (issues or suggestions) and user feedback (if available) are provided to the Refiner, which adjusts and improves the recipe.

9. **Refiner → Storage & Frontend:**  
   The finalized recipe is stored in the Relational DB and Vector DB, and the result is returned to the UI for user presentation.


---

## 🧩 Key Design Principles

- **Separation of Concerns** → UI, API, Agents, Storage layers.
- **Retrieval-Augmented Generation (RAG)** → enhances factual grounding.
- **Agent Modularity** → plug-in new capabilities easily.
- **Structured Outputs** → JSON responses for ingredients, steps, nutrition, provenance.
- **Data Privacy** → minimal PII, encrypted storage, and opt-out for data saving.
- **Scalability & Extensibility** → async FastAPI + background workers + vector retrieval.

---

## 🧠 Future Extensions

| Feature | Description |
|----------|--------------|
| **Shopping List Generator** | Automatically extracts ingredients into a grocery list. |
| **Calorie & Nutrition Analyzer** | Adds nutritional scoring via APIs. |
| **Image-Based Ingredient Recognition** | Uses Vision model for ingredient uploads. |
| **Conversational Mode** | Persistent chat-like cooking assistant with memory. |

---

## 🧱 Technology Stack

| Layer | Technology |
|--------|-------------|
| **Frontend** | Streamlit / Gradio |
| **Backend API** | FastAPI (Python) |
| **LLM Interface** | OpenAI API |
| **Vector DB** | Chroma / FAISS |
| **Database** | PostgreSQL / SQLite |
| **Workers** | Celery / BackgroundTasks |
| **Storage** | AWS S3 / Local FS |
| **CI/CD** | Docker + GitHub Actions |
| **Monitoring** | Sentry / Prometheus |

---

## 🔐 Security & Privacy Considerations

- Sanitize all user input and uploaded files.  
- Encrypt sensitive recipe metadata and user identifiers.  
- Rate-limit API calls to control OpenAI usage costs.  
- Cache frequent requests for common diets/cuisines.  
- Provide an “opt-out” toggle for saving user preferences.

---

## 📈 Scalability Considerations

- **Async FastAPI** for concurrency and non-blocking LLM calls.  
- **Caching layer (Redis)** for repeated requests and embedding reuse.  
- **Vector DB partitioning** for user-level isolation.  
- **Batch re-embedding** to refresh data on model upgrades.  
- **Cloud-native deployment** for horizontal scaling.

---

> 🧑‍🍳 *AI Recipe Wizard demonstrates key AI engineering skills — agent-based orchestration, RAG, structured LLM prompts, and multi-model reasoning — essential for a production-grade AI portfolio project.*

