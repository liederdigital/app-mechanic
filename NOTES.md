# App Mechanic - Project Notes

## What is this project?
App Mechanic is a lightweight, zero-dependency macOS utility written in pure Python standard library. It scans the `/Applications` folder, cross-references installed apps against the Mac App Store and Homebrew Cask databases, and serves a local, glassmorphic HTML dashboard (on localhost:8000) that displays which apps are up-to-date and which are outdated. It features an interactive "Scan Now" button for real-time rescanning.

## Current State
- The repository is currently live at `github.com/liederdigital/app-mechanic`.
- The working tree is clean (committed and pushed).
- The core functionality (scanning, matching against `mas` and Homebrew, serving the UI) is implemented in a single script (`app_mechanic.py`).

## How Version Detection Works
The tool identifies the update status of applications by falling into one of three categories:

1. **Mac App Store (mas) Apps:**
   - **Detection:** It shells out to the `mas outdated` CLI command.
   - **Parsing:** It parses the command's stdout using regex to extract the app name, the installed version, and the latest version.
   - **Matching:** If a local `.app` name matches a name in the `mas outdated` output, it's flagged as outdated.

2. **Homebrew Cask Apps:**
   - **Detection:** It fetches the Homebrew Cask JSON database from `https://formulae.brew.sh/api/cask.json` and maps Cask artifacts to the corresponding local `/Applications` bundle names.
   - **Installed Version:** It reads the `CFBundleShortVersionString` (or fallback to `CFBundleVersion`) from the local app's `Contents/Info.plist`.
   - **Comparison:** It uses a custom `parse_version()` function that extracts the leading dot-separated digits via regex (`^\d+(\.\d+)+`) and converts them into an array of integers (e.g., `[1, 2, 3]`). The integer arrays for the installed version and Homebrew's latest version are then directly compared (`>` operator) to determine if an update is available.

3. **Native / OS / Other Apps:**
   - **Fallback:** If an app is neither in the `mas outdated` list nor matches a Homebrew cask, it simply reports the installed version from `Info.plist` as both installed and latest, marking the app as "Up to Date" by default.

## Known Issues
The simplistic regex-based integer array comparison in `parse_version()` combined with `Info.plist` scraping causes incorrect version reporting for certain standalone apps:
- **Descript:** Reports as `114.0.4` — it is likely reading the bundled Electron framework version rather than the actual Descript app version.
- **Opera:** Version parsing yields format mismatches (e.g., `133.0` vs `133.0.5932.60`), leading to false flags because of the differing number of version segments.
- **OBS:** Comparison bounces between a stable release (`32.1.2`) and a pre-release (`32.2.0`), presumably because the script doesn't correctly handle pre-release or beta suffixes in version strings.

## Next Steps
1. **Fix Version Detection Logic:** Address the known bugs with Descript, Opera, and OBS (improving plist parsing, segment padding for version comparisons, and handling pre-releases).
2. **Packaging:** Bundle the Python script into a native macOS `.app` bundle using `py2app` and/or package it as a standalone, single-file binary using `PyInstaller`.
