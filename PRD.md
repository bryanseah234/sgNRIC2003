# PRD: sgNRIC2003

## Overview
A Python script that generates Code128 barcodes for Singapore NRIC numbers in the 2003-era format (S-prefix and T-prefix). Demonstrates the barcode format used on Singapore identity cards circa 2003. Educational resource showing how ID card barcodes were structured.

## Goals
- Generate Code128 barcodes for NRIC numbers
- Output barcode images (PNG or SVG) per NRIC
- Educational demonstration of 2003 SG ID card barcode format

## Non-Goals
- Generating NRICs (input must be pre-formed valid NRIC strings)
- Checking NRIC validity (no checksum validation here — see validateNRIC2020)
- Any form of identity document forgery

## Tech Stack
- **Language**: Python 3.x
- **Libraries**: `python-barcode` (pip)

## Architecture
```
sgNRIC2003/
├── code/         # Barcode generation scripts
├── output/       # Generated barcode images
└── archive/      # Reference images of 2003 format
```

## Deployment / Run
```bash
pip install python-barcode
python code/<script>.py
```

## Constraints & Notes
- **Educational only**: generating barcodes that appear to replicate government ID documents for any deceptive purpose is illegal
- **2003 format**: barcode format on Singapore IDs has changed since 2003; this represents historical format only
- **NRIC input**: requires user to supply NRIC strings — does not generate NRICs itself
