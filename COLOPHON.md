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
| Era | 2026-07-27 to 2026-11-02 (America/Denver, Mountain Time) |
| Status | active (`v0.6.5`) |

## How the work was done

Ron Stauffer directed the product architecture, feature roadmap, catalog accuracy rules, and UI design across ten sessions in the Google Antigravity desktop application on macOS, testing builds across a MacBook Air, MacBook Pro, and iMac and approving each release. Google Antigravity wrote and maintained the pure-Python application ([`app_mechanic.py`](app_mechanic.py)), `py2app` bundle configuration ([`setup.py`](setup.py)), code-signing and Apple notarization script ([`build.sh`](build.sh)), and documentation ([`README.md`](README.md), [`NOTES.md`](NOTES.md), [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md)), as well as the companion marketing site and interactive simulator at [`liederdigital/appmechanic.dev`](https://github.com/liederdigital/appmechanic.dev).

## Builder history (newest first)

| Date | Builder | Role | Surface | Model / mode | Contribution | Evidence |
|---|---|---|---|---|---|---|
| 2026-11-02 | Google Antigravity | built, deployed | desktop app | Gemini (Low effort) (shown by the tool) | Releases `v0.6.4` and `v0.6.5`: added per-row `⚠️` Update Error Reporter (`/api/log_error`, `update_errors.json`), keg-only Homebrew & version-manager Node `PATH` auto-discovery (`get_node_bin_dirs()`), `Sort by` Install/Update Type selector and sortable headers, `APP_REBRAND_MAP` (`Superset` → `Paradev`), 1-level `/Applications/<Subfolder>/` scanning + Moth Software Kaju feed check (`Mail Archiver X`), single-integer `Build XXXX` parsing (`Sublime Text`), JetBrains `product-info.json` resolution (`Android Studio`), Mac App Store `_MASReceipt` isolation from Homebrew Cask (`WhatsApp`), `Descript` Electron shell handling, and `COLOPHON.md` | `dc50263` (`v0.6.4`), `d86034a` (`v0.6.5`), `97d235c`, [`app_mechanic.py`](app_mechanic.py), [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) |
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

## Evidence limits

- Followed **COLOPHON.md instructions v1.1.2** (https://colophon.md).
- **Inspected**: Full `git log` (`f4a873e` through `97d235c`), existing [`CREDITS.md`](CREDITS.md), [`README.md`](README.md), [`NOTES.md`](NOTES.md), [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md), and 10 local Google Antigravity session transcripts on the owner's development Mac (`2026-07-28` through `2026-11-02`).
- **Remains Unknown**:
  - The exact model version and reasoning setting for the earliest Google Antigravity session (`2026-07-28` to `2026-08-11`, commits `ae0ac28`..`a2f2a52`), which predates `USER_SETTINGS_CHANGE` model-selection records in Antigravity transcripts.
  - Whether an AI tool assisted with commit `ea79d2d` (`2026-07-27`, committed one day before the first local Antigravity transcript on this computer).
- The commit that created or updated this file can be found with `git log -- COLOPHON.md`.
