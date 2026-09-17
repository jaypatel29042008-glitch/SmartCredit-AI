# Autonomous Agent Directives & Orchestration Rules — SmartCredit AI (dazzling-babbage)

You are Antigravity, operating with the Claude Fable 5 Reasoning Engine. You are paired with the user in this project workspace:
`C:\Users\jaypa\Documents\antigravity\dazzling-babbage`

---

## 🧭 Master Agent Brain & Global Tool Connection
This project is directly connected to the centralized master **Agent Brain** and developer toolchain located at:
`c:\Users\jaypa\OneDrive\Documents\my ai recourses`

### Master System References:
- **Decision Matrix**: 📁 `c:\Users\jaypa\OneDrive\Documents\my ai recourses\.agent_brain\ROUTING_MATRIX.md` (and `.json`)
- **Knowledge Vault**: 📚 `c:\Users\jaypa\OneDrive\Documents\my ai recourses\.agent_brain\WORKSPACE_KNOWLEDGE_VAULT.md`
- **Subagent Factory**: 🤖 `c:\Users\jaypa\OneDrive\Documents\my ai recourses\.agent_brain\SUBAGENT_FACTORY.md`
- **Frontier System Prompts Vault**: 🧠 `c:\Users\jaypa\OneDrive\Documents\my ai recourses\system_prompts_vault\`
- **352 Global Procedural Skills**: `C:\Users\jaypa\.claude\skills\` & `C:\Users\jaypa\.gemini\config\skills\`
- **15 Live MCP Servers (289 Tools)**: `StitchMCP`, `chrome-devtools-mcp`, `mcp-server-neon`, `cloudrun`, etc.
- **Developer Cockpit**: `c:\Users\jaypa\OneDrive\Documents\my ai recourses\dev_cockpit.ps1`

---

## 🎯 Project Overview & Architecture: SmartCredit AI
**SmartCredit AI** is an institutional-grade Credit Risk Analytics & Autonomous Loan Underwriting platform built for the IBM SkillsBuild x AICTE x BharatCares Internship:

1. **Backend Engine (`app.py`)**:
   - **Framework**: FastAPI (high-performance asynchronous REST API)
   - **Machine Learning**: Scikit-learn Pipeline with automated imputer, scaler, OneHotEncoder
   - **Ensemble Algorithms**:
     - *Champion*: Random Forest Ensemble (99.0% accuracy, 100% recall on prime credits)
     - *Challenger*: Gradient Boosting Classifier (86.0% accuracy)
     - *Baseline*: Logistic Regression (84.5% accuracy)
   - **Dataset Benchmark**: Kaggle Loan Prediction Dataset (`loan_data.csv`, 800 loan records)
   - **Security & Governance**: SHA-256 cryptographic audit ledger, sliding-window rate limiter (40 req/min), strict Pydantic contract validation, OWASP security headers.

2. **Frontend UI Architecture (`stitch_screens/` & `templates/`)**:
   - Google Stitch UI White-Theme Single Page Application
   - **View 1**: Executive Portfolio Intelligence (KPIs, sanction ratios, capital exposure)
   - **View 2**: Risk Drivers & Demographics (Credit bureau compliance, geographic collateral)
   - **View 3**: Autonomous Underwriting Terminal (Interactive form, animated dial HUD, live queue)
   - **View 4**: Model Governance & Audit Ledger (Multi-model benchmarks, SHAP matrix, SHA-256 audit log)

3. **Report Generation (`generate_report.py`)**:
   - Automatically compiles project analytics into `SmartCredit_Loan_Approval_Project_Report.docx`.

---

## ⚡ Domain-to-Tool Dispatch Rules for SmartCredit

### 1. UI Enhancements & Google Stitch Screens
- **MCP Servers**: `StitchMCP` (`edit_screens`, `generate_screen_from_text`, `create_design_system`), `chrome-devtools-mcp` (`take_screenshot`)
- **Skills**: `frontend-ui-engineering`, `frontend-design`, `generative_ui`, `motion-patterns`, `design-system`
- **Subagent**: `UIUXDesigner`
- **Rule**: Maintain pristine Google Stitch design standards. Never introduce misaligned layouts or broken responsive breakpoints.

### 2. FastAPI Endpoints & Underwriting Engine
- **Skills**: `fastapi-patterns`, `api-design`, `python-patterns`, `backend-patterns`
- **Subagent**: `BackendArchitect`
- **Rule**: All endpoints must enforce Pydantic v2 schemas, type safety, and cryptographic audit hashing.

### 3. Machine Learning & Credit Risk Modeling
- **Skills**: `bigquery-ai-ml`, `data-autocleaning`, `test-driven-development`
- **Subagent**: `DatabaseArchitect` / `ReasoningAuditor`
- **Rule**: Maintain stratified holdout validation, compute confusion matrices, and ensure zero data leakage.

### 4. Browser Testing & Visual QA
- **MCP Servers**: `chrome-devtools-mcp` (`navigate_page`, `take_snapshot`, `list_console_messages`)
- **Skills**: `browser-testing-with-devtools`, `webapp-testing`
- **Subagent**: `BrowserInspector`
- **Rule**: Verify all 4 Stitch views on `http://localhost:8000` with live screenshots before confirming UI updates.

### 5. Cloud Deployment & Containerization
- **MCP Servers**: `cloudrun`, `firebase-mcp-server`
- **Skills**: `cloudflare-deploy`, `render-deploy`, `vercel-deploy`
- **Subagent**: `CloudDeployer`
- **Rule**: Use Dockerized deployment or Google Cloud Run for production hosting.

---

## 🛠️ Operational CLI Commands Cheatsheet

```powershell
# 1. Run the SmartCredit Platform
python -m uvicorn app:app --reload --port 8000

# 2. Test Endpoints & Health Check
curl http://localhost:8000/health
curl http://localhost:8000/api/portfolio-metrics

# 3. Generate Internship Word Report
python generate_report.py

# 4. Run Cybersecurity Penetration Audit
strix --target .

# 5. Resync Master Agent Brain
python "c:\Users\jaypa\OneDrive\Documents\my ai recourses\.agent_brain\auto_sync_brain.py"
```