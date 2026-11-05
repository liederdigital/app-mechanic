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
* **GUI Version Resolution (`Hermes.app`):** When scanning `/Applications/Hermes.app` (`com.nousresearch.hermes`) and `CFBundleShortVersionString` is `"0.0.0"` or `"0.0.1"`, `app_mechanic.py` resolves the real installed version and update state directly from `hermes --version` (`NousResearch Git`) rather than comparing against the community `hermes-desktop` Homebrew Cask (`0.21.2`).
* **Fast 1-Step Diagnostic & Recovery Runbook:**
  * **Check state in one command:** ` ~/.local/bin/hermes --version && tail -n 30 ~/.hermes/logs/desktop.log ~/.hermes/logs/update.log ~/.hermes/logs/errors.log`
  * **One-shot full update & app bundle sync:** `pgrep -x Hermes >/dev/null && { killall Hermes; ~/.local/bin/hermes update --yes && open -a /Applications/Hermes.app; } || ~/.local/bin/hermes update --yes`
  * **Key paths:** Checkout at `~/.hermes/hermes-agent`, OAuth state at `~/.hermes/auth.json` (and `~/.hermes/shared/nous_auth.json`), passive update check cache at `~/.hermes/source-checks/`, logs at `~/.hermes/logs/`.

---

### 3. Grok Bot (`grok-bot` / `com.anysphere.sand`)
* **Report Date:** 2026-11-02
* **App / Tool:** `Grok Bot` (`/Applications/Grok Bot.app`)
* **Installed Version:** `0.78.1`
* **Reported Latest:** `0.78.3`
* **Catalog Source:** Homebrew Cask (`grok-bot`)
* **Install Method:** Manual / OS
* **Classification:** Staged Auto-Updater Rollout vs. Cask Livecheck Feed

#### Upstream Context & Root Cause
* `Grok Bot.app` (`com.anysphere.sand`) auto-updates via `api2.cursor.sh/updates/api/update/darwin-arm64/sand/.../stable`, which rolls out minor patch builds (`0.78.1` -> `0.78.3`) in staged waves or slightly out of sync with the Homebrew Cask `livecheck` scrape.
* Because `Grok Bot` manages its own background updates silently, flagging minor cask diffs produces false alarms on machines where the in-app updater reports `0.78.1` as current.

#### App Mechanic Handling
* Added `'grok bot'` to `auto_updaters` in `app_mechanic.py` so background-managed minor build drift against `grok-bot` does not trigger false alarms.

---

### 4. Sublime Text, Mail Archiver X, & ChatGPT (Missed Updates)
* **Report Date:** 2026-11-02
* **Apps:** `Sublime Text` (`/Applications/Sublime Text.app`), `Mail Archiver X` (`/Applications/Mail Archiver X/Mail Archiver X.app`), `ChatGPT` (`/Applications/ChatGPT.app`)
* **Classification:** Build-String Parsing, Subfolder Bundle Discovery + Kaju Feed, & Over-Broad Auto-Updater Suppression

#### Upstream Context & Root Cause
1. **Sublime Text (`com.sublimetext.4`):** Stores `CFBundleShortVersionString = "Build 4215"` and `CFBundleVersion = "4215"`, whereas Homebrew Cask (`sublime-text`) reports `"4215"`. Previously, `parse_version()` required at least one dot (`^\d+(\.\d+)+`), returning `[]` for both `"Build 4215"` and `"4215"` and defaulting to `up_to_date`.
2. **Mail Archiver X (`com.mothsoftware.mailarchiverx`):** Installs inside a subfolder (`/Applications/Mail Archiver X/Mail Archiver X.app`) and is not in Homebrew Cask; it uses Moth Software's signed Kaju JSON feed (`https://www.mothsoftware.com/UpdateInformation.json`).
3. **ChatGPT (`com.openai.codex`):** Updates `CFBundleShortVersionString` in `Info.plist` (`26.1027.x`), which Homebrew Cask (`chatgpt`) tracks accurately, but `'chatgpt'` was previously listed in `auto_updaters`, unconditionally masking real updates.

#### App Mechanic Handling
* **Sublime Text:** Updated `parse_version()` to parse single-integer and `"Build NNNN"` version strings, and fall back to `CFBundleVersion` when `CFBundleShortVersionString` is non-numeric.
* **Mail Archiver X:** Extended `run_scan()` to discover `.app` bundles one folder deep inside `/Applications/<Subfolder>/` and added `check_mothsoftware_kaju_update()` to query `https://www.mothsoftware.com/UpdateInformation.json`.
* **ChatGPT (and other plist-accurate apps):** Removed `'chatgpt'` (along with other apps that accurately update their `Info.plist`) from `auto_updaters` so legitimate updates are surfaced.

