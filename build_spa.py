# -*- coding: utf-8 -*-
import re
import os

WORKSPACE_DIR = r"c:\Users\jaypa\Documents\antigravity\dazzling-babbage"

def load_screen(name):
    path = os.path.join(WORKSPACE_DIR, "stitch_screens", f"{name}.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    head = re.search(r'<head[^>]*>(.*?)</head>', html, re.DOTALL | re.I).group(1)
    main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL | re.I)
    main = main_match.group(1) if main_match else ""
    footer_match = re.search(r'<footer[^>]*>(.*?)</footer>', html, re.DOTALL | re.I)
    footer = footer_match.group(0) if footer_match else ""
    return head, main, footer

p_head, p_main, p_footer = load_screen("portfolio")
_, r_main, _ = load_screen("risk_drivers")
_, u_main, _ = load_screen("underwriting")
_, g_main, _ = load_screen("governance")

# Clean conflicting inline scripts from screens
u_main = re.sub(r'<script.*?</script>', '', u_main, flags=re.DOTALL | re.I)
p_main = re.sub(r'<script.*?</script>', '', p_main, flags=re.DOTALL | re.I)
r_main = re.sub(r'<script.*?</script>', '', r_main, flags=re.DOTALL | re.I)
g_main = re.sub(r'<script.*?</script>', '', g_main, flags=re.DOTALL | re.I)

# -------------------------------------------------------------
# 1. ENHANCE UNDERWRITING SCREEN (View 3)
# -------------------------------------------------------------
# Replace static credit score card with interactive slider & sync box
credit_pattern = re.compile(
    r'<div class="flex flex-col gap-space-xs">\s*<label[^>]*>\s*<span>Bureau Credit Score</span>.*?</label>\s*<div class="flex items-center gap-space-xs bg-surface-container-lowest[^"]*">.*?</div>\s*</div>',
    re.DOTALL
)

interactive_credit_html = '''<div class="flex flex-col gap-2 bg-surface-container-lowest p-3 rounded-lg shadow-inner border border-outline-variant/30">
  <div class="flex items-center justify-between">
    <label class="font-label-md text-label-md text-on-surface font-semibold flex items-center gap-1.5">
      <span class="material-symbols-outlined text-secondary text-base">verified</span>
      <span>Bureau Credit Score</span>
    </label>
    <span id="credit-tier-badge" class="px-2 py-0.5 rounded text-xs font-bold uppercase bg-secondary/15 text-secondary">
      Optimal Tier (755)
    </span>
  </div>
  <div class="flex items-center gap-3 pt-1">
    <input id="inp-credit-score-slider" type="range" min="300" max="850" value="755" step="5" class="w-full accent-secondary cursor-pointer h-2 bg-surface-container-high rounded-lg" oninput="syncCreditScore(this.value)">
    <input id="inp-credit-score" type="number" min="300" max="850" value="755" class="w-16 px-2 py-1 bg-surface-container-high text-on-surface font-bold text-center rounded-md border border-outline-variant/40 focus:outline-none focus:ring-1 focus:ring-secondary text-sm" oninput="syncCreditScore(this.value)">
  </div>
  <div class="flex items-center justify-between text-[10px] text-outline font-semibold px-0.5">
    <span class="text-error font-semibold">300 (Subprime &lt;600)</span>
    <span class="text-secondary font-semibold">650 (Prime Gating)</span>
    <span class="text-on-tertiary-container font-semibold">850 (Super-Prime)</span>
  </div>
</div>'''

if credit_pattern.search(u_main):
    u_main = credit_pattern.sub(interactive_credit_html, u_main, count=1)
    print("Replaced static credit score with interactive controller")
else:
    print("Warning: Credit pattern regex did not match")

# Add IDs to Underwriting Screen Elements
u_main = re.sub(
    r'<span class="px-space-xs py-0.5 rounded bg-secondary/20 text-secondary font-label-sm text-label-sm uppercase font-bold tracking-wide">SANCTIONED \(LOW RISK\)</span>',
    r'<span id="hud-verdict-badge" class="px-space-xs py-0.5 rounded bg-secondary/20 text-secondary font-label-sm text-label-sm uppercase font-bold tracking-wide">SANCTIONED (LOW RISK)</span>',
    u_main
)

u_main = re.sub(
    r'<span class="font-headline-md text-headline-md text-on-surface font-semibold tracking-tight mt-0.5">Facility Sanction Recommended</span>',
    r'<span id="hud-verdict-title" class="font-headline-md text-headline-md text-on-surface font-semibold tracking-tight mt-0.5">Facility Sanction Recommended</span>',
    u_main
)

u_main = re.sub(
    r'<p class="font-body-md text-body-md text-on-surface leading-relaxed">\s*Issue formal sanction letter at prime rate.*?</p>',
    r'<p id="hud-prescriptive-directive" class="font-body-md text-body-md text-on-surface leading-relaxed">Issue formal sanction letter at prime rate (<span class="font-metric-md text-metric-md text-secondary font-semibold">8.25% APR</span>). Standard property mortgage first-lien registration required prior to capital disbursement. Loan-to-Value (<span class="text-tertiary font-semibold">71.4% LTV</span>) adheres to Basel III Risk-Weighted Capital Directive Section 4b. No secondary guarantor requirement triggered.</p>',
    u_main,
    flags=re.DOTALL
)

u_main = re.sub(
    r'<tbody class="divide-y divide-surface-container-high">',
    r'<tbody id="underwriting-queue-body" class="divide-y divide-surface-container-high">',
    u_main,
    count=1
)

# Connect Run Underwriting, Benchmark & Reset Buttons in u_main
u_main = re.sub(
    r'<button[^>]*id="btn-run-underwriting"[^>]*>',
    r'<button id="btn-run-underwriting" onclick="runUnderwriting()" type="button" class="w-full sm:flex-1 py-space-md px-space-lg bg-primary hover:bg-primary-fixed-dim text-on-primary-fixed rounded-lg font-headline-sm text-headline-sm font-semibold flex items-center justify-center gap-space-xs transition-all transform active:scale-[0.99] shadow-[0_0_24px_rgba(192,193,255,0.35)] cursor-pointer">',
    u_main
)

