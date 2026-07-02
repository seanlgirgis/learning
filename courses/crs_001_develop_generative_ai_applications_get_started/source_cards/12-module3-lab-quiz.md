# Module 3 — Lab + final quiz reinforcement

Import after `11-module2-quiz.md`. Cards from Cloud IDE lab + post-course quizzes.

---

## Model selection & evaluation

- Nina's **first** step when picking a model for a critical task? >>A)
    - Write a clear definition of the use case and requirements
    - Choose the model with the best performance rating
    - Select the most cost-effective model
    - Deploy with minimal configuration

- Why send the **same prompt** to different models? >>A)
    - It allows consistent evaluation across models
    - It eliminates the need for guardrails
    - It reduces deployment complexity
    - It ensures faster integration into production

- Emily comparing Llama, Granite, Mistral should prioritize? >>A)
    - Evaluate model performance, accuracy, and reliability
    - Choose the model with the largest number of features
    - Rely on the model's documentation quality
    - Select the model with the fastest response time only

- Leila comparing market models should analyze? >>A)
    - The model's performance, speed, reliability, and cost
    - The size of the model's training dataset only
    - The frequency of API updates
    - The popularity of the model

- After deployment, Priya should? >>A)
    - Continuously test and update the model as needed
    - Avoid switching models to reduce complexity
    - Skip performance monitoring unless issues arise
    - Rely on initial test results only

---

## Prompting techniques

- Technique that provides **examples** to guide responses? >>A)
    - Few-shot prompting
    - Zero-shot prompting
    - Chain-of-thought prompting
    - Random prompting

- Domain-specific tasks in **real GenAI apps** (your labs) — first lever? >>A)
    - RAG + prompt templates + few-shot (not weight fine-tuning first)
    - Fine-tune model weights before any prompting
    - Random prompting for diversity
    - Zero-shot only for every task

- Structured JSON for support tickets — focus on? >>A)
    - Prompts that clearly articulate the use case and required output shape
    - Ignoring the model's guardrails
    - Using complex language
    - Focusing on the model's training data

---

## Module 3 lab code

- Skills Network watsonx auth in this lab? >>A)
    - `Credentials(url=...)` only — no `api_key` in code; `project_id="skills-network"`
    - Always pass `api_key=os.environ["WATSONX_APIKEY"]` in Credentials
    - Hardcode API key in `config.py`
    - Use only `OPENAI_API_KEY`

- Why did `llama-3-2-11b-vision-instruct` fail on SN? >>A)
    - Not in the IDE's supported model list — use Maverick ID instead
    - Granite tokens were missing
    - Flask was not installed
    - JsonOutputParser was not imported

- `llm_test.py` gets model IDs how? >>A)
    - Imports `model` → `model` imports `config` (indirect chain)
    - Imports `config` directly in `llm_test.py`
    - Reads `config.py` from Flask request
    - Hardcoded inside `llm_test.py` only

- `model.py` in the Flask lab is? >>A)
    - The AI utility module — templates, chains, per-model functions
    - The Flask HTTP router
    - The HTML template folder
    - The Redis session store

- `AIResponse` + `JsonOutputParser` returns? >>A)
    - A Python dict with keys like summary, sentiment, response
    - Only a plain string
    - A Chroma document
    - An HTTP status code

---

## Data sovereignty & delivery

- Strict data sovereignty — best approach among quiz options? >>A)
    - Run the model on company / on-prem infrastructure
    - Host using external APIs
    - Share data to public cloud platforms
    - Rely on large external datasets

- Production GenAI exposure pattern (industry default)? >>A)
    - Web API (REST/FastAPI) with server-side chains — not embedding LLM in client
    - Email the model weights to users
    - Run everything in the browser only
    - One global Python list for all users' history

- Stateful chat: client holds? >>A)
    - `session_id` on every request; server holds message history keyed by that ID
    - The watsonx API key in localStorage
    - The model weights
    - Nothing — HTTP is automatically stateful