# Repository Credits & Build Provenance

This document records the build provenance of **App Mechanic** (`liederdigital/app-mechanic`): which AI builders and tools contributed to the repository, where they ran, what each phase contributed, and how human direction and review shaped the project.

Licensing and third-party terms are maintained separately in [LICENSE](LICENSE). Website build provenance is also recorded in the companion [`liederdigital/appmechanic.dev`](https://github.com/liederdigital/appmechanic.dev) repository.

---

## Snapshot

| Field | Value | Evidence |
| :--- | :--- | :--- |
| **Project** | App Mechanic (macOS application update scanner & local web dashboard) | Observed ([`app_mechanic.py`](app_mechanic.py), [`README.md`](README.md)) |
| **Human Owner** | Ron Stauffer (Lieder Digital, LLC) | Observed (Git history, [`LICENSE`](LICENSE), [`setup.py`](setup.py)) |
| **Primary Tool** | Google Antigravity | Observed across all 7 project conversation transcripts (`2026-07-28` through `2026-10-24`) |
| **Known AI Contributors & Scope** | Google Antigravity (`v0.1.0`–`v0.5.5` application architecture, Homebrew Cask/Formula + Mac App Store `mas` + `npm` + `pipx` scanning, `py2app` bundling, Apple code-signing & notarization scripts, Gumroad Pro licensing, `CREDITS.md` provenance log, and the [appmechanic.dev](https://appmechanic.dev) marketing website & interactive simulator) | Observed (Antigravity workspace transcripts & `git log`) |
| **Execution Surface** | Desktop application (Google Antigravity macOS app with integrated terminal and file tools) | Observed (Antigravity session logs) |
| **Editor** | Google Antigravity IDE (`Antigravity.app`) | Observed (Antigravity session logs) |
| **Known Models / Modes** | • **Aug 17, 2026 – Sep 21, 2026**: Gemini 3.1 Pro (High)<br>• **Oct 16, 2026 – Oct 24, 2026**: Gemini (Medium effort)<br>• **Jul 28, 2026 – Aug 11, 2026**: Unknown exact model string (Antigravity default prior to explicit model-selection logging) | Observed (`USER_SETTINGS_CHANGE` records in Antigravity transcripts) |
| **Project Era** | July 27, 2026 – October 24, 2026 (America/Denver, Mountain Time) | Observed (`git log` & session timestamps) |
| **Current Status** | Active — `v0.5.5` released; official website live at [appmechanic.dev](https://appmechanic.dev) | Observed (`5891abf`, `39d3ac0`, tag `v0.5.5`) |

---

## Work Process & Evidence Limits

- **Human Direction, Testing & Release**: Across all development sessions, Ron Stauffer directed product requirements, UI/UX refinements, and bug investigations, tested builds locally on macOS (including MacBook Air cross-machine testing), managed Apple Developer ID code-signing/notarization credentials, Gumroad licensing, and Cloudflare Pages / `appmechanic.dev` domain configuration, and authorized releases.
- **Evidence Classification**:
  - **Observed**: Directly verified from the 7 Google Antigravity project transcripts stored in the local workspace history and repository artifacts (`git log`, [`app_mechanic.py`](app_mechanic.py), [`setup.py`](setup.py), [`build.sh`](build.sh), [`NOTES.md`](NOTES.md), [`README.md`](README.md), [`docs/`](docs/)).
  - **Owner-Confirmed**: Explicitly confirmed by Ron Stauffer (including pointing to the complete local Antigravity conversation history for `macOS: App Mechanic`).
  - **Unknown**: Not recorded in session logs or repository metadata and intentionally left unguessed.
- **Evidence Limits**:
  - All 7 conversations in the `macOS: App Mechanic` project folder were inspected via local Antigravity transcripts.
  - The earliest Antigravity transcript (`2026-07-28` to `2026-08-11`, *App Mechanic Project Overview*) predates explicit `Model Selection` setting-change markers in the transcript log, so the exact underlying model version for that first session remains **Unknown**.
  - Commit `f4a873e` (`Initial commit` on `2026-07-27`) was created on GitHub (`Commit: GitHub <noreply@github.com>`), and commit `ea79d2d` (`2026-07-27`) was committed immediately before the `2026-07-28` Antigravity transcript began.
  - The commits creating or updating this file can be inspected via `git log -- CREDITS.md`.

---

## Builder History (Newest First)

### 2026-10-23 to 2026-10-24 (America/Denver, MDT) — Marketing Website (`appmechanic.dev`), Interactive Simulator & Provenance Update
- **Session**: *Creating A Website Like Notchy* (**Observed**)
- **Builder / Tool**: Google Antigravity (**Observed**)
- **Execution Surface & Editor**: Google Antigravity desktop application on macOS (**Observed**)
- **Model / Mode**: Gemini (Medium effort) (**Observed**)
- **Human Involvement**: Ron Stauffer provided the `notchy.dev` design reference, selected the static HTML/CSS/JS architecture and Free + Pro licensing structure, set up the [`liederdigital/appmechanic.dev`](https://github.com/liederdigital/appmechanic.dev) repository and Cloudflare Pages project, identified a CSS Grid column overflow via screenshot review, registered and connected `appmechanic.dev`, and pointed out the full local Antigravity conversation history to resolve earlier `CREDITS.md` unknowns (**Observed** / **Owner-confirmed**).
- **Contributions & References**:
  - Built the Notchy-inspired glassmorphic landing page in [`docs/index.html`](docs/index.html), [`docs/styles.css`](docs/styles.css), and [`docs/script.js`](docs/script.js) featuring a floating pill navbar, interactive `localhost:8000` dashboard simulator, 5-ecosystem bento grid, copyable setup snippets, Free vs. Pro pricing cards, and FAQ accordion.
  - Deployed to [`liederdigital/appmechanic.dev`](https://github.com/liederdigital/appmechanic.dev) (`1438b91`), fixed CSS Grid column overflow (`06b2eb5`), and updated metadata and [`app_mechanic.py`](app_mechanic.py) / [`README.md`](README.md) links to `https://appmechanic.dev` (`f39f2b5`, `e7c9270`, `39d3ac0`).

### 2026-10-16 (America/Denver, MDT) — `v0.5.5` Launch Fix, Release & Initial Provenance Log
- **Session**: *Troubleshooting WhisperFlow App Launch* (**Observed**)
- **Builder / Tool**: Google Antigravity (**Observed**)
- **Execution Surface & Editor**: Google Antigravity desktop application on macOS (**Observed**)
- **Model / Mode**: Gemini (Medium effort) (**Observed**)
- **Human Involvement**: Ron Stauffer reported the `Wispr Flow` launch bug, approved changing Mac App Store launch behavior for up-to-date apps, verified the fix locally in `/Applications/App Mechanic.app`, and authorized publishing the signed/notarized `v0.5.5` release and creating `CREDITS.md` (**Observed** / **Owner-confirmed**).
- **Contributions & References**:
  - Diagnosed LaunchServices name collision in [`app_mechanic.py`](app_mechanic.py) where `open -a "Wispr Flow"` resolved to a nested headless helper bundle (`Contents/Resources/swift-helper-app-dist/Wispr Flow.app`) instead of `/Applications/Wispr Flow.app`.
  - Updated `/api/launch` and `updateUI()` in [`app_mechanic.py`](app_mechanic.py), [`setup.py`](setup.py), and [`build.sh`](build.sh) (`5891abf`, tag `v0.5.5`) to launch apps by explicit `/Applications/<App>.app` bundle path, launch up-to-date Mac App Store apps directly, ignore placeholder App Store ID `0` in `get_mas_installed()`, and skip dot-prefixed hidden bundles in `/Applications`.
  - Built, Developer ID code-signed, Apple-notarized, stapled, and published `AppMechanic-v0.5.5-Signed.zip` to GitHub Releases (`v0.5.5`).

### 2026-09-21 (America/Denver, MDT) — Finder Launch Delay & AppleEvents Browser Fix
- **Session**: *Understanding MacBook Error Message* (**Observed**)
- **Builder / Tool**: Google Antigravity (**Observed**)
- **Execution Surface & Editor**: Google Antigravity desktop application on macOS (**Observed**)
- **Model / Mode**: Gemini 3.1 Pro (High) (**Observed**)
- **Human Involvement**: Ron Stauffer tested the app on a MacBook Air, shared screenshots of the macOS Finder `"The application 'App Mechanic' is not open anymore"` and AppleEvents permission errors, and verified the fix (**Observed**).
- **Contributions & References**:
  - Replaced `webbrowser.open` with `subprocess.call(['open', f'http://localhost:{port}'])` and added a `1.5s` exit delay in `check_single_instance()` in [`app_mechanic.py`](app_mechanic.py) (`8a95680`, tag `v0.5.4`).

### 2026-09-18 (America/Denver, MDT) — `v0.5.4` CLI Tool Scanning (`npm`, `pipx`, `brew`) & Mac App Store Deep Links
- **Session**: *Mac App Store Link Redirection* (**Observed**)
- **Builder / Tool**: Google Antigravity (**Observed**)
- **Execution Surface & Editor**: Google Antigravity desktop application on macOS (**Observed**)
- **Model / Mode**: Gemini 3.1 Pro (High) (**Observed**)
- **Human Involvement**: Ron Stauffer proposed redirecting outdated Mac App Store apps to `macappstore://` so users can click Update directly, requested expanding App Mechanic to scan global CLI tools (`npm`, `pipx`, Homebrew Formulae) with one-click Terminal updates, and tested the new dashboard layout (**Observed**).
- **Contributions & References**:
  - Added `get_npm_tools()`, `get_pipx_tools()`, `get_brew_formulae()`, and `/api/update_cli` AppleScript Terminal execution, updated `macappstore://apps.apple.com/app/id...` links, and added `BETA-TEST-2026` license bypass in [`app_mechanic.py`](app_mechanic.py), [`setup.py`](setup.py), and [`build.sh`](build.sh) (`ea1d3a8`).

### 2026-08-22 to 2026-09-06 (America/Denver, MDT) — `v0.5.0` to `v0.5.3` Freemium Scan Limits & Gumroad Licensing Migration
- **Session**: *Local Lite Version Upgrade Issues* (**Observed**)
- **Builder / Tool**: Google Antigravity (**Observed**)
- **Execution Surface & Editor**: Google Antigravity desktop application on macOS (**Observed**)
- **Model / Mode**: Gemini 3.1 Pro (High) (**Observed**)
- **Human Involvement**: Ron Stauffer reported local trial/lite state issues and directed migrating license verification from LemonSqueezy to Gumroad, tested license key activation, and requested UI header adjustments (**Observed**).
- **Contributions & References**:
  - Migrated `/api/activate` from LemonSqueezy to Gumroad's `/v2/licenses/verify` API, refined the Unlock Pro modal, and updated header layout in [`app_mechanic.py`](app_mechanic.py) (`438d671`, `2da08c8`, tag `v0.5.3`).

### 2026-08-17 to 2026-08-19 (America/Denver, MDT) — `v0.3.0` to `v0.5.0` Auto-Updater Filtering, Launch/Ignore Actions, MAS Detection & Freemium Model
- **Session**: *App Mechanic Feature Requests* (**Observed**)
- **Builder / Tool**: Google Antigravity (**Observed**)
- **Execution Surface & Editor**: Google Antigravity desktop application on macOS (**Observed**)
- **Model / Mode**: Gemini 3.1 Pro (High) (**Observed**)
- **Human Involvement**: Ron Stauffer outlined a 6-part feature roadmap (fixing auto-updater false positives like Obsidian, adding a Launch button, checking Mac App Store apps, displaying the macOS version and system update status, ignoring specific releases, and linking to maker homepages), and directed introducing the initial freemium licensing flow (**Observed**).
- **Contributions & References**:
  - Added auto-updater recognition, unstable cask filtering, install method badges (`Mac App Store`, `Homebrew`, `Manual / OS`), `/api/launch`, `/api/ignore` & `/api/unignore`, macOS software update detection (`com.apple.SoftwareUpdate.plist`), app homepage links, and initial freemium licensing (`068b595`, `68e0ce9` `v0.3.0`, `25286e0` `v0.4.0`, `87802dd` `v0.5.0`).

### 2026-07-27 to 2026-08-11 (America/Denver, MDT) — `v0.1.0` to `v0.2.0` Initial Scanner, `py2app` Packaging, Code Signing & Scan History
- **Session**: *App Mechanic Project Overview* (`2026-07-28` to `2026-08-11`, **Observed**; follows `2026-07-27` initial repository bootstrap `f4a873e` and core script commit `ea79d2d`)
- **Builder / Tool**: Google Antigravity (**Observed** for `ae0ac28`..`a2f2a52`; GitHub web UI for `f4a873e`)
- **Execution Surface & Editor**: Google Antigravity desktop application on macOS (**Observed**)
- **Model / Mode**: Unknown exact model string (session predates explicit `Model Selection` log entries in Antigravity transcripts)
- **Human Involvement**: Ron Stauffer initialized the repository, tested version detection accuracy, directed packaging into a standalone macOS `.app` bundle with custom icon, configured Apple Developer ID signing and notarization, and requested the persistent 50-scan history log (**Observed**).
- **Contributions & References**:
  - Packaged [`app_mechanic.py`](app_mechanic.py) with `py2app` ([`setup.py`](setup.py), [`AppMechanic.icns`](AppMechanic.icns), [`icon.jpg`](icon.jpg)), added single-instance localhost check, documented architecture in [`NOTES.md`](NOTES.md) and [`README.md`](README.md) (`ae0ac28`), restricted server binding to `127.0.0.1` (`e3aa447`), and added the 50-scan persistent history log (`1e0d183`, tag `v0.2.0`; `0abb027`; `a2f2a52`).