u_main = re.sub(
    r'<button[^>]*id="btn-benchmark"[^>]*>',
    r'<button id="btn-benchmark" onclick="loadBenchmark()" title="Load Benchmark Profile" type="button" class="flex-1 sm:flex-none p-space-md bg-surface-container-high hover:bg-surface-container-highest text-on-surface-variant hover:text-on-surface rounded-lg transition-colors flex items-center justify-center gap-space-xs cursor-pointer">',
    u_main
)

u_main = re.sub(
    r'<button[^>]*id="btn-reset"[^>]*>',
    r'<button id="btn-reset" onclick="resetForm()" title="Reset Parameters" type="button" class="flex-1 sm:flex-none p-space-md bg-surface-container-high hover:bg-surface-container-highest text-on-surface-variant hover:text-on-surface rounded-lg transition-colors flex items-center justify-center cursor-pointer">',
    u_main
)

# Connect Sanction Letter and Disbursal Buttons in u_main
u_main = re.sub(
    r'<button[^>]*id="btn-sanction-letter"[^>]*>',
    r'<button id="btn-sanction-letter" onclick="openSanctionModal()" type="button" class="w-full sm:flex-1 py-space-sm px-space-md rounded-lg bg-secondary text-on-secondary font-headline-sm text-headline-sm font-semibold flex items-center justify-center gap-space-xs hover:bg-secondary-fixed transition-all cursor-pointer shadow-[0_0_20px_rgba(78,222,163,0.3)] active:scale-[0.99]">',
    u_main
)

u_main = re.sub(
    r'<button[^>]*id="btn-route-disbursal"[^>]*>',
    r'<button id="btn-route-disbursal" onclick="triggerDisbursalToast()" type="button" class="w-full sm:flex-1 py-space-sm px-space-md rounded-lg bg-primary-container text-on-primary font-headline-sm text-headline-sm font-semibold flex items-center justify-center gap-space-xs hover:bg-primary transition-all cursor-pointer shadow-[0_0_18px_rgba(128,131,255,0.3)] active:scale-[0.99]">',
    u_main
)

# -------------------------------------------------------------
# 2. ENHANCE GOVERNANCE SCREEN (View 4)
# -------------------------------------------------------------
audit_trail_enhanced = '''<!-- Real-Time Cryptographic Decision Ledger -->
<div class="bg-surface-container/90 backdrop-blur-xl rounded-xl p-space-lg shadow-xl flex flex-col gap-space-md">
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-space-xs">
      <span class="material-symbols-outlined text-tertiary text-base">lock</span>
      <h3 class="font-headline-sm text-headline-sm text-on-surface font-semibold">Cryptographic Audit Trail (SHA-256)</h3>
    </div>
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 rounded-full bg-secondary animate-ping"></span>
      <span class="font-label-sm text-secondary uppercase font-semibold">Live Feed</span>
    </div>
  </div>

  <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2">
    <div class="relative flex-1">
      <span class="material-symbols-outlined absolute left-2.5 top-1/2 -translate-y-1/2 text-outline text-sm">search</span>
      <input id="audit-search" type="text" placeholder="Filter ledger by App ID, Verdict, or SHA-256..." oninput="filterAuditTable(this.value)" class="w-full pl-8 pr-3 py-1.5 rounded-lg bg-surface-container-lowest border border-outline-variant/40 text-xs text-on-surface placeholder:text-outline focus:outline-none focus:ring-1 focus:ring-secondary">
    </div>
    <div class="flex items-center gap-1.5">
      <a href="/api/export-audit-csv" download="smartcredit_audit_ledger.csv" class="px-2.5 py-1.5 rounded-lg bg-surface-container-lowest border border-outline-variant/40 hover:bg-surface-container text-on-surface text-xs font-semibold transition-colors flex items-center gap-1 shadow-xs">
        <span class="material-symbols-outlined text-sm text-secondary">download</span>
        Export CSV
      </a>
      <a href="/download-report" download="SmartCredit_Loan_Approval_Project_Report.docx" class="px-2.5 py-1.5 rounded-lg bg-primary text-on-primary text-xs font-semibold hover:bg-primary-container transition-colors flex items-center gap-1 shadow-xs">
        <span class="material-symbols-outlined text-sm">print</span>
        Report (.docx)
      </a>
    </div>
  </div>

  <div class="overflow-x-auto max-h-72 overflow-y-auto rounded-lg border border-outline-variant/20">
    <table class="w-full text-left font-body-sm text-body-sm">
      <thead>
        <tr class="bg-surface-container-lowest text-outline font-label-sm uppercase border-b border-outline-variant/30 text-[11px]">
          <th class="py-2 px-2.5">App ID</th>
          <th class="py-2 px-2.5">Timestamp</th>
          <th class="py-2 px-2.5">Verdict</th>
          <th class="py-2 px-2.5">Facility</th>
          <th class="py-2 px-2.5">Score</th>
          <th class="py-2 px-2.5">SHA-256 Hash</th>
        </tr>
      </thead>
      <tbody id="audit-table-body" class="divide-y divide-outline-variant/20 text-on-surface">
        <tr class="border-b border-outline-variant/20 hover:bg-surface-container/50 transition-colors audit-row">
          <td class="py-2 px-2.5 font-mono text-xs font-bold text-secondary">#8849-FAC</td>
          <td class="py-2 px-2.5 text-xs text-on-surface">14:02:19 UTC</td>
          <td class="py-2 px-2.5 text-xs font-bold text-secondary">APPROVED</td>
          <td class="py-2 px-2.5 font-mono text-xs text-on-surface">$4,200,000</td>
          <td class="py-2 px-2.5 font-mono text-xs text-on-surface">91.4%</td>
          <td class="py-2 px-2.5 font-mono text-[10px] text-outline truncate max-w-[100px]" title="0x93f41bb8726acda094156ce99a14e9128">0x93f41bb8726a...</td>
        </tr>
        <tr class="border-b border-outline-variant/20 hover:bg-surface-container/50 transition-colors audit-row">
          <td class="py-2 px-2.5 font-mono text-xs font-bold text-secondary">#8848-FAC</td>
          <td class="py-2 px-2.5 text-xs text-on-surface">14:01:54 UTC</td>
          <td class="py-2 px-2.5 text-xs font-bold text-secondary">APPROVED</td>
          <td class="py-2 px-2.5 font-mono text-xs text-on-surface">$1,800,000</td>
          <td class="py-2 px-2.5 font-mono text-xs text-on-surface">84.2%</td>
          <td class="py-2 px-2.5 font-mono text-[10px] text-outline truncate max-w-[100px]" title="0x77b029f6da110294e776a3cc02832daef">0x77b029f6da11...</td>
        </tr>
        <tr class="border-b border-outline-variant/20 hover:bg-surface-container/50 transition-colors audit-row">
          <td class="py-2 px-2.5 font-mono text-xs font-bold text-error">#8847-FAC</td>
          <td class="py-2 px-2.5 text-xs text-on-surface">13:59:12 UTC</td>
          <td class="py-2 px-2.5 text-xs font-bold text-error">DECLINED</td>
          <td class="py-2 px-2.5 font-mono text-xs text-on-surface">$9,500,000</td>
          <td class="py-2 px-2.5 font-mono text-xs text-on-surface">58.0%</td>
          <td class="py-2 px-2.5 font-mono text-[10px] text-outline truncate max-w-[100px]" title="0xcc4910243be12da2857410ebc238fa091">0xcc4910243be1...</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="pt-space-xs flex items-center justify-between text-outline font-label-sm">
    <span>Merkle Tree Root: 0xFD89...991A</span>
    <span class="text-secondary">Immutable Block #1,940,211</span>
  </div>
</div>'''

