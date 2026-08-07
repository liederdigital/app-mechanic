# App Mechanic

![App Mechanic Icon](icon.jpg)

App Mechanic is a sleek, zero-dependency macOS utility written in pure Python that scans your installed applications and compares their versions against Homebrew Casks and the Mac App Store to see if they need updating. 

It serves a beautiful, glassmorphic dark-mode dashboard directly on your local machine so you can see the status of all your apps at a glance.

## Prerequisites & Dependencies
App Mechanic leverages two powerful developer tools behind the scenes to check for updates. To get accurate results, you **must** have these installed:

1. **Homebrew**: Used to check the latest versions of standard apps (Chrome, Spotify, OBS, etc.). Install from [brew.sh](https://brew.sh).
2. **mas (Mac App Store command-line interface)**: Used to check the latest versions of App Store apps. Install via Homebrew: `brew install mas`

*(If you don't have these installed, App Mechanic will still run, but it will silently assume all your apps are up to date!)*

## Features
- Scans `~/Applications` and `/Applications` against Homebrew and Mac App Store versions.
- Beautiful, animated glassmorphic dashboard in your web browser.
- **Scan History Log:** Keeps a persistent record of your last 50 scans so you can track your progress over time.
- Single-instance background server that is light on system resources.

## Installation

As of version 0.2.0, App Mechanic is officially code-signed by Lieder Digital, LLC and Notarized by Apple to ensure it is free of malware. 

1. Download the `AppMechanic.zip` file from the [Releases](https://github.com/liederdigital/app-mechanic/releases) page.
2. Double-click to extract the `.zip`.
3. Drag `App Mechanic.app` into your `/Applications` folder.
4. Double-click it to launch!

## How It Works
App Mechanic behaves like a native single-instance macOS app. When you double-click it, it runs entirely in the background and automatically opens `http://localhost:8000` in your default web browser to show you the dashboard.

If you close the browser tab, the background server continues to run. If you double click the `.app` again, it will simply re-open your browser to the existing dashboard instantly. To completely shut down the background scanner, just click the **Quit** button on the dashboard UI.

## License & Disclaimer
This software is provided under the **MIT License** by Lieder Digital, LLC.

**WARNING:** This software comes with **ABSOLUTELY NO WARRANTIES WHATSOEVER**. While it definitely won't break your computer or delete your emails and passwords, Lieder Digital, LLC is not responsible if it accidentally leaves the back door open and your dog runs away from home. Use at your own risk! See the `LICENSE` file for more details.
