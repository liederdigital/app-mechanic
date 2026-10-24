// Interactive Live Demo Dataset (mirrors real App Mechanic scan output)
let demoApps = [
    {
        name: "@anthropic-ai/claude-code",
        installed: "1.0.21",
        latest: "1.0.24",
        status: "outdated",
        source: "NPM Global",
        install_method: "NPM",
        type: "cli"
    },
    {
        name: "ripgrep",
        installed: "14.1.0",
        latest: "14.1.1",
        status: "outdated",
        source: "Homebrew Formula",
        install_method: "Homebrew CLI",
        type: "cli"
    },
    {
        name: "poetry",
        installed: "1.8.3",
        latest: "1.8.3",
        status: "up_to_date",
        source: "Pipx",
        install_method: "Pipx",
        type: "cli"
    },
    {
        name: "1Password",
        installed: "8.12.30",
        latest: "8.12.30",
        status: "up_to_date",
        source: "Homebrew Cask (1password)",
        install_method: "Homebrew",
        type: "gui"
    },
    {
        name: "App Mechanic",
        installed: "0.5.5",
        latest: "0.5.5",
        status: "up_to_date",
        source: "Native / OS",
        install_method: "Manual / OS",
        type: "gui"
    },
    {
        name: "Blender",
        installed: "4.2.0",
        latest: "4.3.1",
        status: "outdated",
        source: "Homebrew Cask (blender)",
        install_method: "Homebrew",
        type: "gui"
    },
    {
        name: "Cursor",
        installed: "0.45.11",
        latest: "0.45.11",
        status: "up_to_date",
        source: "Homebrew Cask (cursor)",
        install_method: "Manual / OS",
        type: "gui"
    },
    {
        name: "Final Cut Pro",
        installed: "10.8",
        latest: "10.8.1",
        status: "ignored",
        source: "Mac App Store",
        install_method: "Mac App Store",
        type: "gui"
    },
    {
        name: "Figma",
        installed: "124.5.2",
        latest: "124.5.2",
        status: "up_to_date",
        source: "Homebrew Cask (figma)",
        install_method: "Homebrew",
        type: "gui"
    },
    {
        name: "Obsidian",
        installed: "1.7.4",
        latest: "1.7.4",
        status: "up_to_date",
        source: "Homebrew Cask (obsidian)",
        install_method: "Homebrew",
        type: "gui"
    },
    {
        name: "Pixelmator Pro",
        installed: "3.6.8",
        latest: "3.6.8",
        status: "up_to_date",
        source: "Mac App Store",
        install_method: "Mac App Store",
        type: "gui"
    },
    {
        name: "Raycast",
        installed: "1.84.2",
        latest: "1.84.2",
        status: "up_to_date",
        source: "Homebrew Cask (raycast)",
        install_method: "Homebrew",
        type: "gui"
    }
];

let currentSimFilter = 'all';
let isDemoPro = true;
let toastTimeout = null;

function showSimToast(msg) {
    const toast = document.getElementById('simToast');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    if (toastTimeout) clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
    }, 3200);
}

function getMethodBadgeStyle(method) {
    if (method === 'Mac App Store') {
        return 'background: rgba(59, 130, 246, 0.12); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.25);';
    } else if (method === 'Homebrew' || method === 'Homebrew CLI') {
        return 'background: rgba(245, 158, 11, 0.12); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.25);';
    } else if (method === 'NPM') {
        return 'background: rgba(244, 63, 94, 0.12); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.25);';
    } else if (method === 'Pipx') {
        return 'background: rgba(234, 179, 8, 0.12); color: #eab308; border: 1px solid rgba(234, 179, 8, 0.25);';
    }
    return 'background: rgba(148, 163, 184, 0.12); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.22);';
}

function updateSimStats() {
    const total = demoApps.length;
    const outdated = demoApps.filter(a => a.status === 'outdated').length;
    const ignored = demoApps.filter(a => a.status === 'ignored').length;
    const upToDate = total - outdated - ignored;
    const healthy = upToDate + ignored;
    const pct = total > 0 ? Math.round((healthy / total) * 1000) / 10 : 0;

    document.getElementById('simPctVal').textContent = pct + '%';
    document.getElementById('simRingLabel').textContent = Math.round(pct) + '%';
    document.getElementById('simUpToDateVal').textContent = upToDate;
    document.getElementById('simOutdatedVal').textContent = outdated;
    document.getElementById('simIgnoredVal').textContent = ignored;

    document.getElementById('simFilterAll').textContent = `All Apps (${total})`;
    document.getElementById('simFilterOutdated').textContent = `Outdated (${outdated})`;
    document.getElementById('simFilterUp').textContent = `Up to Date (${upToDate})`;
    document.getElementById('simFilterIgnored').textContent = `Ignored (${ignored})`;

    const circle = document.getElementById('simRingCircle');
    if (circle) {
        const circumference = 213.6;
        const offset = circumference - (circumference * pct / 100);
        circle.style.strokeDashoffset = offset;
    }
}

