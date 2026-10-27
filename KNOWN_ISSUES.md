# Known Catalog Discrepancies & False Alarm Log

This document tracks known upstream catalog mismatches, split release lines, and packaging idiosyncrasies reported through App Mechanic's **False Alarm & Inaccuracy Reporter** (`v0.6.2+`). 

When an app reports a mismatch that is not a bug in App Mechanic’s parser, but rather an upstream release divergence, it is cataloged here for ongoing scanner tuning.

---

## Log Entries

### 1. OpenCode (`opencode-desktop`)
* **Report Date:** 2026-10-26
* **App / Tool:** `OpenCode` (`/Applications/OpenCode.app`)
* **Installed Version:** `1.19.4`
* **Reported Latest:** `2.1.4`
* **Catalog Source:** Homebrew Cask (`opencode-desktop`)
* **Install Method:** Manual / OS
* **Classification:** Upstream Major Version Split & Disabled Auto-Updates

#### Upstream Context & Root Cause
* **Dual Release Branches:** `1.19.4` is the active maintenance line for **OpenCode V1** (`opencode-ai`). `2.1.4` is the stable line for the overhauled **OpenCode V2** (`@opencode/cli`).
* **Frozen Auto-Updates:** Starting in `1.19.0+`, OpenCode intentionally disabled automatic background updates for major version upgrades to prevent unexpected breaking changes for users on the 1.x line.
* **Catalog Tracking:** Homebrew Cask (`opencode-desktop`) tracks the active HEAD version (`2.1.4`). Because `2.1.4 > 1.19.4`, App Mechanic flags the app as Outdated.
* **User Impact:** To users on the 1.x branch whose app claims to be "up to date" (within 1.x), this looks like a false positive alert.