g_main = re.sub(
    r'<!-- Real-Time Cryptographic Decision Ledger -->\s*<div class="bg-surface-container/90[^"]*">.*?Immutable Block #1,940,211</span>\s*</div>\s*</div>',
    audit_trail_enhanced,
    g_main,
    flags=re.DOTALL
)

# Connect Generate Examiner Package Button
g_main = re.sub(
    r'<button[^>]*>\s*<span class="material-symbols-outlined text-sm">print</span>\s*Generate Examiner Package\s*</button>',
    r'<a href="/download-report" download="SmartCredit_Loan_Approval_Project_Report.docx" class="px-space-md py-space-sm rounded-lg bg-primary text-on-primary font-semibold font-label-md shadow-md hover:brightness-110 transition-all flex items-center gap-space-xs"><span class="material-symbols-outlined text-sm">print</span>Generate Examiner Package (.docx)</a>',
    g_main
)

# -------------------------------------------------------------
# 3. ENHANCE PORTFOLIO SCREEN (View 1)
# -------------------------------------------------------------
cohort_selector_html = '''<div class="relative inline-block">
<select id="cohort-select" onchange="switchCohort(this.value)" class="px-3 py-1.5 bg-surface-container-low hover:bg-surface-container text-on-surface font-label-md text-label-md rounded border border-outline-variant/30 shadow-xs transition-colors cursor-pointer appearance-none pr-8">
  <option value="all" selected>Q3 2025 YTD (Consolidated) — All Commercial Portfolios</option>
  <option value="commercial">Commercial High-Ticket Facility (Income &gt; $5,500/mo)</option>
  <option value="retail">Retail &amp; Residential Mortgages (Income &le; $5,500/mo)</option>
  <option value="semiurban">Semiurban High-Growth Collateral Alpha</option>
</select>
<span class="material-symbols-outlined absolute right-2 top-1/2 -translate-y-1/2 text-outline text-sm pointer-events-none">arrow_drop_down</span>
</div>'''

p_main = re.sub(
    r'<div class="relative inline-block">\s*<button[^>]*id="cohort-btn"[^>]*>.*?</button>\s*</div>',
    cohort_selector_html,
    p_main,
    flags=re.DOTALL
)

# Add IDs to KPI Cards in View 1 for dynamic cohort updates
p_main = re.sub(
    r'(<div class="font-metric-xl[^"]*">)(800\s*<span[^>]*>Facilities</span>)(</div>)',
    r'\1<span id="kpi-total-apps">\2</span>\3',
    p_main,
    count=1
)

p_main = re.sub(
    r'(<div class="font-metric-xl[^"]*">)(82\.6%)(</div>)',
    r'\1<span id="kpi-approval-rate">\2</span>\3',
    p_main,
    count=1
)

p_main = re.sub(
    r'(<div class="font-metric-xl[^"]*">)(\$115\.3M\s*<span[^>]*>USD</span>)(</div>)',
    r'\1<span id="kpi-total-capital">\2</span>\3',
    p_main,
    count=1
)

p_main = re.sub(
    r'(<div class="font-metric-xl[^"]*text-error[^"]*">)(17\.4%)(</div>)',
    r'\1<span id="kpi-npa-risk">\2</span>\3',
    p_main,
    count=1
)

