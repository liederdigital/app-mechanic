#!/bin/bash
set -e
source .venv/bin/activate
rm -rf build dist || true
mkdir dist || true
python3 setup.py py2app

find "dist/App Mechanic.app" -type f \( -name "*.dylib" -o -name "*.so" \) -exec codesign --force --verify --verbose --sign "Developer ID Application: Lieder Digital, LLC (W6YRSA9Z5F)" --options runtime --timestamp {} \;
find "dist/App Mechanic.app" -type d -name "*.framework" -exec codesign --force --verify --verbose --sign "Developer ID Application: Lieder Digital, LLC (W6YRSA9Z5F)" --options runtime --timestamp {} \;
find "dist/App Mechanic.app/Contents/MacOS" -type f -not -name "App Mechanic" -exec codesign --force --verify --verbose --sign "Developer ID Application: Lieder Digital, LLC (W6YRSA9Z5F)" --options runtime --timestamp {} \;

codesign --force --verify --verbose --sign "Developer ID Application: Lieder Digital, LLC (W6YRSA9Z5F)" --options runtime --timestamp "dist/App Mechanic.app"

cd dist
ditto -c -k --keepParent --norsrc "App Mechanic.app" "AppMechanic-Submit.zip"
cd ..

xcrun notarytool submit dist/AppMechanic-Submit.zip --apple-id "it@liederdigital.com" --password "zhal-qcyl-zicm-cgqb" --team-id "W6YRSA9Z5F" --wait

xcrun stapler staple "dist/App Mechanic.app"
cd dist
ditto -c -k --keepParent --norsrc "App Mechanic.app" "AppMechanic-v0.4.0-Signed.zip"
cd ..
