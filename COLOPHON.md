# Colophon

How this repository was made: which tools did the work, where they ran, what
each contributed, and who directed it. License and third-party notices live
elsewhere ([`LICENSE`](LICENSE)).

## Snapshot

| | |
|---|---|
| Project | App Mechanic (`liederdigital/app-mechanic`) |
| Primary builder | Google Antigravity |
| Surface | desktop app |
| Model / mode | Gemini (Low effort) (shown by the tool in session transcript `USER_SETTINGS_CHANGE`); earlier phases used Gemini (High effort), Gemini (Medium effort), and Gemini 3.1 Pro (High) (shown by the tool) |
| Editor | Google Antigravity IDE (`Antigravity.app`) |
| Review | Human, Ron Stauffer (cross-machine testing on macOS across MacBook Air, MacBook Pro, and iMac; screenshot and Terminal verification) |
| Directed by | Ron Stauffer |
| Human owner | Ron Stauffer (Lieder Digital, LLC), product direction, multi-Mac testing, Apple Developer ID signing/notarization & Gumroad configuration, release approval |
| Era | 2026-07-27 to 2026-11-04 (America/Denver, Mountain Time) |
| Status | active (`v0.6.6`) |

## How the work was done

Ron Stauffer directed the product architecture, feature roadmap, catalog accuracy rules, and UI design across ten sessions in the Google Antigravity desktop application on macOS, testing builds across a MacBook Air, MacBook Pro, and iMac and approving each release. Google Antigravity wrote and maintained the pure-Python application ([`app_mechanic.py`](app_mechanic.py)), `py2app` bundle configuration ([`setup.py`](setup.py)), code-signing and Apple notarization script ([`build.sh`](build.sh)), and documentation ([`README.md`](README.md), [`NOTES.md`](NOTES.md), [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md)), as well as the companion marketing site and interactive simulator at [`liederdigital/appmechanic.dev`](https://github.com/liederdigital/appmechanic.dev).

## Builder history (newest first)

| Date | Builder | Role | Surface | Model / mode | Contribution | Evidence |
|---|---|---|---|---|---|---|
| 2026-11-04 | Claude Code | reviewed | browser or cloud workspace (Claude Code cloud session) | Claude Opus 5.5 (`claude-opus-5-5`) (shown by the tool, session metadata); reasoning setting Unknown | Forensic review of this colophon against repository evidence only (`f4a873e` through `2d533cf`, Git tags `v0.1.0` to `v0.6.6`, `CREDITS.md`, `AGENTS.md`, `README.md`, `NOTES.md`, `KNOWN_ISSUES.md`); added the corrections below without changing earlier rows; no code changed | Corrections section below |
| 2026-11-02 | Google Antigravity | built, deployed | desktop app | Gemini (Low effort) (shown by the tool) | Releases `v0.6.4`, `v0.6.5`, and `v0.6.6`: added per-row `⚠️` Update Error Reporter (`/api/log_error`, `update_errors.json`), keg-only Homebrew & version-manager Node `PATH` auto-discovery (`get_node_bin_dirs()`) + cross-prefix `package.json` version lookup (`find_npm_pkg_version()`), `npm install -g --force` for global CLI updates (`@github/copilot`, `openclaw` with `--allow-scripts`), `Sort by` Install/Update Type selector and sortable headers, `APP_REBRAND_MAP` (`Superset` → `Paradev`), 1-level `/Applications/<Subfolder>/` scanning + Moth Software Kaju feed check (`Mail Archiver X`), single-integer `Build XXXX` parsing (`Sublime Text`), JetBrains `product-info.json` resolution (`Android Studio`), Mac App Store `_MASReceipt` isolation from Homebrew Cask (`WhatsApp`), `Descript` & `Discord` self-updater handling, prominent header version badge + step-by-step **About & How to Update App Mechanic** modal + GitHub Releases self-check in the scanned apps table (`check_app_mechanic_github_update()`), instant `<1s` browser launch with live **App Mechanic is Scanning Your Mac...** progress modal (`ThreadedTCPServer` + background initial scan thread), increased Lite free scan allowance from 3 to 5, capped scan history at 10 entries, and `COLOPHON.md` | `dc50263` (`v0.6.4`), `d86034a` (`v0.6.5`), `97d235c`, [`app_mechanic.py`](app_mechanic.py), [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) |
| 2026-10-26 | Google Antigravity | built | desktop app | Gemini 3.8 Flash (High) (shown by the tool) | Created [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) documenting `OpenCode` and `Hermes` catalog discrepancies; updated `Hermes` `update_cmd` and version resolution in [`app_mechanic.py`](app_mechanic.py) to quit running `Hermes.app` cleanly before `hermes update --yes` | `bd80120`, [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md), [`app_mechanic.py`](app_mechanic.py) |
| 2026-10-24 | Google Antigravity | built, deployed | desktop app | Gemini 3.8 Flash (High) (shown by the tool) | Release `v0.6.3`: pointed in-app Pro checkout directly to `store.liederdigital.com/l/appmechanic`, standardized Gumroad URLs, and simplified [`docs/`](docs/) to redirect to `appmechanic.dev` | `c44c6e0` (`v0.6.3`), [`app_mechanic.py`](app_mechanic.py), [`docs/index.html`](docs/index.html) |
| 2026-10-23 to 2026-10-24 | Google Antigravity | built, deployed | desktop app | Gemini (Medium effort) (shown by the tool) | Releases `v0.6.0`, `v0.6.1`, and `v0.6.2`: added Pro-exclusive AI & Vibe-Coding CLI scanner (`get_ai_cli_tools()`, 25+ agents), `uv tool` scanner (`get_uv_tools()`), 1-click Terminal CLI upgrades, `🚩 False Alarm` badge & inaccuracy reporter (`false_alarms.json`), initial [`CREDITS.md`](CREDITS.md), and companion site [`liederdigital/appmechanic.dev`](https://github.com/liederdigital/appmechanic.dev) | `e7c9270`, `39d3ac0`, `837c5fd`, `3e99ba4`, `4e10a45` (`v0.6.0`), `643fb2b`, `8459d17` (`v0.6.1`), `ead0781` (`v0.6.2`), `9401dd3`, `5521d5a` |
| 2026-10-16 | Google Antigravity | built, deployed | desktop app | Gemini (Medium effort) (shown by the tool) | Release `v0.5.5`: fixed LaunchServices helper bundle collision (`Wispr Flow`) by launching explicit `/Applications/<App>.app` paths, ignored placeholder MAS ID `0`, and skipped dot-prefixed hidden bundles | `5891abf` (`v0.5.5`), [`app_mechanic.py`](app_mechanic.py) |
| 2026-09-21 | Google Antigravity | built | desktop app | Gemini 3.1 Pro (High) (shown by the tool) | Replaced `webbrowser.open` with `open http://localhost:8000` and added single-instance exit delay to fix Finder `"not open anymore"` and AppleEvents errors | `8a95680` (`v0.5.4`), [`app_mechanic.py`](app_mechanic.py) |
| 2026-09-18 | Google Antigravity | built | desktop app | Gemini 3.1 Pro (High) (shown by the tool) | Release `v0.5.4`: added developer CLI scanning (`get_npm_tools()`, `get_pipx_tools()`, `get_brew_formulae()`), `/api/update_cli` AppleScript Terminal runner, and `macappstore://` deep links | `ea1d3a8`, [`app_mechanic.py`](app_mechanic.py) |
| 2026-08-22 to 2026-09-06 | Google Antigravity | built | desktop app | Gemini 3.1 Pro (High) (shown by the tool) | Release `v0.5.3`: migrated Pro license activation from LemonSqueezy to Gumroad (`/v2/licenses/verify`) and refined the Unlock Pro modal | `438d671`, `2da08c8` (`v0.5.3`), [`app_mechanic.py`](app_mechanic.py) |
| 2026-08-17 to 2026-08-19 | Google Antigravity | built | desktop app | Gemini 3.1 Pro (High) (shown by the tool) | Releases `v0.3.0`, `v0.4.0`, and `v0.5.0`: added auto-updater filtering, unstable cask filtering, install method badges, `/api/launch`, `/api/ignore` & `/api/unignore`, macOS software update detection, and initial freemium scan counter | `068b595`, `68e0ce9` (`v0.3.0`), `25286e0` (`v0.4.0`), `87802dd` (`v0.5.0`) |
| 2026-07-28 to 2026-08-11 | Google Antigravity | built | desktop app | Unknown | Releases `v0.1.0` and `v0.2.0`: packaged [`app_mechanic.py`](app_mechanic.py) with `py2app` ([`setup.py`](setup.py)), configured Developer ID signing & Apple notarization ([`build.sh`](build.sh)), restricted server to `127.0.0.1`, and added 50-scan history (`history.json`) | `ae0ac28` (`v0.1.0`), `e3aa447`, `1e0d183` (`v0.2.0`), `0abb027`, `a2f2a52` |
| 2026-07-27 | Ron Stauffer | built | Unknown | Unknown | Initial repository bootstrap (`f4a873e` via GitHub web UI) and initial `app_mechanic.py` commit (`ea79d2d`) | `f4a873e`, `ea79d2d` |

## Corrections (forensic review, 2026-11-04)

Earlier rows are kept as written. These notes record where the repository's
own evidence differs from them, or cannot support them.

- **`ea79d2d` (2026-07-27): builder Unknown.** The row above credits Ron
  Stauffer as builder. Ron Stauffer is the Git author of every commit, but a
  Git author is only the identity that made the commit, not proof of who or
  what wrote the change. This commit added the first 882-line
  `app_mechanic.py` and has no AI trailer. Whether a tool wrote it is Unknown,
  as "Evidence limits" already says. `f4a873e` (`LICENSE` and a README stub)
  has the committer `GitHub <noreply@github.com>`, which fits the GitHub web
  UI.
- **No AI trailers in Git.** No commit has a `Co-Authored-By`, `Assisted-by`,
  or similar trailer. Every Google Antigravity credit and every model value in
  the history above comes from session transcripts on the owner's Mac. Those
  transcripts are not in this repository, so they could not be checked in
  this review.
- **Model values that don't line up.** The Snapshot lists "Gemini (High
  effort)", which appears in no history row. In `CREDITS.md`, the Snapshot gives
  Gemini (Medium effort) for 2026-10-16 to 2026-10-24, but its own 2026-10-24
  entry and this file's 2026-10-24 row give Gemini 3.8 Flash (High). Which
  model ran when is Unknown from repository evidence alone.
- **Release tags vs. rows** (from `git ls-remote --tags`):
  - `v0.2.1` and `v0.2.2` both point to `a2f2a52`. No row lists them.
  - `v0.3.0` points to `068b595`, not `68e0ce9`.
  - `v0.5.0` points to `25286e0`, the same commit as `v0.4.0`, but
    `VERSION = "0.5.0"` first appears in `87802dd`.
  - `v0.5.1` points to `438d671` (2026-08-19). No row lists it.
  - `v0.5.4` points to `8a95680`, although `ea1d3a8` already set
    `VERSION = "0.5.4"`.
  - `v0.6.0` points to `643fb2b`, and `v0.6.2` points to `9401dd3`.
  - `v0.6.6` points to `2d533cf` (2026-11-02). That commit also updated the
    2026-11-02 row, so the row could not cite it.
  - No `v0.5.2` tag exists.
- **Date range.** The "2026-08-22 to 2026-09-06" row cites `438d671`, dated
  2026-08-19. The repository has no commits between 2026-08-19 and
  2026-09-06, so the 2026-08-22 start date can't be confirmed here.
- **Human testing and approval.** Testing on a MacBook Pro and an iMac, and
  "approving each release", are not recorded in repository files. `CREDITS.md`
  mentions only MacBook Air testing. Git shows that Ron Stauffer's identity
  made and tagged each release. It doesn't show how each one was reviewed.

## Evidence limits

- Followed **COLOPHON.md instructions v1.1.2** (https://colophon.md).
- **2026-11-04 forensic review** (Claude Code, cloud session): used only
  evidence in this repository: full `git log` with author, committer, and
  trailers (`f4a873e` through `2d533cf`), remote Git tags, per-commit `VERSION`
  strings, [`CREDITS.md`](CREDITS.md), [`AGENTS.md`](AGENTS.md),
  [`README.md`](README.md), [`NOTES.md`](NOTES.md), and
  [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md). No coding-agent session logs from
  earlier work exist in this cloud container, and no Google Antigravity
  transcripts were available. Running the same pass on the owner's other
  computers may fill more gaps.
- **Inspected**: Full `git log` (`f4a873e` through `97d235c`), existing [`CREDITS.md`](CREDITS.md), [`README.md`](README.md), [`NOTES.md`](NOTES.md), [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md), and 10 local Google Antigravity session transcripts on the owner's development Mac (`2026-07-28` through `2026-11-02`).
- **Remains Unknown**:
  - The exact model version and reasoning setting for the earliest Google Antigravity session (`2026-07-28` to `2026-08-11`, commits `ae0ac28`..`a2f2a52`), which predates `USER_SETTINGS_CHANGE` model-selection records in Antigravity transcripts.
  - Whether an AI tool assisted with commit `ea79d2d` (`2026-07-27`, committed one day before the first local Antigravity transcript on this computer).
- The commit that created or updated this file can be found with `git log -- COLOPHON.md`.
