# App Mechanic — Project Architecture & Engineering Notes

## Overview
App Mechanic (`v0.6.3`) is a zero-dependency macOS utility written in pure Python standard library. It scans `/Applications` and developer CLI toolchains, cross-references installed versions against Homebrew Casks, the Mac App Store (`mas`), Homebrew Formulae, NPM, PyPI (`uv` / `pipx`), and 25+ AI coding agent release channels, and serves a local glassmorphic dashboard on `http://127.0.0.1:8000`.

## Repositories & Live Endpoints
- **Core App Repository:** [`github.com/liederdigital/app-mechanic`](https://github.com/liederdigital/app-mechanic)
- **Website Repository:** [`github.com/liederdigital/appmechanic.dev`](https://github.com/liederdigital/appmechanic.dev)
- **Production Website:** [https://appmechanic.dev](https://appmechanic.dev) (Cloudflare Pages project `app-mechanic.pages.dev`)
- **Pro Licensing (Gumroad):** [https://store.liederdigital.com/l/appmechanic](https://store.liederdigital.com/l/appmechanic) (permalink `appmechanic`, API Product ID `iM_J0YmI3uSqvcIJ7l3uFQ==`)
- **Legacy Lieder Digital Page:** [https://liederdigital.com/apps/app-mechanic](https://liederdigital.com/apps/app-mechanic) (301 redirect to [https://appmechanic.dev](https://appmechanic.dev))

## How Version Detection Works (`app_mechanic.py`)
1. **Mac App Store (`mas`) Apps (`get_mas_outdated()`, `get_mas_installed()`):**
   - Shells out to `mas outdated` and `mas list`, ignoring placeholder ID `0`.
   - Outdated MAS apps link directly to `macappstore://apps.apple.com/app/id<MAS_ID>` when clicked.
2. **Homebrew Cask GUI Apps (`fetch_brew_casks()`):**
   - Fetches `https://formulae.brew.sh/api/cask.json`, maps `.app` bundle artifacts, prioritizes exact token matches and stable casks over unstable (`beta`, `nightly`, `dev`, `alpha`, `rc`, `canary`) variants, and compares `CFBundleShortVersionString` / `CFBundleVersion` using segment-padded integer tuples.
   - Filters known silent background auto-updaters (`obsidian`, `discord`, `slack`, `notion`, `cursor`, `code`, `spotify`, `figma`, `whatsapp`, `opera`, `descript`, `chatgpt`, `claude`, `firefox`, etc.) to prevent false positives.
3. **Pro-Only AI & Vibe-Coding CLI Scanner (`get_ai_cli_tools()`):**
   - Gated strictly behind `is_pro_unlocked()`.
   - Checks native self-updaters and upstream registries for `grok` (`grok update --check --json`), `muse` (`api.meta.ai/muse-code/channels/muse-stable`, updated synchronously via `MUSE_SYNC_UPDATE=1 muse --version`), `herdr` (`herdr.dev/latest.json`), `hermes` (`hermes --version`), `openclaw` (`openclaw-safe-update` / NPM), `agy`, `claude`, `codex` (`codex update`), `gemini`, `kimi`, `vibe`, `amp`, `opencode`, `qwen`, `cline`, `kilo`, `pi`, `copilot`, `aider`, `letta`, `openhands`, `goose`, `mercury` (`mercury upgrade`), and `basecamp` (`basecamp upgrade`).
4. **Pro-Only Developer Package Managers (`get_uv_tools()`, `get_npm_tools()`, `get_pipx_tools()`, `get_brew_formulae()`):**
   - Deduplicates packages already covered by `get_ai_cli_tools()`.
   - Dispatches 1-click Terminal upgrades via `osascript` (`/api/update_cli`).
5. **Local State & Overrides (`~/Library/Application Support/AppMechanic/`):**
   - `history.json`: Rolling 50-scan history log.
   - `license.json`: Activated Gumroad Pro license state.
   - `usage.json`: Free tier scan counter (3 free GUI scans).
   - `ignored_releases.json`: Version-specific ignored updates (`🚫 Ignore`, counted under `🟡 Ignored`).
   - `false_alarms.json`: Persistent catalog-mismatch overrides (`🚩 False Alarm`, counted as green `🟢 Up to Date` and paired with a 1-click GitHub Issue / Email inaccuracy report modal).

## Packaging & Notarization (`build.sh`)
- Bundles `app_mechanic.py` into a universal macOS `.app` (`LSUIElement: True`) via `py2app`.
- Signs all Mach-O binaries, frameworks, and bundle resources with `Developer ID Application: Lieder Digital, LLC (W6YRSA9Z5F)` (`--options runtime --timestamp`).
- Submits to Apple Notary Service via `xcrun notarytool submit ... --wait` and staples the ticket via `xcrun stapler staple "dist/App Mechanic.app"`.
