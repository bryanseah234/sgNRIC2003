---
description: Initialize the DejaVista system
---

// system-init

## Steps
1. Navigate to the `dejavista` repository root.
2. Install dependencies using `npm install` or `yarn install`.
3. Build the Chrome extension: `npm run build`.
4. Open Google Chrome and navigate to `chrome://extensions/`.
5. Enable "Developer mode" in the top right corner.
6. Click "Load unpacked" and select the `dist` folder generated from the build.
7. Verify the extension is loaded without errors.

## Troubleshooting
- If the build fails, check for missing dependencies or syntax errors in the React components.
- If the extension doesn't load, verify the `manifest.json` is correctly formatted in the `public` folder.