# -------------------------------------------------------------
# 4. INSTITUTIONAL LEFT SIDEBAR NAVIGATION
# -------------------------------------------------------------
sidebar_html = '''
<!-- Mobile Backdrop -->
<div id="sidebar-backdrop" onclick="toggleSidebar()" class="fixed inset-0 bg-black/40 z-40 hidden md:hidden backdrop-blur-xs transition-opacity"></div>

<!-- Institutional Left Sidebar Navigation Rail -->
<aside id="app-sidebar" class="fixed top-0 bottom-0 left-0 z-50 w-72 bg-surface-container-lowest border-r border-outline-variant/30 flex flex-col justify-between shadow-sm transition-transform duration-300 ease-in-out -translate-x-full md:translate-x-0">
  <div class="flex flex-col h-full">
    <!-- Brand / Platform Emblem -->
    <div class="p-5 border-b border-outline-variant/30 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <img alt="SmartCredit AI" class="h-9 w-9 object-contain" src="https://lh3.googleusercontent.com/aida/AEtjO1U62b818gOWPYrBvbMNkLG4X4viOjb0Q_wHUhWfF0p9oTAoYuQVf5rmvnysdwONOhWNKX3bRyT3g8bZY6rcIR3swiippHCg87m_ZhixOY7-6hg4VYm1ySLNTAhrUV1RELjo_Cl9eQAdDx0XxbfY1XQ_YC94jbe4xr8WLr_7GvuMTmOkzAESSqoPixKbOLbm9TXUNgg63jvJHKxM1ha5DifpnzAhJRNN2br5FLiw8WzivxukmIrpnrOVXB8"/>
        <div class="flex flex-col">
          <span class="font-bold text-on-surface tracking-tight leading-none text-lg">SmartCredit<span class="text-secondary">AI</span></span>
          <span class="text-[10px] text-outline tracking-wider font-semibold uppercase mt-1">Institutional Risk Platform</span>
        </div>
      </div>
      <button onclick="toggleSidebar()" class="md:hidden p-1.5 rounded-lg text-outline hover:bg-surface-container">
        <span class="material-symbols-outlined text-lg">close</span>
      </button>
    </div>

    <!-- Active System Pill -->
    <div class="px-5 py-2.5 bg-surface-container-low/50 border-b border-outline-variant/20 flex items-center justify-between">
      <div class="flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-on-tertiary-container animate-pulse"></span>
        <span class="text-[11px] font-bold text-on-surface tracking-wide uppercase">ENGINE v2.4 ONLINE</span>
      </div>
      <span class="text-[10px] font-semibold text-secondary px-2 py-0.5 rounded bg-secondary/10">OCC Validated</span>
    </div>

    <!-- Navigation Menu Items -->
    <div class="flex-1 overflow-y-auto px-3 py-4 space-y-6">
      <div>
        <p class="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-outline">Core Decision Intelligence</p>
        <nav class="space-y-1">
          <button onclick="switchTab('portfolio')" id="side-nav-portfolio" class="side-nav-item w-full flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium text-xs transition-all text-left bg-surface-container-high text-secondary font-semibold shadow-xs">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-secondary/15 text-secondary shrink-0">
              <span class="material-symbols-outlined text-lg">dashboard</span>
            </div>
            <div class="flex flex-col min-w-0">
              <span class="font-semibold truncate">Portfolio Intelligence</span>
              <span class="text-[10px] text-outline truncate">L1 KPIs &amp; Trajectories</span>
            </div>
          </button>

          <button onclick="switchTab('risk_drivers')" id="side-nav-risk_drivers" class="side-nav-item w-full flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium text-xs transition-all text-left text-on-surface-variant hover:bg-surface-container/60 hover:text-on-surface">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-surface-container-high text-on-surface-variant shrink-0">
              <span class="material-symbols-outlined text-lg">query_stats</span>
            </div>
            <div class="flex flex-col min-w-0">
              <span class="font-semibold truncate">Risk Drivers &amp; Demographics</span>
              <span class="text-[10px] text-outline truncate">Multivariate Risk Matrix</span>
            </div>
          </button>

          <button onclick="switchTab('underwriting')" id="side-nav-underwriting" class="side-nav-item w-full flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium text-xs transition-all text-left text-on-surface-variant hover:bg-surface-container/60 hover:text-on-surface">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-surface-container-high text-on-surface-variant shrink-0">
              <span class="material-symbols-outlined text-lg">bolt</span>
            </div>
            <div class="flex flex-col min-w-0">
              <span class="font-semibold truncate">Autonomous Underwriting</span>
              <span class="text-[10px] text-outline truncate">Real-Time Terminal &amp; HUD</span>
            </div>
          </button>

          <button onclick="switchTab('governance')" id="side-nav-governance" class="side-nav-item w-full flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium text-xs transition-all text-left text-on-surface-variant hover:bg-surface-container/60 hover:text-on-surface">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-surface-container-high text-on-surface-variant shrink-0">
              <span class="material-symbols-outlined text-lg">verified_user</span>
            </div>
            <div class="flex flex-col min-w-0">
              <span class="font-semibold truncate">Model Governance &amp; Audit</span>
              <span class="text-[10px] text-outline truncate">SR 11-7 &amp; SHA-256 Ledger</span>
            </div>
          </button>
        </nav>
      </div>

      <!-- System & Supervisory Actions -->
      <div>
        <p class="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-outline">Supervisory Tools &amp; Output</p>
        <div class="space-y-1">
          <a href="/download-report" download="SmartCredit_Loan_Approval_Project_Report.docx" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs text-on-surface hover:bg-surface-container/60 transition-colors">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center bg-primary/10 text-primary shrink-0">
              <span class="material-symbols-outlined text-base">description</span>
            </div>
            <div class="flex flex-col min-w-0">
              <span class="font-semibold truncate">Examiner Report (.docx)</span>
              <span class="text-[10px] text-outline truncate">657 KB Formal Submission</span>
            </div>
          </a>

          <a href="/api/export-audit-csv" download="smartcredit_audit_ledger.csv" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs text-on-surface hover:bg-surface-container/60 transition-colors">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center bg-secondary/10 text-secondary shrink-0">
              <span class="material-symbols-outlined text-base">download</span>
            </div>
            <div class="flex flex-col min-w-0">
              <span class="font-semibold truncate">Export Audit Ledger (CSV)</span>
              <span class="text-[10px] text-outline truncate">Cryptographic Proofs</span>
            </div>
          </a>

          <a href="/docs" target="_blank" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs text-on-surface hover:bg-surface-container/60 transition-colors">
            <div class="w-7 h-7 rounded-lg flex items-center justify-center bg-surface-container-high text-on-surface-variant shrink-0">
              <span class="material-symbols-outlined text-base">api</span>
            </div>
            <div class="flex flex-col min-w-0">
              <span class="font-semibold truncate">Swagger API Specs</span>
              <span class="text-[10px] text-outline truncate">Interactive REST Endpoints</span>
            </div>
          </a>
        </div>
      </div>

      <!-- Security Sentinel Card -->
      <div class="p-3 rounded-xl bg-surface-container-low border border-outline-variant/30 flex items-start gap-2.5">
        <span class="material-symbols-outlined text-secondary text-lg mt-0.5">shield_lock</span>
        <div class="flex flex-col">
          <span class="text-xs font-bold text-on-surface">Security Sentinel Active</span>
          <span class="text-[10px] text-outline leading-tight mt-0.5">Rate Limit: 40 req/min • OWASP ASVS • SHA-256 Audit</span>
        </div>
      </div>
    </div>

    <!-- Officer Profile & System Health Footer -->
    <div class="p-4 border-t border-outline-variant/30 bg-surface-container-lowest flex items-center justify-between">
      <div class="flex items-center gap-2.5">
        <img alt="Officer" class="w-9 h-9 rounded-full object-cover border border-outline-variant/50" src="https://lh3.googleusercontent.com/aida/AEtjO1VyS_oasWvIJkDjhdzJ653Md75M1JgLqsI6Db8FtCXNbcPAjvks47h5NHu_T_YQ4LQl-JShoqiuDcrh7SLblbTDxkpgVD2jyRTMcb6lQ8ZqmF66QDqySZHYYFEpX1jtB3mHdfODZIOvhczJJ_TBKx2jI4MZ8BYickyyaovQ-gfiKCpzmspt7El43-gOASbfpiGANnD4-RQI73xT4dZrlKjD1M7NzTeVVSG4JloEflwYtU98SGk-7x5ooqM"/>
        <div class="flex flex-col">
          <span class="text-xs font-bold text-on-surface leading-tight">Jay Patel</span>
          <span class="text-[10px] text-outline">Chief Risk Officer • Tier-1</span>
        </div>
      </div>
      <div class="flex items-center text-on-tertiary-container" title="All Microservices Online">
        <span class="material-symbols-outlined text-base">check_circle</span>
      </div>
    </div>
  </div>
</aside>
'''

