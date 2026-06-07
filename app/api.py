from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Agentic Insights Copilot", lifespan=lifespan)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    brief: dict
    status: str = "success"


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Agentic Insights Copilot</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #0b1120;
      color: #e8eaf0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 48px 16px;
    }

    header {
      text-align: center;
      margin-bottom: 40px;
    }

    header h1 {
      font-size: 2rem;
      font-weight: 700;
      color: #ffffff;
      letter-spacing: -0.5px;
    }

    header p {
      margin-top: 8px;
      font-size: 1rem;
      color: #8b94b0;
    }

    .card {
      background: #131c30;
      border: 1px solid #1e2d4a;
      border-radius: 12px;
      padding: 32px;
      width: 100%;
      max-width: 720px;
    }

    label {
      display: block;
      font-size: 0.85rem;
      font-weight: 600;
      color: #8b94b0;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 10px;
    }

    textarea {
      width: 100%;
      min-height: 110px;
      padding: 14px 16px;
      background: #0b1120;
      border: 1px solid #1e2d4a;
      border-radius: 8px;
      color: #e8eaf0;
      font-size: 1rem;
      font-family: inherit;
      resize: vertical;
      outline: none;
      transition: border-color 0.2s;
    }

    textarea:focus { border-color: #3b6aff; }

    button {
      margin-top: 16px;
      width: 100%;
      padding: 14px;
      background: #3b6aff;
      color: #ffffff;
      font-size: 1rem;
      font-weight: 600;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.2s;
    }

    button:hover:not(:disabled) { background: #2d55d6; }
    button:disabled { background: #1e2d4a; color: #8b94b0; cursor: not-allowed; }

    .spinner {
      display: none;
      margin: 32px auto 0;
      width: 36px;
      height: 36px;
      border: 3px solid #1e2d4a;
      border-top-color: #3b6aff;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }

    @keyframes spin { to { transform: rotate(360deg); } }

    .error {
      display: none;
      margin-top: 24px;
      padding: 14px 16px;
      background: #2a0f0f;
      border: 1px solid #7f1d1d;
      border-radius: 8px;
      color: #fca5a5;
      font-size: 0.9rem;
    }

    #results { display: none; margin-top: 32px; }

    #results h2 {
      font-size: 1.15rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid #1e2d4a;
    }

    .field { margin-bottom: 20px; }

    .field-label {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #3b6aff;
      margin-bottom: 6px;
    }

    .field-value {
      font-size: 0.95rem;
      color: #d0d5e8;
      line-height: 1.6;
    }

    .field-list {
      list-style: none;
      padding: 0;
    }

    .field-list li {
      padding: 6px 0 6px 16px;
      position: relative;
      font-size: 0.95rem;
      color: #d0d5e8;
      line-height: 1.5;
    }

    .field-list li::before {
      content: "–";
      position: absolute;
      left: 0;
      color: #3b6aff;
    }
  </style>
</head>
<body>
  <header>
    <h1>Agentic Insights Copilot</h1>
    <p>AI-powered analytics planning assistant</p>
  </header>

  <div class="card">
    <label for="question">Business Question</label>
    <textarea id="question" placeholder="e.g. How should we segment customers by engagement and profitability?"></textarea>
    <button id="submit-btn" onclick="submitQuestion()">Generate Brief</button>
    <div class="spinner" id="spinner"></div>
    <div class="error" id="error-box"></div>
  </div>

  <div class="card" id="results">
    <h2>Segmentation Brief</h2>
    <div id="brief-content"></div>
  </div>

  <script>
    async function submitQuestion() {
      const question = document.getElementById("question").value.trim();
      if (!question) return;

      const btn = document.getElementById("submit-btn");
      const spinner = document.getElementById("spinner");
      const errorBox = document.getElementById("error-box");
      const results = document.getElementById("results");

      btn.disabled = true;
      btn.textContent = "Generating…";
      spinner.style.display = "block";
      errorBox.style.display = "none";
      results.style.display = "none";

      try {
        const res = await fetch("/api/brief", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question })
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || "Request failed");
        }

        const data = await res.json();
        renderBrief(data.brief);
        results.style.display = "block";
      } catch (err) {
        errorBox.textContent = "Error: " + err.message;
        errorBox.style.display = "block";
      } finally {
        btn.disabled = false;
        btn.textContent = "Generate Brief";
        spinner.style.display = "none";
      }
    }

    function field(label, value) {
      return `<div class="field">
        <div class="field-label">${label}</div>
        <div class="field-value">${value}</div>
      </div>`;
    }

    function listField(label, items) {
      if (!items || items.length === 0) return "";
      const lis = items.map(i => `<li>${i}</li>`).join("");
      return `<div class="field">
        <div class="field-label">${label}</div>
        <ul class="field-list">${lis}</ul>
      </div>`;
    }

    function renderBrief(b) {
      document.getElementById("brief-content").innerHTML =
        field("Business Objective", b.business_objective) +
        field("Target Population", b.target_population) +
        field("Recommended Approach", b.recommended_segmentation_approach) +
        listField("Alternative Approaches", b.alternative_approaches) +
        listField("Suggested Variables", b.suggested_variables) +
        field("Recommended Method", b.recommended_method) +
        listField("Expected Deliverables", b.expected_deliverables) +
        listField("Assumptions & Risks", b.assumptions_and_risks) +
        listField("Missing Information", b.missing_information);
    }

    document.getElementById("question").addEventListener("keydown", function(e) {
      if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) submitQuestion();
    });
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML


@app.post("/api/brief", response_model=QueryResponse)
async def generate_brief_endpoint(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        from app.main import run_pipeline
        brief = run_pipeline(request.question)
        return QueryResponse(brief=brief.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok", "model": "groq"}
