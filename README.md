# App Mechanic 🔧

A lightweight, zero-dependency macOS utility that scans your local `/Applications` folder, cross-references versions against the **Mac App Store** and **Homebrew Cask** databases, and displays a glassmorphic update dashboard in your browser.

With a single command, see exactly what is outdated on your system, search by app name, and run real-time updates directly from the dashboard.

---

## Features
* **Zero Dependencies:** Written in pure Python 3 using only standard libraries. No `pip install` required!
* **High-Fidelity UI:** A beautiful dark-mode glassmorphic interface with smooth SVG loading and progress circles.
* **Interactive Live Refresh:** Click **Scan Now** to trigger a real-time system scan on demand.
* **Instant Search & Filter:** Filter apps instantly by name, or view only **Outdated** / **Up to Date** apps.
* **Smart Detection:** Compares version metadata across both Mac App Store (`mas`) and Homebrew Cask databases.

---

## How to Install and Run

### 1. Pre-requisites (Recommended)
To enable full scanning of all package sources, make sure you have Homebrew and `mas` CLI installed:
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install mas CLI (for Mac App Store updates)
brew install mas
```

### 2. Run the Tool
Simply clone the repository and run the Python script:
```bash
python3 app_mechanic.py
```
This will start a lightweight local server (defaults to port `8000`) and automatically open the interactive dashboard in your default browser.

---

## Make it a Shortcut Command (`checkapps`)
To check your updates at any time by simply typing `checkapps` in your Terminal:

1. Add the alias to your Shell profile (Zsh):
   ```bash
   echo 'alias checkapps="python3 /Users/ronstauffer/Developer/app-mechanic/app_mechanic.py"' >> ~/.zshrc
   ```
2. Reload your terminal settings:
   ```bash
   source ~/.zshrc
   ```
3. Run it anytime:
   ```bash
   checkapps
   ```

---

## License
Distributed under the **MIT License**. See `LICENSE` for details.
