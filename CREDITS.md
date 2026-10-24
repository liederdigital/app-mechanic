# Repository Credits & Build Provenance

This document records the build provenance of **App Mechanic** (`liederdigital/app-mechanic`): which AI builders and tools contributed to the repository, where they ran, what each phase contributed, and how human direction and review shaped the project.

Licensing and third-party terms are maintained separately in [LICENSE](LICENSE). Website build provenance is also recorded in the companion [`liederdigital/app-mechanic-website`](https://github.com/liederdigital/app-mechanic-website) repository.

---

## Snapshot

| Field | Value | Evidence |
| :--- | :--- | :--- |
| **Project** | App Mechanic (macOS application update scanner & local web dashboard) | Observed ([`app_mechanic.py`](app_mechanic.py), [`README.md`](README.md)) |
| **Human Owner** | Ron Stauffer (Lieder Digital, LLC) | Observed (Git history, [`LICENSE`](LICENSE), [`setup.py`](setup.py)) |
| **Primary Tool (Current & 2026-10-16 Sessions)** | Google Antigravity | Observed (2026-10-16 and 2026-10-23..2026-10-24 sessions) |
| **Primary Tool (Prior Phases)** | Unknown | Not recorded in repository history (`f4a873e`..`8a95680`) |
| **Known AI Contributors & Scope** | Google Antigravity (`v0.5.5` app launch fix, Mac App Store launch logic, notarized release packaging, `CREDITS.md` provenance log, Notchy-inspired landing page in [`docs/`](docs/) & [`liederdigital/app-mechanic-website`](https://github.com/liederdigital/app-mechanic-website), and `appmechanic.dev` domain integration); prior AI contributors (if any) on `v0.1.0`–`v0.5.4` are Unknown | Observed (2026-10-16 and 2026-10-23..2026-10-24 sessions) / Unknown (prior commits) |
| **Execution Surface (Current Session)** | Desktop application (Google Antigravity macOS app with integrated terminal and file tools) | Observed (2026-10-23..2026-10-24 session) |
| **Editor (Current Session)** | Google Antigravity IDE (`Antigravity.app`) | Observed (2026-10-23..2026-10-24 session) |
| **Known Model / Mode (Current Session)** | Gemini (Medium reasoning effort) | Observed (2026-10-23..2026-10-24 session) |
| **Project Era** | July 27, 2026 – October 24, 2026 (America/Denver, Mountain Time) | Observed (`git log`) |
| **Current Status** | Active — `v0.5.5` released; official website live at [appmechanic.dev](https://appmechanic.dev) | Observed (`5891abf`, `e7c9270`, tag `v0.5.5`) |

---

## Work Process & Evidence Limits

- **Human Direction, Testing & Release**: Ron Stauffer directs feature scope, UI/UX design references, and bug investigations, verifies application and website behavior on macOS and Cloudflare Pages, manages code-signing/notarization credentials and domain registration (`appmechanic.dev`), and authorizes releases.
- **Evidence Classification**:
  - **Observed**: Directly verified from active sessions or repository artifacts (`git log`, [`app_mechanic.py`](app_mechanic.py), [`setup.py`](setup.py), [`build.sh`](build.sh), [`NOTES.md`](NOTES.md), [`README.md`](README.md), [`docs/`](docs/)).
  - **Owner-Confirmed**: Explicitly confirmed by Ron Stauffer.
  - **Unknown**: Not established by repository evidence or owner confirmation and intentionally left unguessed.
- **Evidence Limits**:
  - Git commit authors (`Ron Stauffer <1081418+ronstauffer@users.noreply.github.com>` and `GitHub <noreply@github.com>` on `f4a873e`) reflect the Git committer identity rather than proving whether a human or an AI assistant authored the code.
  - Commits from `f4a873e` (2026-07-27) through `8a95680` (2026-09-21) do not contain AI attribution trailers or embedded session metadata, so the specific AI tools, models, reasoning modes, or editors used during those earlier phases remain **Unknown** unless confirmed by the owner.
  - The commits creating or updating this file can be inspected via `git log -- CREDITS.md`.

---

## Builder History (Newest First)

### 2026-10-23 to 2026-10-24 (America/Denver, MDT) — Marketing Website (`appmechanic.dev`), Interactive Simulator & Domain Integration
- **Builder / Tool**: Google Antigravity (**Observed**)
- **Execution Surface & Editor**: Google Antigravity desktop application on macOS (**Observed**)
- **Model / Mode**: Gemini (Medium effort) (**Observed**)
- **Human Involvement**: Ron Stauffer provided the `notchy.dev` design inspiration, selected the static HTML/CSS/JS architecture and Free + Pro licensing structure, provisioned the [`liederdigital/app-mechanic-website`](https://github.com/liederdigital/app-mechanic-website) repository and Cloudflare Pages project (`app-mechanic.pages.dev`), reviewed the live site and reported a CSS Grid overflow on the Setup cards with a full-page screenshot, and registered and connected the custom domain `appmechanic.dev` (**Observed** / **Owner-confirmed**).
- **Contributions & References**:
  - Created the Notchy-inspired glassmorphic landing page in [`docs/index.html`](docs/index.html), [`docs/styles.css`](docs/styles.css), and [`docs/script.js`](docs/script.js) featuring a floating pill navbar, interactive `localhost:8000` dashboard simulator (live filtering, search, Pro mode toggle, simulated CLI/App Store actions, and screenshot switcher), 5-source ecosystem bento grid, copyable setup snippets, Free vs. Pro pricing comparison, and FAQ accordion.
  - Published the website to [`liederdigital/app-mechanic-website`](https://github.com/liederdigital/app-mechanic-website) (`1438b91`), fixed CSS Grid column width expansion on the Setup cards (`06b2eb5`), and updated canonical/OpenGraph URLs to `https://appmechanic.dev/` (`f39f2b5`).
  - Updated [`README.md`](README.md) and the dashboard footer URL in [`app_mechanic.py`](app_mechanic.py) to point to `https://appmechanic.dev`, and committed [`CREDITS.md`](CREDITS.md) (`e7c9270`).

### 2026-10-16 (America/Denver, MDT) — `v0.5.5` Launch Fix, Release & Initial Provenance Log
- **Builder / Tool**: Google Antigravity (**Observed**)
- **Execution Surface & Editor**: Google Antigravity desktop application on macOS (**Observed**)
- **Model / Mode**: Gemini (Medium effort) (**Observed**)
- **Human Involvement**: Ron Stauffer reported the `Wispr Flow` launch bug, approved changing Mac App Store launch behavior for up-to-date apps, verified the fix locally in `/Applications/App Mechanic.app`, and authorized publishing the signed/notarized `v0.5.5` release and creating `CREDITS.md` (**Observed** / **Owner-confirmed**).
- **Contributions & References**:
  - Diagnosed LaunchServices name collision in [`app_mechanic.py`](app_mechanic.py) where `open -a "Wispr Flow"` resolved to a nested headless helper bundle (`Contents/Resources/swift-helper-app-dist/Wispr Flow.app`) instead of `/Applications/Wispr Flow.app`.
  - Updated `/api/launch` and `updateUI()` in [`app_mechanic.py`](app_mechanic.py), [`setup.py`](setup.py), and [`build.sh`](build.sh) (`5891abf`, tag `v0.5.5`) to launch apps by explicit `/Applications/<App>.app` bundle path, launch up-to-date Mac App Store apps directly instead of opening the App Store, ignore placeholder App Store ID `0` in `get_mas_installed()`, and skip dot-prefixed hidden bundles in `/Applications`.
  - Built, Developer ID code-signed, Apple-notarized, stapled, and published `AppMechanic-v0.5.5-Signed.zip` to GitHub Releases (`v0.5.5`), and drafted [`CREDITS.md`](CREDITS.md).

### 2026-09-18 to 2026-09-21 (America/Denver, MDT) — `v0.5.4` CLI Tool Scanning & Single-Instance Fixes
- **Builder / Tool**: Unknown
- **Execution Surface & Editor**: Unknown
- **Model / Mode**: Unknown
- **Human Involvement**: Committed under Ron Stauffer's Git identity (**Observed**); exact split between human code authorship and AI assistance is **Unknown**.
- **Contributions & References**:
  - Added global CLI package scanning (`npm`, `pipx`, and Homebrew formulae) with Terminal-based one-click upgrades (`/api/update_cli`), updated `macappstore://` URLs, and added testing bypass support in [`app_mechanic.py`](app_mechanic.py), [`setup.py`](setup.py), and [`build.sh`](build.sh) (`ea1d3a8`).
  - Fixed macOS Finder `"not open anymore"` launch error and AppleEvents browser-opening behavior by switching from `webbrowser.open` to `subprocess.call(['open', ...])` with a short exit delay on secondary launches (`8a95680`, tag `v0.5.4`).

### 2026-08-17 to 2026-09-06 (America/Denver, MDT) — `v0.3.0` to `v0.5.3` Install Detection, Ignore Rules, Packaging & Freemium Licensing
- **Builder / Tool**: Unknown
- **Execution Surface & Editor**: Unknown
- **Model / Mode**: Unknown
- **Human Involvement**: Committed under Ron Stauffer's Git identity (**Observed**); exact split between human code authorship and AI assistance is **Unknown**.
- **Contributions & References**:
  - Added install method detection (`Mac App Store`, `Homebrew`, `Manual / OS`), app launching (`/api/launch`), release ignoring (`/api/ignore`, `ignored_releases.json`), and initial [`build.sh`](build.sh) signing/notarization workflow (`068b595`).
  - Compacted table UI, added update-source tooltips, and added `xcrun stapler staple` + release zip creation in [`build.sh`](build.sh) (`68e0ce9`, `v0.3.0`; `25286e0`, `v0.4.0`).
  - Added freemium scan usage limits and Pro license activation flow, initially with LemonSqueezy (`87802dd`) and then migrated to Gumroad license verification (`438d671`, `2da08c8`, `v0.5.3`).

### 2026-07-27 to 2026-08-06 (America/Denver, MDT) — Initial Architecture, `py2app` Bundle & `v0.2.0` Scan History
- **Builder / Tool**: Unknown
- **Execution Surface & Editor**: GitHub web UI for initial repository bootstrap (`f4a873e`, **Observed**); Unknown for subsequent commits (`ea79d2d`..`a2f2a52`).
- **Model / Mode**: Unknown
- **Human Involvement**: Repository created and commits authored under Ron Stauffer's Git identity (**Observed**); exact split between human code authorship and AI assistance is **Unknown**.
- **Contributions & References**:
  - Initialized repository with [`LICENSE`](LICENSE) and [`README.md`](README.md) (`f4a873e`), followed by the core single-file [`app_mechanic.py`](app_mechanic.py) scanner and local glassmorphic HTML/JS dashboard (`ea79d2d`).
  - Added `py2app` bundle configuration ([`setup.py`](setup.py), [`AppMechanic.icns`](AppMechanic.icns), [`icon.jpg`](icon.jpg)), single-instance port check, and project documentation ([`NOTES.md`](NOTES.md), [`README.md`](README.md)) (`ae0ac28`).
  - Restricted HTTP server binding strictly to `127.0.0.1` (`e3aa447`).
  - Added persistent Scan History Log (`history.json`) and updated documentation (`1e0d183`, tag `v0.2.0`; `0abb027`; `a2f2a52`).