function renderSimulatedTable() {
    updateSimStats();
    const tbody = document.getElementById('simTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';

    const query = (document.getElementById('simSearchInput')?.value || '').toLowerCase().trim();

    // Sort CLI first, then alphabetical (just like app_mechanic.py)
    const sorted = [...demoApps].sort((a, b) => {
        if (a.type === 'cli' && b.type !== 'cli') return -1;
        if (a.type !== 'cli' && b.type === 'cli') return 1;
        return a.name.localeCompare(b.name);
    });

    sorted.forEach(app => {
        const matchesFilter = (currentSimFilter === 'all') || (app.status === currentSimFilter);
        const matchesQuery = app.name.toLowerCase().includes(query) || app.install_method.toLowerCase().includes(query);
        if (!matchesFilter || !matchesQuery) return;

        let emoji = '🔴';
        let statusText = 'Update Available';
        if (app.status === 'up_to_date') {
            emoji = '🟢';
            statusText = 'Up to Date';
        } else if (app.status === 'ignored') {
            emoji = '🟡';
            statusText = 'Ignored';
        }

        const versionHtml = app.status === 'outdated'
            ? `<span style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-secondary);">${app.installed} ➔ <strong style="color: var(--accent-red);">${app.latest}</strong></span>`
            : `<span style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-secondary);">${app.installed} ➔ ${app.latest}</span>`;

        let actionsHtml = '';
        if (isDemoPro) {
            if (app.type !== 'cli') {
                actionsHtml += `<button class="sim-action-btn" onclick="simLaunchApp('${app.name}')">🚀 Launch</button>`;
            } else if (app.status === 'outdated') {
                actionsHtml += `<button class="sim-action-btn" style="border-color: var(--accent-blue); color: #60a5fa;" onclick="simUpdateCli('${app.name}', '${app.install_method}')">⬆️ Update</button>`;
            }
            if (app.status === 'outdated') {
                actionsHtml += `<button class="sim-action-btn" onclick="simIgnoreApp('${app.name}')">🚫 Ignore</button>`;
            } else if (app.status === 'ignored') {
                actionsHtml += `<button class="sim-action-btn" onclick="simUnignoreApp('${app.name}')">↩️ Unignore</button>`;
            }
        } else {
            actionsHtml = `<button class="sim-action-btn" onclick="simPromptPro()">🔒 Unlock Pro</button>`;
        }

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="font-weight: 600;">${emoji} <span style="margin-left: 0.35rem;">${app.name}</span></td>
            <td><span class="sim-status-badge sim-status-${app.status}">${statusText}</span></td>
            <td>${versionHtml}</td>
            <td><span class="sim-method-tag" style="${getMethodBadgeStyle(app.install_method)}" title="${app.source}">${app.install_method}</span></td>
            <td>${actionsHtml}</td>
        `;
        tbody.appendChild(tr);
    });
}

function setSimulatedFilter(filter) {
    currentSimFilter = filter;
    document.querySelectorAll('.sim-filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-filter') === filter);
    });
    renderSimulatedTable();
}

function toggleDemoProMode(enabled) {
    isDemoPro = enabled;
    renderSimulatedTable();
    showSimToast(enabled ? '✨ Pro Mode enabled: 1-click Launch, CLI Update & Ignore unlocked' : '🔒 Free Mode preview: Pro actions locked');
}

function simLaunchApp(name) {
    showSimToast(`🚀 Launching "${name}.app" via macOS open -a...`);
}

function simUpdateCli(name, method) {
    const app = demoApps.find(a => a.name === name);
    if (!app) return;
    let cmd = method === 'NPM' ? `npm install -g ${name}` : (method === 'Pipx' ? `pipx upgrade ${name}` : `brew upgrade ${name}`);
    showSimToast(`⬆️ Terminal executing: "${cmd}" → Updated to ${app.latest}!`);
    app.installed = app.latest;
    app.status = 'up_to_date';
    renderSimulatedTable();
}

function simIgnoreApp(name) {
    const app = demoApps.find(a => a.name === name);
    if (!app) return;
    app.status = 'ignored';
    renderSimulatedTable();
    showSimToast(`🚫 Ignored ${name} v${app.latest} — Health score updated!`);
}

function simUnignoreApp(name) {
    const app = demoApps.find(a => a.name === name);
    if (!app) return;
    app.status = 'outdated';
    renderSimulatedTable();
    showSimToast(`↩️ Unignored ${name} v${app.latest}`);
}

function simPromptPro() {
    showSimToast('🔒 Upgrade to App Mechanic Pro to unlock 1-click actions! (Toggle "Preview Pro Mode" top right)');
}

function triggerSimulatedScan() {
    const btn = document.getElementById('simBtnScan');
    const lbl = document.getElementById('simBtnScanLabel');
    if (!btn || btn.disabled) return;

    btn.classList.add('loading');
    btn.disabled = true;
    lbl.textContent = 'Scanning...';

    setTimeout(() => {
        btn.classList.remove('loading');
        btn.disabled = false;
        lbl.textContent = 'Scan Now';
        const now = new Date();
        document.getElementById('simScanTime').textContent = 'Just now (' + now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ')';
        showSimToast('⚡ Scan complete: Checked Homebrew Casks, mas, Formulae, NPM & Pipx');
    }, 900);
}

function switchShowcaseMode(mode) {
    const interactiveWin = document.getElementById('interactiveWindow');
    const screenshotWin = document.getElementById('screenshotWindow');
    const tabSim = document.getElementById('tabLiveSim');
    const tabShot = document.getElementById('tabScreenshot');

    if (mode === 'interactive') {
        interactiveWin.style.display = 'block';
        screenshotWin.style.display = 'none';
        tabSim.classList.add('active');
        tabShot.classList.remove('active');
    } else {
        interactiveWin.style.display = 'none';
        screenshotWin.style.display = 'block';
        tabSim.classList.remove('active');
        tabShot.classList.add('active');
    }
}

function copyCommand(elementId, btn) {
    const el = document.getElementById(elementId);
    if (!el) return;
    navigator.clipboard.writeText(el.textContent.trim()).then(() => {
        const span = btn.querySelector('span');
        const original = span.textContent;
        span.textContent = 'Copied ✓';
        btn.style.borderColor = '#10b981';
        btn.style.color = '#10b981';
        setTimeout(() => {
            span.textContent = original;
            btn.style.borderColor = '';
            btn.style.color = '';
        }, 1800);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    renderSimulatedTable();
});
