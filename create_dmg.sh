#!/bin/bash

rm -rf dmg
mkdir dmg
cp -r dist/optoConfig96.app dmg

readme="dmg/Trouble opening? READ ME!.txt"
cat > "${readme}" << EOF
After dragging optoConfig96 into your Applications directory, you may be shown
a popup with one of these messages:

* "optoConfig96" can't be opened because Apple cannot check it for malicious
  software.
* "optoConfig96" cannot be opened because the developer cannot be verified.

In that case, Control-Click on the optoConfig icon and select "Open". You will
be asked if you are sure you want to open it. Once you confirm this,
optoConfig96 will launch.
You can also go to "System Preferences" > Security & Privacy > General Tab",
and choose "Open Anyway" for optoConfig after having tried to open it once.

You only need to do this when launching optoConfig96 for the first time.
EOF

# Create a .dmg archive from the .app after building
create-dmg \
    --volname "optoConfig" \
    --volicon "optoConfig96/resources/oc96.icns" \
    --window-size 600 300 \
    --icon-size 100 \
    --icon "optoConfig96.app" 100 120 \
    --icon "${readme}" 100 120 \
    --hide-extension "optoConfig96.app" \
    --hide-extension "${readme}" \
    --app-drop-link 500 120 \
    darwin.dmg dist/optoConfig96.app
