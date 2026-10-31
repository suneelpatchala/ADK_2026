# ADK 2026: Google Agent Development Kit (ADK) & Evals

This repository demonstrates building, configuring, and evaluating production AI agents using Google's **Agent Development Kit (ADK)** powered by **Gemini 2.5 Flash** on **Google Cloud Vertex AI**.

---

## 📁 Project Structure

```text
ADK_2026/
├── my_agent/
│   ├── __init__.py                # Module initialization (exports agent)
│   ├── agent.py                   # Root agent definition & custom tools
│   ├── .env                       # Vertex AI environment variables
│   ├── eval_time.evalset.json     # Evaluation dataset (tool trajectory test cases)
│   └── eval_config.json           # Eval scoring metrics & pass/fail thresholds
├── run_evals.py                   # Automated evaluation runner script
├── requirements.txt               # Dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Google Cloud SDK (`gcloud`)** installed and authenticated

### 2. Environment Setup
Create and activate a virtual environment:

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install Google ADK
pip install google-adk
```

### 3. Google Cloud Authentication (Vertex AI)
Vertex AI uses **Application Default Credentials (ADC)** instead of a standard API key:

```powershell
gcloud auth application-default login
```

### 4. Configuration (`my_agent/.env`)
Configure your Google Cloud Project and target region inside `my_agent/.env`:

```env
# Enable Vertex AI (Enterprise) mode
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_GENAI_USE_ENTERPRISE=true

# Google Cloud Project & Region
GOOGLE_CLOUD_PROJECT=suneel-adk-2026
GOOGLE_CLOUD_LOCATION=us-east1
```

> **Note:** Ensure no `GEMINI_API_KEY` or `GOOGLE_API_KEY` is defined in `.env` or in your terminal session, as ADK will otherwise default to Google AI Studio.

---

## 🤖 The Agent (`my_agent/agent.py`)

The agent is exposed via the required **`root_agent`** variable and equipped with custom tools:

- **Model:** `gemini-2.5-flash` running on Vertex AI
- **Tools:** `get_current_time(city: str)` – Demonstrates autonomous function calling with structured inputs and type hints.

---

## 💬 Running the Agent

### Option A: Local Developer Web UI (Recommended)
Launch the visual interactive development server from the repository root:

```powershell
adk web
```
- Open `http://localhost:8000` in your browser.
- Select `my_agent` to chat, inspect real-time tool calls, and view session events.

### Option B: Terminal CLI Chat
To test conversational interactions directly inside your terminal:

```powershell
adk run
```

---

## 🧪 Agent Evaluations (Evals)

Because LLM outputs are non-deterministic, ADK provides an evaluation framework to test:
1. **Tool Trajectory:** Did the agent invoke the expected tool with the right arguments?
2. **Safety & Precision:** Did the agent avoid unnecessary tool calls during casual conversation?

### Evaluation Files
- **`my_agent/eval_time.evalset.json`**: Contains test scenarios:
  - `test_time_new_york`: Verifies that the agent calls `get_current_time` with `{"city": "New York"}`.
  - `test_greeting_no_tool`: Verifies that no tool calls are made for general inquiries.
- **`my_agent/eval_config.json`**: Sets pass/fail thresholds (e.g., `tool_trajectory_avg_score: 1.0`).

---

## ▶️ How to Execute Evals

### 1. Via ADK Web UI
1. Start `adk web` and navigate to `http://localhost:8000`.
2. Click the **Evals** tab in the top navigation bar.
3. Select `eval_time` and click **Run Eval** to view visual diffs and trajectory scores.

### 2. Via ADK CLI
Run evaluations directly from PowerShell with detailed results:

```powershell
adk eval my_agent my_agent/eval_time.evalset.json --config_file_path=my_agent/eval_config.json --print_detailed_results
```

### 3. Programmatically / CI Automation (`run_evals.py`)
Run the Python evaluation script:

```powershell
python run_evals.py
```
*(Can be integrated into CI/CD pipelines via `pytest`.)*