---

### 5. Android Studio (`android-studio`) & Xmind (`xmind`)
* **Report Date:** 2026-11-02
* **Apps:** `Android Studio` (`/Applications/Android Studio.app`, `com.google.android.studio`) & `Xmind` (`/Applications/Xmind.app`, `net.xmind.vana.app`)
* **Installed Versions:** `2026.2` (`AndroidStudio2026.2.2` in `product-info.json`) & `26.05.01107`
* **Reported Latest:** `2026.2.2.8` & `27.01.05086-202610272240`
* **Catalog Source:** Homebrew Cask (`android-studio` / `xmind`)
* **Install Method:** Manual / OS
* **Classification:** Truncated `CFBundleShortVersionString` Prefix (`Android Studio`) & Major Year-Branch Auto-Updater Split (`Xmind`)

#### Upstream Context & Root Cause
1. **Android Studio (`com.google.android.studio`):**
   * Stores only `CFBundleShortVersionString = "2026.2"` in `Info.plist`, while `Contents/Resources/product-info.json` stores `dataDirectoryName = "AndroidStudio2026.2.2"` (`buildNumber = "262.10968.63.2622.16730706"`, which is the exact build of Android Studio Rabbit 2 `2026.2.2.8`).
   * Because `Info.plist` omits the `.2.8` patch/build segments, naive zero-padded comparison treated `[2026, 2, 0, 0] < [2026, 2, 2, 8]` as outdated even when the exact latest release was installed.
2. **Xmind (`net.xmind.vana.app`):**
   * Xmind 26 (`26.05.01107`) is the terminal release of the 2026 branch; Xmind's in-app updater does not auto-upgrade across major year versions (`26.x` -> `27.x`), and Homebrew Cask appends a build timestamp suffix (`-202610272240`).

#### App Mechanic Handling
* **JetBrains / Android Studio `product-info.json` Resolution:** Added `resolve_jetbrains_product_version()` in `app_mechanic.py` to extract the full `X.Y.Z` release from `Contents/Resources/product-info.json`, and updated version comparison so shorter `Info.plist` prefixes (`orig_inst_len >= 2`) that match all leading segments of a 4-part cask build string are treated as `up_to_date`.
* **Xmind Major Branch Handling & Build Suffix Stripping:** Stripped trailing `-<timestamp>` build suffixes from cask versions (`27.01.05086`) and suppressed cross-year major branch alerts (`26.x` vs `27.x`) for Xmind when the installed 26.x branch reports itself up to date.

---

### 6. Superset -> Paradev Rebrand (`superset` / `paradev`)
* **Report Date:** 2026-11-02
* **App / Tool:** `Superset` (`/Applications/Superset.app`, `com.superset.desktop`) -> `Paradev` (`/Applications/Paradev.app`, `com.paradev.desktop`)
* **Classification:** Upstream Application & Cask Rebrand

#### Upstream Context & Root Cause
* Superset (`superset.sh`) rebranded to **Paradev** (`paradev.com`, GitHub `ParadevAI/Paradev`). During a rebrand transition, users may have `Superset.app` or `Paradev.app` installed locally while Homebrew Cask transitions from `superset` to `paradev`.

#### App Mechanic Handling
* Added `APP_REBRAND_MAP` and `BUNDLE_ID_REBRAND_MAP` in `app_mechanic.py` so both `Superset.app` and `Paradev.app` cross-check `paradev` and `superset` casks/tokens, recognize either token in `brew list --cask`, and display as **`Superset (now Paradev)`** / **`Paradev (formerly Superset)`** while keeping `launch_name` mapped to the actual `.app` bundle on disk.

---

### 7. Descript (`descript`) & Mac App Store vs. Homebrew Cask Split (`whatsapp`)
* **Report Date:** 2026-11-02
* **Apps:** `Descript` (`/Applications/Descript.app`, `com.descript.beachcube`) & `WhatsApp` (`/Applications/WhatsApp.app`, `net.whatsapp.WhatsApp`)
* **Installed Versions:** `2.22.1` (`Descript`) & `26.43.75` (`WhatsApp` via Mac App Store)
* **Reported Latest:** `114.0.4` (`Descript` Homebrew Cask) & `26.44.12` (`WhatsApp` Homebrew Cask)
* **Catalog Source:** Homebrew Cask (`descript` / `whatsapp`)
* **Install Method:** Manual / OS (`Descript`) & Mac App Store (`WhatsApp`)
* **Classification:** Electron Shell vs. Web Engine Version Split (`Descript`) & Mac App Store Receipt Isolation (`WhatsApp`)

