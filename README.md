# A2A Educational Assistant Platform

A modular, agent-based educational Q&A system that leverages web scraping, LLM-based critique, and answer refinement to deliver high-quality, information-rich answers to user questions. The system is built with FastAPI (Python) for backend microservices and a modern React/Vue frontend.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Backend Services](#backend-services)
- [Frontend](#frontend)
- [Setup Instructions](#setup-instructions)
  - [Backend](#backend)
  - [Frontend](#frontend-1)
- [Environment Variables](#environment-variables)
- [Running the System](#running-the-system)
- [API Endpoints](#api-endpoints)
- [Agent Registry](#agent-registry)
- [Pipeline Example](#pipeline-example)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Web Scraping**: Extracts educational content from the web using SERP API and BeautifulSoup.
- **LLM Critic**: Uses Groq’s Llama3-70b-8192 to critique answers and provide constructive feedback and scoring.
- **LLM Refiner**: Refines answers based on critic feedback for clarity, completeness, and technical accuracy.
- **Agent Registry**: Dynamic discovery and registration of microservices.
- **Orchestration**: Central entrypoint coordinates the pipeline: Scraper → Critic → (Refiner) → Critic.
- **Modern Frontend**: React/Vue-based UI for user interaction and answer display.

---

## Backend Services

- **MCP Orchestrator (`mcp_server.py`)**: Receives user questions, coordinates the pipeline, and returns the final answer and trace.
- **Scraper Tool (`dynamic_scraper_tool.py` / `scraper.py`)**: Scrapes educational content from the web using SERP API and BeautifulSoup.
- **Critic Tool (`critic.py`)**: Uses LLM to critique answers, provide feedback, and score (1-10).
- **LLM Refiner (`llm_refiner.py`)**: Refines answers based on critic feedback for improved quality.
- **Agent Registry (`agent_registry.json`, `registry_service.py`)**: Maintains a list of available agents and their endpoints.

---

## Frontend

- **Location**: `frontend/frontend/`
- **Stack**: React 19, Vue 3, Vite, Axios
- **Key Components**:
  - `QueryForm.jsx`: User input form
  - `AnswerDisplay.jsx`: Shows the final answer
  - `PipelineView.jsx`: Visualizes the pipeline trace
  - `header.jsx`, `HelloWorld.vue`: UI elements

---

## Setup Instructions

### Backend

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>/folder
   ```

2. **Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the `folder/` directory:
   ```env
   GROQ_API_KEY=your-groq-api-key
   SERP_API_KEY=your-serpapi-key
   REGISTRY_URL=http://localhost:9000
   ```

### Frontend

1. **Navigate to Frontend**
   ```bash
   cd ../frontend/frontend
   ```

2. **Install Node Dependencies**
   ```bash
   npm install
   ```

3. **Run the Frontend**
   ```bash
   npm run dev
   ```
   The app will be available at [http://localhost:5173](http://localhost:5173) (default Vite port).

---

## Environment Variables

- `GROQ_API_KEY`: API key for Groq LLM (required for critic and refiner).
- `SERP_API_KEY`: API key for SERP API (required for scraper).
- `REGISTRY_URL`: URL for the agent registry (default: `http://localhost:9000`).

---

## Running the System

**Start all backend services (in separate terminals):**

```bash
# In folder/
uvicorn mcp_server:app --host 0.0.0.0 --port 8000
uvicorn dynamic_scraper_tool:app --host 0.0.0.0 --port 8001
uvicorn critic:app --host 0.0.0.0 --port 8002
uvicorn llm_refiner:app --host 0.0.0.0 --port 8003
```

**Start the frontend:**

```bash
cd frontend/frontend
npm run dev
```

---

## API Endpoints

### MCP Orchestrator

- **POST `/ask`**
  - Request: `{ "question": "What is the capital of France?" }`
  - Response: `{ "answer": "...", "pipeline_trace": [...] }`

### Scraper Tool

- **POST `/a2a`**
  - Request: `{ "input": "What is ...?", "context": {} }`
  - Response: `{ "answer": "...", ... }`

### Critic Tool

- **POST `/a2a`**
  - Request: `{ "input": "...", "context": { "answer": "..." } }`
  - Response: `{ "score": 8, "feedback": "...", ... }`

### LLM Refiner

- **POST `/a2a`**
  - Request: `{ "input": "...", "context": { "answer": "...", "feedback": "..." } }`
  - Response: `{ "answer": "...", ... }`

### Health Checks

- **GET /** on any service returns a status message.

---

## Agent Registry

- **File**: `agent_registry.json`
- **Format**:
  ```json
  [
    { "name": "Scraper Tool", "url": "http://localhost:8001", "tags": ["scraper"] },
    { "name": "Critic Tool", "url": "http://localhost:8002", "tags": ["critic"] },
    { "name": "LLM Refiner", "url": "http://localhost:8003", "tags": ["llm"] }
  ]
  ```

Agents self-register on startup and can be discovered by tag.

---

## Pipeline Example

1. **User asks:** "What is the capital of France?"
2. **Scraper** fetches web content.
3. **Critic** scores and provides feedback.
4. If score < 9, **LLM Refiner** improves the answer.
5. **Critic** re-scores the refined answer.
6. **Final answer** and trace returned to the user.

---

## Troubleshooting

- **Registration Fails**: Ensure the registry is running and `REGISTRY_URL` is correct.
- **LLM Errors**: Check your `GROQ_API_KEY` and network connectivity.
- **Scraper Issues**: Ensure `SERP_API_KEY` is set and valid.
- **Dependency Issues**: Reinstall requirements and ensure Python/Node versions are compatible.

---

## Contact

For questions or support, contact [vardaangulati0@gmail.com] or open an issue in the repository. 


