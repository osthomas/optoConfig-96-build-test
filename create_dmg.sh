#!/bin/sh

# Create a .dmg archive from the .app after building
create-dmg \
    --volname "optoConfig" \
    --volicon "optoConfig96/resources/oc96.icns" \
    --window-size 600 300 \
    --icon-size 100 \
    --icon "optoConfig96.app" 175 120 \
    --hide-extension "optoConfig96.app" \
    --app-drop-link 425 120 \
    darwin.dmg dist/optoConfig96.app