# -------------------------------------------------------------
# 5. TOP UTILITY HEADER
# -------------------------------------------------------------
top_utility_bar = '''
<header class="sticky top-0 z-30 h-14 bg-surface-container-lowest border-b border-outline-variant/30 flex items-center justify-between px-4 sm:px-6 shadow-xs">
  <div class="flex items-center gap-3">
    <button onclick="toggleSidebar()" class="md:hidden p-1.5 rounded-lg text-on-surface hover:bg-surface-container transition-colors">
      <span class="material-symbols-outlined text-xl">menu</span>
    </button>
    <div class="flex items-center gap-2 text-xs text-outline">
      <span class="material-symbols-outlined text-sm text-outline">home</span>
      <span>/</span>
      <span>Institutional Risk</span>
      <span>/</span>
      <span id="breadcrumb-title" class="font-bold text-secondary">Portfolio Intelligence</span>
    </div>
  </div>

  <div class="flex items-center gap-3">
    <div class="hidden md:flex items-center gap-2 px-2.5 py-1 rounded bg-surface-container text-on-surface-variant text-xs font-semibold">
      <span class="material-symbols-outlined text-xs text-secondary">speed</span>
      <span>Inference: 12ms</span>
    </div>
    <a href="/download-report" download="SmartCredit_Loan_Approval_Project_Report.docx" class="px-3 py-1.5 rounded-lg bg-primary hover:bg-primary-container text-on-primary text-xs font-semibold transition-colors flex items-center gap-1.5 shadow-xs">
      <span class="material-symbols-outlined text-sm">description</span>
      <span class="hidden sm:inline">Download Examiner Package</span> (.docx)
    </a>
  </div>
</header>
'''

# -------------------------------------------------------------
# 6. MODALS & TOASTS
# -------------------------------------------------------------
modal_sanction_html = '''
<!-- Sanction Facility Note Modal -->
<div id="modal-sanction-sheet" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 hidden transition-opacity">
  <div class="max-w-2xl w-full bg-surface-container-lowest rounded-2xl shadow-2xl border border-outline-variant/40 overflow-hidden flex flex-col max-h-[90vh]">
    <div class="p-5 bg-gradient-to-r from-surface-container to-surface-container-high border-b border-outline-variant/30 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-secondary/15 flex items-center justify-center text-secondary">
          <span class="material-symbols-outlined text-2xl">verified</span>
        </div>
        <div class="flex flex-col">
          <span class="font-bold text-on-surface text-base">Official Facility Sanction Note</span>
          <span class="text-xs text-outline">Basel III Risk-Weighted Capital Directive Section 4b</span>
        </div>
      </div>
      <button onclick="closeSanctionModal()" class="p-1.5 rounded-lg hover:bg-surface-container-highest text-outline transition-colors">
        <span class="material-symbols-outlined text-xl">close</span>
      </button>
    </div>

    <div class="p-6 overflow-y-auto space-y-4 text-xs font-body-sm text-on-surface">
      <div class="p-3 rounded-lg bg-surface-container-low flex items-center justify-between border border-outline-variant/30">
        <div>
          <span class="text-outline block">Sanction Facility Reference</span>
          <span class="font-mono font-bold text-secondary text-sm">#SF-2025-9812-PRIME</span>
        </div>
        <div class="text-right">
          <span class="text-outline block">Issuance Date</span>
          <span class="font-semibold" id="modal-date">September 18, 2026</span>
        </div>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
        <div class="p-3 rounded-lg bg-surface-container-low">
          <span class="text-outline block text-[10px] uppercase font-bold">Approved Capital</span>
          <span id="modal-capital" class="font-bold text-sm text-on-surface font-mono">$140,000</span>
        </div>
        <div class="p-3 rounded-lg bg-surface-container-low">
          <span class="text-outline block text-[10px] uppercase font-bold">Prime APR Rate</span>
          <span class="font-bold text-sm text-secondary font-mono">8.25% Fixed</span>
        </div>
        <div class="p-3 rounded-lg bg-surface-container-low">
          <span class="text-outline block text-[10px] uppercase font-bold">Amortization</span>
          <span id="modal-term" class="font-bold text-sm text-on-surface font-mono">360 Mos (30Y)</span>
        </div>
        <div class="p-3 rounded-lg bg-surface-container-low">
          <span class="text-outline block text-[10px] uppercase font-bold">Collateral LTV</span>
          <span class="font-bold text-sm text-tertiary font-mono">71.4% LTV</span>
        </div>
      </div>

      <div class="space-y-2">
        <span class="font-bold uppercase tracking-wider text-[11px] text-outline block">Mandatory Pre-Disbursement Covenants</span>
        <ul class="space-y-1.5 list-disc pl-4 text-outline">
          <li>Execution of first-priority registered mortgage lien on target residential/commercial parcel.</li>
          <li>Comprehensive Title Search Certificate confirming free and unencumbered ownership rights.</li>
          <li>Escrow insurance policy active covering 100% of appraised collateral replacement valuation.</li>
          <li>Secondary income and employer KYC verification authenticated via standard bureau API.</li>
        </ul>
      </div>

      <div class="p-3 rounded-lg bg-secondary/5 border border-secondary/20 flex items-center gap-2 text-secondary">
        <span class="material-symbols-outlined text-lg shrink-0">gavel</span>
        <span>This automated facility note constitutes a conditional sanction recommendation compliant with OCC 2011-12.</span>
      </div>
    </div>

    <div class="p-4 border-t border-outline-variant/30 bg-surface-container-lowest flex items-center justify-end gap-2">
      <button onclick="closeSanctionModal()" type="button" class="px-4 py-2 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-semibold text-xs transition-colors">
        Close
      </button>
      <button onclick="window.print()" type="button" class="px-4 py-2 rounded-lg bg-secondary text-on-secondary font-semibold text-xs hover:bg-secondary-fixed transition-colors flex items-center gap-1.5 shadow-sm">
        <span class="material-symbols-outlined text-sm">print</span>
        Print / Save Official Note
      </button>
    </div>
  </div>
</div>
'''

