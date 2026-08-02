#!/usr/bin/env python3
import os
import sys
import json
import plistlib
import re
import subprocess
import urllib.request
import webbrowser
import socket
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import threading
import ssl

# Ensure Homebrew is in the PATH for bundled apps to find `mas`
if "/opt/homebrew/bin" not in os.environ.get("PATH", ""):
    os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin"
if "/usr/local/bin" not in os.environ.get("PATH", ""):
    os.environ["PATH"] += os.pathsep + "/usr/local/bin"

# Global cache of the last scan data
cached_scan_data = []
last_scan_time = ""

HISTORY_DIR = os.path.expanduser("~/Library/Application Support/AppMechanic")
HISTORY_FILE = os.path.join(HISTORY_DIR, "history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return []

def save_history(entry):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    history = load_history()
    history.append(entry)
    history = history[-50:]
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f)
    except Exception as e:
        print(f"Failed to save history: {e}")

def fetch_brew_casks():
    print("Fetching Homebrew Cask database...")
    url = "https://formulae.brew.sh/api/cask.json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    # Use unverified context to bypass SSL certificate issues inside py2app bundles
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Warning: Could not fetch Homebrew Cask database: {e}")
        return []

def get_mas_outdated():
    print("Checking Mac App Store updates...")
    try:
        res = subprocess.run(["mas", "outdated"], capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            outdated = {}
            for line in res.stdout.strip().split("\n"):
                if not line:
                    continue
                parts = re.split(r'\s+', line.strip(), maxsplit=2)
                if len(parts) >= 2:
                    app_id = parts[0]
                    match = re.match(r'^(.*?)\s+\(([\d\.]+)\s+->\s+([\d\.]+)\)$', parts[1] + (parts[2] if len(parts) > 2 else ""))
                    if match:
                        name, inst_v, late_v = match.groups()
                        outdated[name.lower()] = {
                            "installed": inst_v,
                            "latest": late_v,
                            "id": app_id
                        }
            return outdated
    except FileNotFoundError:
        print("Note: 'mas' command line tool not found. Skipping App Store CLI checks.")
    except Exception as e:
        print(f"Warning: Failed checking mas updates: {e}")
    return {}

def parse_version(v):
    m = re.search(r'^\d+(\.\d+)+', v.strip())
    if m:
        return [int(p) for p in m.group(0).split('.')]
    return []

def run_scan():
    global cached_scan_data, last_scan_time
    print("Scanning installed applications...")
    apps_dir = "/Applications"
    casks = fetch_brew_casks()
    mas_outdated = get_mas_outdated()
    
    app_to_latest = {}
    for cask in casks:
        version = cask.get("version", "")
        artifacts = cask.get("artifacts", [])
        for art in artifacts:
            if isinstance(art, dict) and "app" in art:
                app_list = art["app"]
                if isinstance(app_list, list):
                    for a in app_list:
                        if isinstance(a, str):
                            app_to_latest[a.lower()] = (cask["token"], version)
                elif isinstance(app_list, str):
                    app_to_latest[app_list.lower()] = (cask["token"], version)

    report_data = []
    
    if not os.path.exists(apps_dir):
        print(f"Error: {apps_dir} directory not found.")
        return []

    all_apps = sorted([f for f in os.listdir(apps_dir) if f.endswith(".app")])

    for item in all_apps:
        name_clean = item[:-4]
        plist_path = os.path.join(apps_dir, item, "Contents", "Info.plist")
        installed_ver = "Unknown"
        
        if os.path.exists(plist_path):
            try:
                with open(plist_path, 'rb') as f:
                    plist = plistlib.load(f)
                    installed_ver = str(plist.get("CFBundleShortVersionString") or plist.get("CFBundleVersion") or "Unknown")
            except Exception:
                pass

        if name_clean.lower() in mas_outdated:
            mas_info = mas_outdated[name_clean.lower()]
            report_data.append({
                "name": name_clean,
                "installed": mas_info["installed"],
                "latest": mas_info["latest"],
                "status": "outdated",
                "source": "Mac App Store"
            })
            continue

        cask_info = app_to_latest.get(item.lower())
        if cask_info:
            token, latest_raw = cask_info
            latest_ver = latest_raw.split(',')[0]
            
            if latest_ver == "latest":
                report_data.append({
                    "name": name_clean,
                    "installed": installed_ver,
                    "latest": "Latest",
                    "status": "up_to_date",
                    "source": "System/Web"
                })
                continue
                
            p_inst = parse_version(installed_ver)
            p_late = parse_version(latest_ver)
            
            if p_inst and p_late:
                # Pad to same length to fix format mismatches (e.g. Opera 133.0 vs 133.0.5932.60)
                max_len = max(len(p_inst), len(p_late))
                p_inst.extend([0] * (max_len - len(p_inst)))
                p_late.extend([0] * (max_len - len(p_late)))
                
                if p_late > p_inst:
                    # Ignore pre-releases from Homebrew (e.g. OBS beta/rc) to avoid bouncing updates
                    if any(tag in latest_raw.lower() for tag in ['beta', 'rc', 'alpha', 'pre', 'b']):
                        status = "up_to_date"
                    else:
                        status = "outdated"
                else:
                    status = "up_to_date"
            else:
                status = "up_to_date"

            report_data.append({
                "name": name_clean,
                "installed": installed_ver,
                "latest": latest_ver,
                "status": status,
                "source": f"Homebrew Cask ({token})"
            })
        else:
            report_data.append({
                "name": name_clean,
                "installed": installed_ver,
                "latest": installed_ver,
                "status": "up_to_date",
                "source": "Native / OS"
            })
            
    cached_scan_data = report_data
    last_scan_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    total = len(report_data)
    outdated = sum(1 for x in report_data if x["status"] == "outdated")
    up_to_date = total - outdated
    pct = round((up_to_date / total) * 100, 1) if total > 0 else 0
    
    save_history({
        "timestamp": last_scan_time,
        "percentage": pct,
        "up_to_date_count": up_to_date,
        "outdated_count": outdated
    })
    
    return report_data

def get_html_content():
    total = len(cached_scan_data)
    outdated = sum(1 for x in cached_scan_data if x["status"] == "outdated")
    up_to_date = total - outdated
    pct = round((up_to_date / total) * 100, 1) if total > 0 else 0
    stroke_offset = 226 - (226 * pct / 100)

    template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App Mechanic</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: rgba(20, 26, 46, 0.4);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-green: #10b981;
            --accent-green-glow: rgba(16, 185, 129, 0.15);
            --accent-red: #f43f5e;
            --accent-red-glow: rgba(244, 63, 94, 0.15);
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 2.5rem 1.5rem;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(59, 130, 246, 0.08) 0%, transparent 40%);
            background-attachment: fixed;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2.5rem;
            flex-wrap: wrap;
            gap: 1.5rem;
        }

        .title-area h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #fff 30%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.25rem;
        }

        .title-area p {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .scan-time {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            padding: 0.6rem 1.2rem;
            border-radius: 12px;
            font-size: 0.85rem;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            backdrop-filter: blur(10px);
        }

        /* Refresh Button */
        .refresh-btn {
            background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
            border: none;
            color: white;
            padding: 0.65rem 1.4rem;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
            transition: all 0.3s ease;
        }

        .refresh-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(59, 130, 246, 0.45);
        }

        .refresh-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .spinner {
            width: 16px;
            height: 16px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            display: none;
            animation: spin 0.8s linear infinite;
        }

        .refresh-btn.loading .spinner {
            display: block;
        }
        .refresh-btn.loading .btn-icon {
            display: none;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }

        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 1.8rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(16px);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s;
        }

        .stat-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255, 255, 255, 0.15);
        }

        .stat-info h3 {
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .stat-info .stat-value {
            font-family: 'Outfit', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
        }

        .stat-progress-ring {
            position: relative;
            width: 80px;
            height: 80px;
        }

        .stat-progress-ring svg {
            transform: rotate(-90deg);
        }

        .progress-ring-circle-bg {
            fill: none;
            stroke: rgba(255, 255, 255, 0.05);
            stroke-width: 6;
        }

        .progress-ring-circle {
            fill: none;
            stroke: var(--accent-green);
            stroke-width: 6;
            stroke-linecap: round;
            stroke-dasharray: 226;
            stroke-dashoffset: {{STROKE_OFFSET}};
            transition: stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .progress-percent-label {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 0.95rem;
        }

        .stat-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }

        .icon-up-to-date {
            background: var(--accent-green-glow);
            color: var(--accent-green);
        }

        .icon-outdated {
            background: var(--accent-red-glow);
            color: var(--accent-red);
        }

        /* History Section */
        .history-panel {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 2.5rem;
            backdrop-filter: blur(16px);
        }
        .history-header {
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
        }
        .history-list {
            max-height: 160px;
            overflow-y: auto;
            padding-right: 0.5rem;
        }
        .history-list::-webkit-scrollbar {
            width: 6px;
        }
        .history-list::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 4px;
        }
        .history-list::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }
        .history-item {
            display: flex;
            justify-content: space-between;
            padding: 0.75rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            font-size: 0.85rem;
            color: var(--text-secondary);
        }
        .history-item:last-child {
            border-bottom: none;
        }
        .history-pct {
            font-weight: 600;
            color: var(--text-primary);
        }
        .history-up {
            color: var(--accent-green);
        }

        /* Table & Controls Section */
        .dashboard-main {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 1.5rem;
            backdrop-filter: blur(16px);
        }

        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .search-wrapper {
            position: relative;
            flex: 1;
            max-width: 400px;
        }

        .search-input {
            width: 100%;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--card-border);
            padding: 0.75rem 1rem 0.75rem 2.5rem;
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 0.9rem;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .search-input:focus {
            border-color: var(--accent-blue);
            outline: none;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
        }

        .search-icon {
            position: absolute;
            left: 0.9rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-secondary);
            pointer-events: none;
        }

        .filter-buttons {
            display: flex;
            gap: 0.5rem;
        }

        .btn {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--card-border);
            color: var(--text-secondary);
            padding: 0.6rem 1.1rem;
            border-radius: 12px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
        }

        .btn:hover {
            background: rgba(255, 255, 255, 0.08);
            color: var(--text-primary);
        }

        .btn.active {
            background: var(--accent-blue);
            border-color: var(--accent-blue);
            color: white;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
        }

        /* App Table */
        .table-responsive {
            overflow-x: auto;
            border-radius: 14px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }

        th {
            background: rgba(15, 23, 42, 0.4);
            padding: 1rem 1.25rem;
            color: var(--text-secondary);
            font-weight: 600;
            border-bottom: 1px solid var(--card-border);
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }

        td {
            padding: 1rem 1.25rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            vertical-align: middle;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr {
            transition: background-color 0.15s;
        }

        tr:hover {
            background-color: rgba(255, 255, 255, 0.015);
        }

        .app-name-cell {
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.35rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        .status-up_to_date {
            background: var(--accent-green-glow);
            color: var(--accent-green);
        }

        .status-outdated {
            background: var(--accent-red-glow);
            color: var(--accent-red);
            animation: pulse-border 2s infinite;
        }

        .source-tag {
            background: rgba(255, 255, 255, 0.05);
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            font-size: 0.75rem;
            color: var(--text-secondary);
            font-family: monospace;
        }

        @keyframes pulse-border {
            0%, 100% {
                box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.2);
            }
            50% {
                box-shadow: 0 0 0 4px rgba(244, 63, 94, 0);
            }
        }

        @media (max-width: 768px) {
            body {
                padding: 1.5rem 1rem;
            }
            header {
                flex-direction: column;
                align-items: flex-start;
            }
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            .search-wrapper {
                max-width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="title-area">
                <h1>App Mechanic</h1>
                <p>Track updates and versions of all your applications</p>
            </div>
            <div class="header-actions">
                <div class="scan-time">
                    <span>⚡</span> Last Scanned: <span id="lblScanTime">Loading...</span>
                </div>
                <button id="btnRefresh" class="refresh-btn" onclick="triggerRefresh()">
                    <span class="btn-icon">🔄</span>
                    <span class="spinner"></span>
                    <span>Scan Now</span>
                </button>
                <button id="btnQuit" class="btn" style="background: rgba(244, 63, 94, 0.1); border-color: rgba(244, 63, 94, 0.3); color: var(--accent-red); display: flex; align-items: center; gap: 0.5rem;" onclick="quitServer()">
                    <span>🛑 Quit</span>
                </button>
            </div>
        </header>

        <!-- Stats Section -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-info">
                    <h3>Overall Status</h3>
                    <div class="stat-value" id="lblOverallPct">{{PCT}}%</div>
                </div>
                <div class="stat-progress-ring">
                    <svg width="80" height="80">
                        <circle class="progress-ring-circle-bg" cx="40" cy="40" r="36" />
                        <circle class="progress-ring-circle" id="progressRingCircle" cx="40" cy="40" r="36" />
                    </svg>
                    <div class="progress-percent-label" id="lblProgressRingText">{{PCT}}%</div>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-info">
                    <h3>Up To Date</h3>
                    <div class="stat-value" id="lblUpToDateCount" style="color: var(--accent-green);">{{UP_TO_DATE}}</div>
                </div>
                <div class="stat-icon icon-up-to-date">
                    <span>🟢</span>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-info">
                    <h3>Updates Pending</h3>
                    <div class="stat-value" id="lblOutdatedCount" style="color: var(--accent-red);">{{OUTDATED}}</div>
                </div>
                <div class="stat-icon icon-outdated">
                    <span>🔴</span>
                </div>
            </div>
        </div>

        <!-- History Section -->
        <div class="history-panel">
            <h3 class="history-header">Recent Scan History</h3>
            <div class="history-list" id="historyList">
                <!-- Populated by JS -->
            </div>
        </div>

        <!-- Main Section -->
        <div class="dashboard-main">
            <div class="controls">
                <div class="search-wrapper">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="searchInput" class="search-input" placeholder="Search applications...">
                </div>
                <div class="filter-buttons">
                    <button class="btn active" id="btnAll" onclick="filterApps('all')">All Apps</button>
                    <button class="btn" id="btnOutdated" onclick="filterApps('outdated')">Outdated</button>
                    <button class="btn" id="btnUpToDate" onclick="filterApps('up_to_date')">Up to Date</button>
                </div>
            </div>

            <div class="table-responsive">
                <table id="appsTable">
                    <thead>
                        <tr>
                            <th>Application</th>
                            <th>Status</th>
                            <th>Installed Version</th>
                            <th>Latest Version</th>
                            <th>Source</th>
                        </tr>
                    </thead>
                    <tbody id="appsTableBody">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        let currentFilter = 'all';
        let scanData = [];
        let scanHistory = {{HISTORY_JSON}};

        function updateHistoryUI(historyData) {
            const container = document.getElementById('historyList');
            container.innerHTML = '';
            if (!historyData || historyData.length === 0) {
                container.innerHTML = '<div style="padding: 1rem; text-align: center; color: var(--text-secondary);">No history available yet. Run a scan to build history.</div>';
                return;
            }
            
            // Show latest first
            [...historyData].reverse().forEach(entry => {
                const item = document.createElement('div');
                item.className = 'history-item';
                item.innerHTML = `
                    <span>${entry.timestamp}</span>
                    <span>
                        <span class="history-pct">${entry.percentage}%</span> up to date 
                        (<span class="history-up">${entry.up_to_date_count}</span> updated, 
                        <span style="color: var(--accent-red);">${entry.outdated_count}</span> pending)
                    </span>
                `;
                container.appendChild(item);
            });
        }

        function updateUI(data, scanTime, historyData) {
            scanData = data;
            if (historyData) {
                scanHistory = historyData;
            }
            updateHistoryUI(scanHistory);
            
            document.getElementById('lblScanTime').textContent = scanTime;

            const total = data.length;
            const outdated = data.filter(x => x.status === 'outdated').length;
            const upToDate = total - outdated;
            const pct = total > 0 ? Math.round((upToDate / total) * 1000) / 10 : 0;

            // Update stats labels
            document.getElementById('lblOverallPct').textContent = pct + '%';
            document.getElementById('lblProgressRingText').textContent = Math.round(pct) + '%';
            document.getElementById('lblUpToDateCount').textContent = upToDate;
            document.getElementById('lblOutdatedCount').textContent = outdated;

            // Update filter button labels
            document.getElementById('btnAll').textContent = `All Apps (${total})`;
            document.getElementById('btnOutdated').textContent = `Outdated (${outdated})`;
            document.getElementById('btnUpToDate').textContent = `Up to Date (${upToDate})`;

            // Update progress ring stroke dashoffset
            const circle = document.getElementById('progressRingCircle');
            const offset = 226 - (226 * pct / 100);
            circle.style.strokeDashoffset = offset;

            // Render table
            const tbody = document.getElementById('appsTableBody');
            tbody.innerHTML = '';
            
            data.forEach(row => {
                const statusLabel = row.status === 'up_to_date' ? 'Up to Date' : 'Update Available';
                const statusEmoji = row.status === 'up_to_date' ? '🟢' : '🔴';
                
                const tr = document.createElement('tr');
                tr.className = 'app-row';
                tr.setAttribute('data-status', row.status);
                tr.innerHTML = `
                    <td>
                        <div class="app-name-cell">
                            <span>${statusEmoji}</span>
                            ${row.name}
                        </div>
                    </td>
                    <td>
                        <span class="status-badge status-${row.status}">
                            ${statusLabel}
                        </span>
                    </td>
                    <td>${row.installed}</td>
                    <td>${row.latest}</td>
                    <td><span class="source-tag">${row.source}</span></td>
                `;
                tbody.appendChild(tr);
            });

            filterRows();
        }

        function triggerRefresh() {
            const btn = document.getElementById('btnRefresh');
            btn.classList.add('loading');
            btn.disabled = true;

            fetch('/api/scan')
                .then(res => res.json())
                .then(res => {
                    updateUI(res.data, res.scan_time, res.history);
                })
                .catch(err => {
                    console.error('Scan failed:', err);
                    alert('Scan failed. Please check the terminal output.');
                })
                .finally(() => {
                    btn.classList.remove('loading');
                    btn.disabled = false;
                });
        }

        // Real-time Search functionality
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', () => filterRows());

        function filterApps(filterType) {
            currentFilter = filterType;
            
            document.querySelectorAll('.filter-buttons .btn').forEach(btn => {
                btn.classList.remove('active');
            });
            if (filterType === 'all') document.getElementById('btnAll').classList.add('active');
            if (filterType === 'outdated') document.getElementById('btnOutdated').classList.add('active');
            if (filterType === 'up_to_date') document.getElementById('btnUpToDate').classList.add('active');

            filterRows();
        }

        function filterRows() {
            const searchQuery = searchInput.value.toLowerCase().trim();
            const rows = document.querySelectorAll('.app-row');

            rows.forEach(row => {
                const appName = row.querySelector('.app-name-cell').textContent.toLowerCase();
                const appStatus = row.getAttribute('data-status');
                
                const matchesSearch = appName.includes(searchQuery);
                const matchesFilter = (currentFilter === 'all') || (appStatus === currentFilter);

                if (matchesSearch && matchesFilter) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }

        function quitServer() {
            if (confirm("Are you sure you want to quit the App Mechanic server?")) {
                fetch('/api/quit').then(() => {
                    document.body.innerHTML = '<div style="display:flex; flex-direction:column; height:100vh; align-items:center; justify-content:center; text-align:center;"><h2>App Mechanic Server Stopped.</h2><p style="color: var(--text-secondary); margin-top: 1rem;">You can safely close this tab or window.</p></div>';
                }).catch(err => {
                    console.error('Failed to quit:', err);
                });
            }
        }

        // Initial load of cached data
        fetch('/api/data')
            .then(res => res.json())
            .then(res => {
                updateUI(res.data, res.scan_time, res.history);
            });
    </script>
</body>
</html>
"""
    # Replace template tokens
    template = template.replace("{{PCT}}", str(pct))
    template = template.replace("{{OUTDATED}}", str(outdated))
    template = template.replace("{{UP_TO_DATE}}", str(up_to_date))
    template = template.replace("{{TOTAL}}", str(total))
    template = template.replace("{{TIME_STR}}", str(last_scan_time))
    template = template.replace("{{STROKE_OFFSET}}", str(stroke_offset))
    template = template.replace("{{HISTORY_JSON}}", json.dumps(load_history()))
    return template

class DashboardHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        global cached_scan_data, last_scan_time
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(get_html_content().encode('utf-8'))
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "data": cached_scan_data,
                "scan_time": last_scan_time,
                "history": load_history()
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == '/api/scan':
            new_data = run_scan()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "data": new_data,
                "scan_time": last_scan_time,
                "history": load_history()
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == '/api/quit':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "shutting down"}).encode('utf-8'))
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        else:
            self.send_response(404)
            self.end_headers()

def start_server(port=8000):
    handler = DashboardHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
            print(f"==========================================")
            print(f"  Dashboard Server Running on port {port}")
            print(f"  Access UI at http://localhost:{port}")
            print(f"  Press Ctrl+C in this Terminal to exit.")
            print(f"==========================================")
            
            webbrowser.open(f"http://localhost:{port}")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:
            print(f"Port {port} is already in use. Exiting.")
            sys.exit(0)
        else:
            raise e

def check_single_instance(port=8000):
    """If another instance is already running on the port, open the browser to it and exit."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # connect_ex returns 0 if connection succeeds (meaning port is actively in use by our app)
        if s.connect_ex(('localhost', port)) == 0:
            print(f"App Mechanic is already running on port {port}. Opening existing instance...")
            webbrowser.open(f"http://localhost:{port}")
            sys.exit(0)

def main():
    print("==========================================")
    print("            App Mechanic                  ")
    print("==========================================")
    
    check_single_instance(port=8000)
    
    run_scan()
    start_server(port=8000)

if __name__ == "__main__":
    main()