#### Upstream Context & Root Cause
1. **Descript (`com.descript.beachcube`):**
   * Descript's macOS DMG (`Descript-114.0.4-release.20250509.32955-arm64.dmg`) is versioned after its web/cloud application engine (`114.0.4`), which updates dynamically inside the Electron app, while the outer Electron launcher bundle stamps `CFBundleShortVersionString = "2.22.1"` and `CFBundleVersion = "2.22.1"` in `Info.plist` (verified by `brew info --cask --json=v2 descript` reporting `bundle_short_version: "2.22.1"` for cask `114.0.4`).
2. **WhatsApp (`net.whatsapp.WhatsApp`) & Mac App Store Apps:**
   * When an app is installed from the Mac App Store (`Contents/_MASReceipt` present), its updates are delivered exclusively through the Mac App Store (`mas outdated`).
   * Previously, if a Mac App Store app was not in `mas outdated`, `run_scan()` fell through to `resolve_cask_info()` and compared the Mac App Store bundle against Homebrew Cask's direct-download feed (`whatsapp` cask `26.44.12` vs. Mac App Store `26.43.75`), causing a false alarm whenever direct-download builds shipped ahead of Apple App Store review.

#### App Mechanic Handling
* **Descript:** Added `'descript'` to `auto_updaters` in `app_mechanic.py` so its frozen Electron shell version (`2.22.1`) is not falsely flagged against the `114.x` web engine cask string.
* **Mac App Store Isolation:** Updated `run_scan()` so any app with `install_method == "Mac App Store"` (`Contents/_MASReceipt`) is checked exclusively against `mas outdated` and reported with `source: "Mac App Store"` rather than falling through to Homebrew Cask.

---

### 8. ChatGPT (`chatgpt` / `com.openai.codex`) — Intra-Day Sub-Build Cohort Drift ([Issue #2](https://github.com/liederdigital/app-mechanic/issues/2))
* **Report Date:** 2026-11-05
* **App / Tool:** `ChatGPT` (`/Applications/ChatGPT.app`, `com.openai.codex`)
* **Installed Version:** `26.1029.61003` (`CFBundleVersion = "24614"`)
* **Reported Latest:** `26.1029.70936`
* **Catalog Source:** Homebrew Cask (`chatgpt`)
* **Install Method:** Manual / OS
* **Classification:** Cohort-Gated Dynamic Appcast vs. Static Cask `appcast.xml` on Same `YY.MMDD` Release Train

#### Upstream Context & Root Cause
* Inside `/Applications/ChatGPT.app/Contents/Resources/app.asar`, `ChatGPT.app` (`com.openai.codex`) resolves its in-app update checks against a dynamic, cohort-gated backend endpoint:
  `https://updates.oaistatic.com/codex/app/appcast?installation_id=<id>&arch=arm64&app_version=26.1029.61003&beta=false&os-version=<ver>&plan_type=<plan>`
* Meanwhile, Homebrew Cask (`chatgpt`) scrapes the static feed `https://persistent.oaistatic.com/codex-app-prod/appcast.xml` (`ChatGPT-darwin-arm64-26.1029.70936.zip`).
* Both `26.1029.61003` and `26.1029.70936` belong to the same **`26.1029` (`YY.MMDD`, October 29, 2026)** release train; only the third segment (the intra-day sub-build identifier `61003` vs. `70936`) differs. OpenAI's dynamic appcast reports `26.1029.61003` as up to date rather than forcing every `installation_id` / `plan_type` cohort onto same-day sub-builds.

#### App Mechanic Handling
* Updated `_run_scan_impl()` in `app_mechanic.py` so that for `ChatGPT` (`com.openai.codex`), when the installed version and the Homebrew Cask version share the same `YY.MMDD` release date (`p_inst[:2] == p_late[:2]`, e.g., `26.1029.*`), the app is treated as `up_to_date` (`latest_ver = installed_ver`), while still flagging genuine multi-day release updates (such as `26.1027.*` -> `26.1029.*`).

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