toast_disbursal_html = '''
<!-- Disbursal Confirmation Toast -->
<div id="toast-disbursal" class="fixed bottom-6 right-6 z-50 bg-surface-container-lowest border-l-4 border-on-tertiary-container shadow-2xl rounded-xl p-4 flex items-center gap-3 transition-all duration-300 transform translate-y-20 opacity-0 pointer-events-none max-w-sm">
  <div class="w-10 h-10 rounded-xl bg-on-tertiary-container/15 flex items-center justify-center text-on-tertiary-container shrink-0">
    <span class="material-symbols-outlined text-2xl">task_alt</span>
  </div>
  <div class="flex flex-col min-w-0">
    <span class="text-xs font-bold text-on-surface">Application Routed to Disbursal Desk</span>
    <span class="text-[11px] text-outline leading-tight mt-0.5">Liquidity allocated from Central Tier-1 Pool. Priority wire order #DSB-9812 created.</span>
  </div>
</div>
'''

# -------------------------------------------------------------
# 7. CLIENT JAVASCRIPT CONTROLLER
# -------------------------------------------------------------
full_script_js = '''
<script>
// Tab Switching Controller
function switchTab(tabKey) {
  const views = {
    'portfolio': document.getElementById('view-portfolio'),
    'risk_drivers': document.getElementById('view-risk_drivers'),
    'underwriting': document.getElementById('view-underwriting'),
    'governance': document.getElementById('view-governance')
  };

  const titles = {
    'portfolio': 'Portfolio Intelligence',
    'risk_drivers': 'Risk Drivers & Demographics',
    'underwriting': 'Autonomous Underwriting Terminal',
    'governance': 'Model Governance & Audit Ledger'
  };

  Object.keys(views).forEach(key => {
    if (views[key]) {
      if (key === tabKey) {
        views[key].classList.remove('hidden');
      } else {
        views[key].classList.add('hidden');
      }
    }
  });

  // Update Left Sidebar Active State
  document.querySelectorAll('.side-nav-item').forEach(item => {
    item.className = "side-nav-item w-full flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium text-xs transition-all text-left text-on-surface-variant hover:bg-surface-container/60 hover:text-on-surface";
    const iconContainer = item.querySelector('div');
    if (iconContainer) iconContainer.className = "w-8 h-8 rounded-lg flex items-center justify-center bg-surface-container-high text-on-surface-variant shrink-0";
  });

  const activeSide = document.getElementById('side-nav-' + tabKey);
  if (activeSide) {
    activeSide.className = "side-nav-item w-full flex items-center gap-3 px-3 py-2.5 rounded-xl font-semibold text-xs transition-all text-left bg-surface-container-high text-secondary shadow-xs";
    const iconContainer = activeSide.querySelector('div');
    if (iconContainer) iconContainer.className = "w-8 h-8 rounded-lg flex items-center justify-center bg-secondary/15 text-secondary shrink-0";
  }

  // Update Breadcrumb Title
  const breadTitle = document.getElementById('breadcrumb-title');
  if (breadTitle && titles[tabKey]) {
    breadTitle.innerText = titles[tabKey];
  }

  // Auto close mobile drawer if open
  const sidebar = document.getElementById('app-sidebar');
  const backdrop = document.getElementById('sidebar-backdrop');
  if (sidebar && !sidebar.classList.contains('-translate-x-full') && window.innerWidth < 768) {
    toggleSidebar();
  }

  window.scrollTo({top: 0, behavior: 'smooth'});
}

// Mobile Sidebar Drawer Toggle
function toggleSidebar() {
  const sidebar = document.getElementById('app-sidebar');
  const backdrop = document.getElementById('sidebar-backdrop');
  if (sidebar) {
    const isClosed = sidebar.classList.contains('-translate-x-full');
    if (isClosed) {
      sidebar.classList.remove('-translate-x-full');
      if (backdrop) backdrop.classList.remove('hidden');
    } else {
      sidebar.classList.add('-translate-x-full');
      if (backdrop) backdrop.classList.add('hidden');
    }
  }
}

// Interactive Credit Score Synchronization
function syncCreditScore(val) {
  const numVal = Math.max(300, Math.min(850, parseInt(val) || 755));
  const slider = document.getElementById('inp-credit-score-slider');
  const box = document.getElementById('inp-credit-score');
  const badge = document.getElementById('credit-tier-badge');

  if (slider && slider.value != numVal) slider.value = numVal;
  if (box && box.value != numVal) box.value = numVal;

  if (badge) {
    if (numVal >= 750) {
      badge.className = "px-2 py-0.5 rounded text-xs font-bold uppercase bg-on-tertiary-container/15 text-on-tertiary-container";
      badge.innerText = `Optimal Tier (${numVal})`;
    } else if (numVal >= 650) {
      badge.className = "px-2 py-0.5 rounded text-xs font-bold uppercase bg-secondary/15 text-secondary";
      badge.innerText = `Prime Tier (${numVal})`;
    } else if (numVal >= 600) {
      badge.className = "px-2 py-0.5 rounded text-xs font-bold uppercase bg-amber-500/15 text-amber-600";
      badge.innerText = `Near-Prime (${numVal})`;
    } else {
      badge.className = "px-2 py-0.5 rounded text-xs font-bold uppercase bg-error/15 text-error";
      badge.innerText = `Subprime Risk (${numVal})`;
    }
  }
}

// Interactive AI Underwriting Form Submission
async function runUnderwriting() {
  const btn = document.getElementById('btn-run-underwriting');
  const originalHtml = btn ? btn.innerHTML : '';
  if (btn) {
    btn.innerHTML = '<span class="material-symbols-outlined animate-spin text-sm">progress_activity</span> Computing Deep Credit Decision...';
    btn.disabled = true;
  }

  const parseVal = (id, fallback) => {
    const el = document.getElementById(id);
    if (!el) return fallback;
    const v = el.value.replace(/[^0-9.]/g, '');
    return parseFloat(v) || fallback;
  };

  const primIncome = parseVal('inp-prim-income', 5500);
  const coIncome = parseVal('inp-co-income', 1500);
  const loanCapital = parseVal('inp-loan-capital', 140000);
  const term = parseVal('inp-term', 360);

  const geoEl = document.getElementById('inp-geo');
  let geo = 'Semiurban';
  if (geoEl) {
    const v = geoEl.value;
    if (v.includes('urban') && !v.includes('semi')) geo = 'Urban';
    else if (v.includes('rural')) geo = 'Rural';
    else geo = 'Semiurban';
  }

  const eduEl = document.getElementById('inp-edu');
  const edu = (eduEl && eduEl.value === 'grad') ? 'Graduate' : 'Not Graduate';

  // Read synchronized Credit Score
  const scoreBox = document.getElementById('inp-credit-score');
  const creditScore = scoreBox ? parseFloat(scoreBox.value) : 755;
  const creditHistory = creditScore >= 650 ? 1.0 : 0.0;

  const payload = {
    ApplicantIncome: primIncome,
    CoapplicantIncome: coIncome,
    LoanAmount: loanCapital / 1000.0,
    Loan_Amount_Term: term,
    Credit_History: creditHistory,
    Gender: "Male",
    Married: "Yes",
    Dependents: "0",
    Education: edu,
    Self_Employed: "No",
    Property_Area: geo
  };

  try {
    const res = await fetch('/api/underwrite', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `API returned status ${res.status}`);
    }

    const data = await res.json();
    renderUnderwritingResult(data, loanCapital, term);
  } catch (err) {
    console.error("Underwriting call failed:", err);
    alert("Underwriting evaluation error: " + err.message);
  } finally {
    if (btn) {
      btn.innerHTML = originalHtml;
      btn.disabled = false;
    }
  }
}

function renderUnderwritingResult(data, loanCapital, term) {
  const isApproved = data.verdict === 'APPROVED';

  // Update Decision HUD Header Badge
  const badgeEl = document.getElementById('hud-verdict-badge');
  if (badgeEl) {
    if (isApproved) {
      badgeEl.className = "px-space-xs py-0.5 rounded bg-secondary/20 text-secondary font-label-sm text-label-sm uppercase font-bold tracking-wide";
      badgeEl.innerText = "SANCTIONED (LOW RISK)";
    } else {
      badgeEl.className = "px-space-xs py-0.5 rounded bg-error-container text-on-error-container font-label-sm text-label-sm uppercase font-bold tracking-wide";
      badgeEl.innerText = "DECLINED (HIGH DEFAULT RISK)";
    }
  }

  // Update Title
  const titleEl = document.getElementById('hud-verdict-title');
  if (titleEl) {
    titleEl.innerText = isApproved ? "Facility Sanction Recommended" : "Application Decline Prescribed";
  }

  // Update Probability Score & Dial
  const probEl = document.getElementById('prob-val') || document.getElementById('hud-prob-value');
  if (probEl) {
    probEl.innerText = `${data.approval_probability.toFixed(1)}%`;
  }
  const dial = document.getElementById('approval-dial');
  if (dial) {
    const offset = Math.max(0, Math.min(427.25, (1 - (data.approval_probability / 100)) * 427.25));
    dial.style.strokeDashoffset = offset.toFixed(2);
    dial.className = isApproved 
      ? "text-secondary fill-none transition-all duration-1000 ease-out drop-shadow-[0_0_8px_rgba(78,222,163,0.6)]"
      : "text-error fill-none transition-all duration-1000 ease-out drop-shadow-[0_0_8px_rgba(255,84,73,0.6)]";
  }

  // Update Prescriptive Directive
  const directiveEl = document.getElementById('hud-prescriptive-directive');
  if (directiveEl && data.prescriptive_actions && data.prescriptive_actions.length > 0) {
    directiveEl.innerHTML = data.prescriptive_actions.map(a => `• ${a}`).join('<br>');
  }

  // Update Modal Values
  const modalCap = document.getElementById('modal-capital');
  if (modalCap) modalCap.innerText = `$${(loanCapital || 140000).toLocaleString()}`;
  const modalTerm = document.getElementById('modal-term');
  if (modalTerm) modalTerm.innerText = `${term || 360} Mos (${Math.round((term || 360)/12)}Y)`;

  // Prepend to Live Underwriting Queue
  const queueBody = document.getElementById('underwriting-queue-body');
  if (queueBody && data.audit_entry) {
    const e = data.audit_entry;
    const qRow = document.createElement('tr');
    qRow.className = "hover:bg-surface-container/60 transition-colors";
    qRow.innerHTML = `
      <td class="py-space-md px-space-md font-metric-md text-metric-md text-outline">${e.timestamp.split(' ')[1] || e.timestamp}</td>
      <td class="py-space-md px-space-md">
        <span class="font-metric-md text-metric-md text-primary font-semibold">#${e.app_id}</span>
        <span class="block font-body-sm text-body-sm text-outline">Autonomous Model Inference</span>
      </td>
      <td class="py-space-md px-space-md font-body-md text-body-md text-on-surface">Live KYC Profile</td>
      <td class="py-space-md px-space-md font-metric-md text-metric-md text-on-surface font-semibold">$${e.capital.toLocaleString()}</td>
      <td class="py-space-md px-space-md"><span class="font-metric-md text-metric-md ${isApproved ? 'text-secondary' : 'text-error'} font-semibold">${e.probability}%</span></td>
      <td class="py-space-md px-space-md font-metric-md text-metric-md text-outline">12ms</td>
      <td class="py-space-md px-space-md text-right"><span class="font-label-sm text-label-sm ${isApproved ? 'text-secondary' : 'text-error'} font-semibold uppercase">${e.verdict}</span></td>
    `;
    queueBody.insertBefore(qRow, queueBody.firstChild);
  }

  // Prepend to Governance Audit Ledger
  const auditBody = document.getElementById('audit-table-body');
  if (auditBody && data.audit_entry) {
    const e = data.audit_entry;
    const row = document.createElement('tr');
    row.className = "border-b border-outline-variant/30 hover:bg-surface-container/50 transition-colors audit-row";
    row.innerHTML = `
      <td class="py-2 px-3 font-mono text-xs font-bold text-secondary">${e.app_id}</td>
      <td class="py-2 px-3 text-xs text-on-surface">${e.timestamp}</td>
      <td class="py-2 px-3 text-xs font-bold ${isApproved ? 'text-secondary' : 'text-error'}">${e.verdict}</td>
      <td class="py-2 px-3 font-mono text-xs text-on-surface">$${e.capital.toLocaleString()}</td>
      <td class="py-2 px-3 font-mono text-xs text-on-surface">${e.probability}%</td>
      <td class="py-2 px-3 font-mono text-[10px] text-outline truncate max-w-[120px]" title="${e.hash}">${e.hash.substring(0, 16)}...</td>
    `;
    auditBody.insertBefore(row, auditBody.firstChild);
  }
}

// Load Benchmark Profile
function loadBenchmark() {
  const pInc = document.getElementById('inp-prim-income');
  if (pInc) pInc.value = '8,200';
  const cInc = document.getElementById('inp-co-income');
  if (cInc) cInc.value = '3,400';
  const cap = document.getElementById('inp-loan-capital');
  if (cap) cap.value = '160,000';
  const dti = document.getElementById('inp-dti');
  if (dti) dti.value = '24.1%';
  const term = document.getElementById('inp-term');
  if (term) term.value = '360';
  const geo = document.getElementById('inp-geo');
  if (geo) geo.value = 'semiurban';
  const edu = document.getElementById('inp-edu');
  if (edu) edu.value = 'grad';
  syncCreditScore(785);
  runUnderwriting();
}

// Reset Form to Baseline
function resetForm() {
  const pInc = document.getElementById('inp-prim-income');
  if (pInc) pInc.value = '5,500';
  const cInc = document.getElementById('inp-co-income');
  if (cInc) cInc.value = '1,500';
  const cap = document.getElementById('inp-loan-capital');
  if (cap) cap.value = '140,000';
  const dti = document.getElementById('inp-dti');
  if (dti) dti.value = '28.4%';
  const term = document.getElementById('inp-term');
  if (term) term.value = '360';
  const geo = document.getElementById('inp-geo');
  if (geo) geo.value = 'semiurban';
  const edu = document.getElementById('inp-edu');
  if (edu) edu.value = 'grad';
  syncCreditScore(755);
}

// Sanction Modal Handlers
function openSanctionModal() {
  const modal = document.getElementById('modal-sanction-sheet');
  if (modal) {
    modal.classList.remove('hidden');
  }
}

function closeSanctionModal() {
  const modal = document.getElementById('modal-sanction-sheet');
  if (modal) {
    modal.classList.add('hidden');
  }
}

// Disbursal Routing Toast
function triggerDisbursalToast() {
  const toast = document.getElementById('toast-disbursal');
  if (toast) {
    toast.classList.remove('translate-y-20', 'opacity-0', 'pointer-events-none');
    setTimeout(() => {
      toast.classList.add('translate-y-20', 'opacity-0', 'pointer-events-none');
    }, 3500);
  }
}

// Cohort Selector in Portfolio View
async function switchCohort(cohortVal) {
  try {
    const res = await fetch(`/api/portfolio-metrics?cohort=${cohortVal}`);
    if (!res.ok) return;
    const data = await res.json();
    const totalApps = document.getElementById('kpi-total-apps');
    if (totalApps) totalApps.innerText = `${data.total_applications} Facilities`;
    const appRate = document.getElementById('kpi-approval-rate');
    if (appRate) appRate.innerText = `${data.approval_rate_pct.toFixed(1)}%`;
    const totCap = document.getElementById('kpi-total-capital');
    if (totCap) totCap.innerText = `$${(data.total_capital_requested / 1000000).toFixed(1)}M USD`;
    const npaRisk = document.getElementById('kpi-npa-risk');
    if (npaRisk) npaRisk.innerText = `${data.portfolio_npa_risk_pct.toFixed(1)}%`;
  } catch (err) {
    console.error("Cohort update failed:", err);
  }
}

// Audit Table Filter
function filterAuditTable(query) {
  const q = (query || '').toLowerCase().trim();
  const rows = document.querySelectorAll('.audit-row');
  rows.forEach(row => {
    const text = row.innerText.toLowerCase();
    row.style.display = text.includes(q) ? '' : 'none';
  });
}

// Wire Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('btn-run-underwriting');
  if (btn) btn.addEventListener('click', runUnderwriting);
});
</script>
'''