#### App Mechanic Handling
* **Scanner Status:** Working as designed. `2.1.4` is a legitimate upgrade, so suppressing it globally via `auto_updaters` is not recommended (doing so would prevent users from knowing v2 exists).
* **Local Resolution:** Users who intentionally remain on the 1.x branch can flag the item as **`🚩 False Alarm`** or **`🚫 Ignore`** in App Mechanic. It is then saved to `~/Library/Application Support/AppMechanic/false_alarms.json` and counted as healthy (`🟢 Up to Date`).
* **Manual Upgrade Command:** Users wishing to upgrade to V2 can update the desktop app via `brew install --cask --force opencode-desktop` (or download the DMG from [opencode.ai](https://opencode.ai)), and/or install the CLI via `curl -fsSL https://opencode.ai/v2/install | bash` or `npm install -g @opencode/cli`.

---

### 2. Hermes Agent & Hermes Desktop (`hermes` / `Hermes.app`)
* **Report Date:** 2026-10-26
* **App / Tool:** `Hermes` (`/Applications/Hermes.app`) & `Hermes Agent (hermes)` (`~/.local/bin/hermes`)
* **Installed Version:** `0.0.0` in `Info.plist` (`v0.21.5` / `v0.22.5` in CLI runtime)
* **Reported Latest:** `Update Available` (or Cask version mismatch)
* **Catalog Source:** NousResearch Git (`~/.hermes/hermes-agent`)
* **Install Method:** Manual / OS (local source build) & AI CLI (`git`)
* **Classification:** Running-App Bundle Swap Lockout, Local Build `0.0.0` `Info.plist` Stamp, & Git Compare API Commit Cap

#### Upstream Context & Root Cause
1. **CLI Update Skips `/Applications/Hermes.app` While Running (GUI/Backend Split):**
   * `hermes update` rebuilds both the Python backend (`~/.hermes/hermes-agent`) and the packaged macOS Electron app (`/Applications/Hermes.app`).
   * However, if `/Applications/Hermes.app` is currently open when `hermes update` is invoked from a terminal (or via App Mechanic's **Update** button), `hermes update` **refuses to overwrite `/Applications/Hermes.app`** (`⚠ /Applications/Hermes.app is running and was not refreshed`) while simultaneously **killing the running Desktop app's local loopback backend process** (`Stopping 1 dashboard process(es) (the running backend no longer matches the updated frontend)`).
   * This leaves the open `Hermes.app` window stranded on the pre-update frontend version with a dead backend until the user manually quits `Hermes.app` and runs `hermes update` a second time.
2. **Local Ad-Hoc Electron Build Stamps `0.0.0` in `Info.plist`:**
   * Because `hermes update` builds `/Applications/Hermes.app` locally from `apps/desktop/package.json` (`"version": "0.0.0"`) with an ad-hoc signature, `/Applications/Hermes.app/Contents/Info.plist` reports `CFBundleShortVersionString = "0.0.0"`. The true version is reported by `hermes --version` (or `~/.hermes/hermes-agent`).
3. **`main` Channel Commit Flood vs. `stable` Channel (`v0.22.5+`):**
   * Prior to `v0.22.5`, Hermes checkouts defaulted to tracking every commit on `origin/main` (~500 commits/day). After a few weeks without updating, the checkout falls thousands of commits behind (e.g., 9,953 commits), exceeding GitHub's `/compare/` API limit and causing `~/.hermes/source-checks/<id>.json` to record `"behind": -1, "commits": []` (which renders in Hermes Desktop's status bar as `v0.21.5 (update)` with an empty changelog). Starting in `v0.22.5`, Hermes defaults to the `stable` release channel.
4. **Nous Portal OAuth Token Expiry After Extended Idle:**
   * If Hermes is not opened for several weeks and background refresh fails, `~/.hermes/auth.json` loses its `access_token` (`No access token found for Nous Portal login.`), causing Hermes Desktop to display a startup reply error modal on the last active session until OAuth device login completes or a free/configured model is selected.

#### App Mechanic Handling
* **Safe Update Command (`update_cmd`):** Updated `Hermes Agent (hermes)` in `app_mechanic.py` to:
  ```sh
  pgrep -x Hermes >/dev/null && { killall Hermes; hermes update --yes && open -a Hermes; } || hermes update --yes
  ```
  If `Hermes.app` is running, App Mechanic cleanly quits it before running `hermes update --yes` so the rebuilt `/Applications/Hermes.app` bundle is always swapped in a single pass and then relaunched.
* **GUI Version Resolution (`Hermes.app`):** When scanning `/Applications/Hermes.app` (`com.nousresearch.hermes`) and `CFBundleShortVersionString` is `"0.0.0"`, `app_mechanic.py` resolves the real installed version from `hermes --version` so the GUI row never reports `0.0.0`.
* **Fast 1-Step Diagnostic & Recovery Runbook:**
  * **Check state in one command:** ` ~/.local/bin/hermes --version && tail -n 30 ~/.hermes/logs/desktop.log ~/.hermes/logs/update.log ~/.hermes/logs/errors.log`
  * **One-shot full update & app bundle sync:** `pgrep -x Hermes >/dev/null && { killall Hermes; ~/.local/bin/hermes update --yes && open -a /Applications/Hermes.app; } || ~/.local/bin/hermes update --yes`
  * **Key paths:** Checkout at `~/.hermes/hermes-agent`, OAuth state at `~/.hermes/auth.json` (and `~/.hermes/shared/nous_auth.json`), passive update check cache at `~/.hermes/source-checks/`, logs at `~/.hermes/logs/`.

---

## Report Entry Template

For new reports received via GitHub Issues or Email:

```markdown
### [App Name] ([Catalog Token / Identifier])
* **Report Date:** YYYY-MM-DD
* **App / Tool:** [Display Name] ([Bundle or Binary Path])
* **Installed Version:** [X.Y.Z]
* **Reported Latest:** [A.B.C]
* **Catalog Source:** [Homebrew Cask / Formula / MAS / NPM / uv / etc.]
* **Install Method:** [Manual / OS | Homebrew | MAS]
* **Classification:** [e.g. Major Version Split | Auto-Updater Desync | Token Disambiguation | Bundle Version Mismatch]

#### Upstream Context & Root Cause
[Explain why the mismatch occurs, e.g. CFBundleVersion vs CFBundleShortVersionString, upstream repo migration, multi-branch releases, etc.]

#### App Mechanic Handling
[Note whether this should be solved via code in app_mechanic.py, added to auto_updaters, or handled via local false_alarms.json]
```
