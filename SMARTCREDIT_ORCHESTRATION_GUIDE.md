# 🚀 SmartCredit AI — Complete User & Orchestration Guide
> **IBM SkillsBuild x AICTE x BharatCares Capstone Project**  
> **Workspace**: `C:\Users\jaypa\Documents\antigravity\dazzling-babbage`  
> **Master Agent Brain**: `c:\Users\jaypa\OneDrive\Documents\my ai recourses`

---

## 📖 1. What is SmartCredit AI?
SmartCredit AI is a production-grade Credit Risk Analytics & Autonomous Loan Underwriting platform:
- **Champion ML Model**: Random Forest (99.0% accuracy, 100% recall on prime credits)
- **Challenger Models**: Gradient Boosting (86.0%) and Logistic Regression (84.5%)
- **Dataset**: Kaggle Loan Prediction Dataset (`loan_data.csv`, 800 applicant profiles)
- **Frontend**: Google Stitch UI Single Page Application (4 complete views: Portfolio KPIs, Risk Drivers, Underwriting Terminal, Governance & SHA-256 Audit Ledger)
- **Backend**: FastAPI REST API with sliding-window rate limiting, Pydantic v2 validation, and OWASP security headers.

---

## ⚡ 2. How to Run SmartCredit AI in 3 Seconds

### Option A: From Any PowerShell Window
```powershell
cd C:\Users\jaypa\Documents\antigravity\dazzling-babbage
python -m uvicorn app:app --reload --port 8000
```
Then open your browser to:
- 🌐 **Web Platform**: [http://localhost:8000](http://localhost:8000)
- 📚 **Interactive Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Option B: Using Our Dev Cockpit
In your PowerShell terminal:
```powershell
start-smartcredit
```
*(Added to `dev_cockpit.ps1` for instant launch!)*

---

## 🤖 3. How to Use Our Powerful Setup With SmartCredit

Whenever you are working on SmartCredit in **Antigravity** or **Claude Code**, here is how to deploy our specialized tools:

### A. To Modify or Add UI Screens (Google Stitch)
- **How to tell the AI**:
  > *"Use StitchMCP to refine the Underwriting Terminal view with modern dark-mode accent cards."*
- **What happens autonomously**:
  The AI will invoke `StitchMCP` (`edit_screens`, `generate_variants`) and apply `frontend-ui-engineering` to ensure typography, tokens, and layouts match production standards.

### B. To Test the Live App in the Browser (Chrome DevTools MCP)
- **How to tell the AI**:
  > *"Launch the app and use Chrome DevTools to take a screenshot of View 1 and test the loan submission form."*
- **What happens autonomously**:
  The AI will call `chrome-devtools-mcp` (`navigate_page`, `take_snapshot`, `click`, `fill`) to test the underwriting pipeline end-to-end and report back with visual screenshots.

### C. To Add Database Storage (Neon Postgres / Supabase)
- **How to tell the AI**:
  > *"Migrate the mock audit trail in app.py to our Neon Serverless Postgres database."*
- **What happens autonomously**:
  The AI will deploy the `DatabaseArchitect` subagent using `mcp-server-neon` to provision a Postgres schema, link connection strings, and persist all loan decisions.

### D. To Generate the Internship Word Report (.docx)
```powershell
python generate_report.py
```
This automatically produces `SmartCredit_Loan_Approval_Project_Report.docx` with all benchmark metrics, confusion matrices, and project deliverables.

### E. To Deploy SmartCredit to the Cloud (Live URL)
- **Option 1 (Google Cloud Run)**: Use `cloudrun` MCP server to deploy `app.py` in a container.
- **Option 2 (Render / Railway / Azure)**: Run `az webapp up` or deploy via Docker.

---

## 🗂️ 4. Key Files Reference

| File | Purpose |
| :--- | :--- |
| **`app.py`** | Main application: FastAPI API, ML model engine, and embedded Stitch frontend |
| **`loan_data.csv`** | 800-record Kaggle benchmark loan prediction dataset |
| **`generate_report.py`** | Script compiling the comprehensive internship project report |
| **`SmartCredit_Loan_Approval_Project_Report.docx`** | Formatted Word project documentation |
| **`stitch_screens/`** | Google Stitch design templates and HTML layouts |
| **`AGENTS.md`** | Antigravity autonomous agent instructions |
| **`CLAUDE.md`** | Claude Code CLI developer directives |