# -------------------------------------------------------------
# 8. ASSEMBLE FULL HTML
# -------------------------------------------------------------
full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{p_head}
<title>SmartCredit AI | Institutional Credit Risk Platform</title>
</head>
<body class="bg-surface text-on-surface antialiased overflow-x-hidden">

{sidebar_html}

<!-- Main Application Content Area (Offset for Desktop Left Sidebar) -->
<div class="md:pl-72 flex-1 flex flex-col min-h-screen bg-surface">
  {top_utility_bar}

  <!-- VIEW 1: Portfolio Intelligence -->
  <main id="view-portfolio" class="w-full flex-1">
    {p_main}
  </main>

  <!-- VIEW 2: Risk Drivers & Demographics -->
  <main id="view-risk_drivers" class="w-full flex-1 hidden">
    {r_main}
  </main>

  <!-- VIEW 3: AI Underwriting Terminal -->
  <main id="view-underwriting" class="w-full flex-1 hidden">
    {u_main}
  </main>

  <!-- VIEW 4: Model Governance & Audit -->
  <main id="view-governance" class="w-full flex-1 hidden">
    {g_main}
  </main>

  {p_footer}
</div>

{modal_sanction_html}
{toast_disbursal_html}
{full_script_js}
</body>
</html>
'''

output_path = os.path.join(WORKSPACE_DIR, "templates", "index.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Successfully generated {output_path} ({os.path.getsize(output_path)} bytes)")
