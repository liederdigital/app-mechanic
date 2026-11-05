# App Mechanic (`v0.6.7`)

![App Mechanic Icon](icon.jpg)

**App Mechanic** is a sleek, zero-dependency macOS utility written in pure Python that scans your installed `/Applications` and developer CLI toolchains against **Homebrew Casks**, **Mac App Store (`mas`)**, **Sparkle (`SUFeedURL`) & `electron-updater` (`app-update.yml`) feeds**, **Homebrew Formulae**, **NPM Global**, **Python `uv` & `pipx`**, and **25+ AI & Vibe-Coding CLI release channels**.

🌐 **Official Website & Live Interactive Simulator:** [https://appmechanic.dev](https://appmechanic.dev) (companion repo: [`liederdigital/appmechanic.dev`](https://github.com/liederdigital/appmechanic.dev))  
⚡ **Get App Mechanic Pro (\$12 once, no subscription):** [https://store.liederdigital.com/l/appmechanic](https://store.liederdigital.com/l/appmechanic)

It serves a glassmorphic dark-mode dashboard directly on `http://localhost:8000` so you can see the health of your entire Mac software stack at a glance.

---

## Features

### Free Starter Tier
- **5 Free Full macOS GUI Scans:** Scans `/Applications` against Homebrew Casks and the Mac App Store (`mas`).
- **Smart Auto-Updater Filtering:** Recognizes self-updating apps (Cursor, VS Code, Obsidian, Slack, Discord, Claude, ChatGPT, Spotify, Figma, etc.) and filters out unstable `beta`, `nightly`, and `canary` casks.
- **10-Scan Local History Log:** Tracks your overall system health percentage over time in `~/Library/Application Support/AppMechanic/history.json`.
- **macOS System Update Detection:** Inspects `com.apple.SoftwareUpdate.plist` and displays a header badge when a macOS update is waiting.

### App Mechanic Pro (`$12` One-Time License via Gumroad)
- **Unlimited System Scans** anytime.
- **🤖 25+ AI & Vibe-Coding CLI Scanner (Pro Exclusive):** Detects and checks installed versions against official release channels for:
  - **Claude Code** (`claude`), **Grok Build** (`grok`), **Meta Muse** (`muse`), **Mistral Vibe** (`vibe`), **OpenAI Codex** (`codex`), **Google Gemini CLI** (`gemini`), **Moonshot Kimi** (`kimi`), **Herdr** (`herdr`), **Hermes Agent** (`hermes`), **OpenClaw** (`openclaw`), **Sourcegraph Amp** (`amp`), **OpenCode** (`opencode`), **Alibaba Qwen Code** (`qwen`), **Cline** (`cline`), **Kilo Code** (`kilo`), **Pi Coding Agent** (`pi`), **GitHub Copilot CLI** (`copilot`), **Aider** (`aider`), **Letta** (`letta`), **OpenHands** (`openhands`), **Block Goose** (`goose`), **Mercury CLI** (`mercury`), **Basecamp CLI** (`basecamp`), and **Antigravity CLI** (`agy`).
- **🛠️ Developer Package Manager & Shell Scanner (Pro Exclusive):** Scans **Homebrew Formulae** (`brew leaves`), **macOS Legacy `/bin/bash`** (detects Apple's frozen 2007 `3.2.57` `/bin/bash` when Homebrew `bash` `5.x` is not installed, with 1-click `brew install bash` and sticky ignore support), **NPM Global** (`npm outdated -g`), **Python `uv` tools** (`uv tool list`), and **Pipx** (`pipx list`).
- **⬆️ 1-Click Terminal CLI Upgrades & 🚀 1-Click App Launch:** Dispatches AppleScript to macOS Terminal to run the exact native upgrade command (`claude update`, `grok update`, `MUSE_SYNC_UPDATE=1 muse --version`, `codex update`, `herdr update`, `basecamp upgrade`, `brew upgrade`, `brew install bash`, `uv tool upgrade`, `npm install -g`, etc.) or opens outdated Mac App Store apps directly to their `macappstore://` page.
- **🚫 Ignore Releases & 🚩 Flag False Alarms:** Skip specific point updates (`ignored_releases.json`) or flag catalog mismatches (`false_alarms.json`) as green/healthy with a 1-click GitHub Issue / Email diagnostic reporter.

---

## Supported Update Channels & Self-Managed Apps

App Mechanic verifies installed GUI and CLI versions across the following channels:
- **Homebrew Casks (`formulae.brew.sh`):** Includes standard `.app` casks, `target`-renamed installers, and `.pkg` / `installer` suites (such as Microsoft Office, Zoom, Cloudflare WARP, Tailscale, Adobe Acrobat Pro, Google Drive, DisplayLink, Karabiner-Elements, Logitech Options+ / G HUB / Logi Tune, and MAMP).
- **Mac App Store (`mas`):** Includes native macOS App Store bundles (`Contents/_MASReceipt`) and Apple Silicon iOS/iPadOS App Store Wrapper bundles (`WrappedBundle/Info.plist` & `Wrapper/iTunesMetadata.plist`).
- **Built-In App Feeds:** Automatically checks **Sparkle Appcast XML feeds** (`SUFeedURL` in `Info.plist`), **`electron-updater` manifests** (`Contents/Resources/app-update.yml` generic `latest-mac.yml` and GitHub Releases providers), **Moth Software Kaju feeds**, **MediaHuman XML feeds**, and **NousResearch Git**.
- **AI & Developer CLI Toolchains:** Homebrew Formulae, macOS `/bin/bash`, NPM Global, Python `uv` & `pipx`, and 25+ AI coding agents.

### Self-Managed & Ecosystem Apps
To keep your dashboard clutter-free so you can always reach a clean **100% green (`0 Outdated`)** state, apps managed by closed external updaters are shown as healthy with a descriptive `?` source tooltip:
- **Adobe Creative Cloud Suite** (*Photoshop, Illustrator, InDesign, Lightroom Classic, Bridge, Premiere Rush*): Managed exclusively inside the proprietary **Adobe Creative Cloud Desktop** daemon (except *Adobe Acrobat Pro*, which is checked automatically).
- **macOS Built-In & Companion Apps** (*Safari, Google Drive shortcut stubs, Python IDLE, Automator apps*): Managed by macOS **System Settings ➔ General ➔ Software Update** (which App Mechanic surfaces in the top header badge) or by their parent application.
- **Closed-Feed Standalone Apps**: Apps that require an authenticated in-app license session to check for updates (such as *Hindenburg PRO*, *Sitebulb*, or *Muse Hub*) display `Self-Managed (Check in-app for updates)` in their source tooltip and provide a 1-click **🚀 Launch** button.

---

## Prerequisites & Dependencies
App Mechanic uses only the Python standard library (`0` third-party Python packages required). To scan standard GUI apps and Mac App Store apps accurately, install:

1. **Homebrew**: Used to check the latest versions of standard macOS apps and CLI formulae. Install from [brew.sh](https://brew.sh).
2. **`mas` (Mac App Store CLI)**: Used to check the latest versions of App Store apps. Install via Homebrew:
   ```bash
   brew install mas
   ```

---

## Installation

App Mechanic is officially code-signed with a Developer ID by **Lieder Digital, LLC** and **Notarized by Apple**.

1. Download the latest `AppMechanic-v0.6.7-Signed.zip` from the [GitHub Releases](https://github.com/liederdigital/app-mechanic/releases/latest) page (or [appmechanic.dev](https://appmechanic.dev)).
2. Double-click to extract the `.zip`.
3. Drag `App Mechanic.app` into your `/Applications` folder and double-click to launch!

---

## Architecture & Repository Layout
- **Application Repo (`liederdigital/app-mechanic`)**:
  - [`app_mechanic.py`](app_mechanic.py) — Single-file Python scanner, local HTTP server (`127.0.0.1:8000`), Gumroad `/v2/licenses/verify` client, and embedded glassmorphic web UI.
  - [`setup.py`](setup.py) & [`build.sh`](build.sh) — `py2app` bundling, Developer ID code signing, Apple `notarytool` submission, and `stapler` packaging.
  - [`docs/`](docs/) — Redirect to official website and live interactive simulator at [appmechanic.dev](https://appmechanic.dev).
  - [`COLOPHON.md`](COLOPHON.md) — Repository colophon and AI/tool build record.
- **Website Repo ([`liederdigital/appmechanic.dev`](https://github.com/liederdigital/appmechanic.dev))**:
  - Deployed via Cloudflare Pages (`app-mechanic.pages.dev`) to **[https://appmechanic.dev](https://appmechanic.dev)**.

---

## License & Disclaimer
This software is provided under the **MIT License** by Lieder Digital, LLC.

**WARNING:** This software comes with **ABSOLUTELY NO WARRANTIES WHATSOEVER**. While it definitely won't break your computer or delete your emails and passwords, Lieder Digital, LLC is not responsible if it accidentally leaves the back door open and your dog runs away from home. Use at your own risk! See the [LICENSE](LICENSE) file for more details.

How this repository was made is recorded in [COLOPHON.md](COLOPHON.md).
