from setuptools import setup

APP = ['app_mechanic.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'AppMechanic.icns',
    'plist': {
        'CFBundleName': 'App Mechanic',
        'CFBundleDisplayName': 'App Mechanic',
        'CFBundleIdentifier': "com.liederdigital.appmechanic",
        'CFBundleVersion': "0.5.0",
        'CFBundleShortVersionString': "0.5.0",
        'NSHumanReadableCopyright': "Copyright © 2026 Lieder Digital, LLC. All rights reserved.",
        'CFBundleGetInfoString': "App Mechanic - macOS App Updater and Scanner",
        'LSUIElement': True, # Runs in the background (no Dock icon), relying on the web browser for UI
    }
}

setup(
    app=APP,
    name="App Mechanic",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
