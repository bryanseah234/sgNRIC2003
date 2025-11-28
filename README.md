# Singapore NRIC 2003

A Python tool to generate, validate, and create barcodes for Singapore NRIC numbers from 2003.

## Description

This project demonstrates how to generate all possible Singapore NRIC (National Registration Identity Card) combinations for the year 2003, validate them using the official checksum algorithm, and generate Code 39 barcodes for each valid NRIC. It serves as an educational tool to highlight potential security vulnerabilities in the NRIC system.

<p align="center">
  <img src="https://github.com/bryanseah234/sgNRIC2003/blob/master/archive/nric2003.JPG" />
</p>

## Features

- Generate all possible NRIC combinations for year 2003 (T03XXXXXZ format, where X = digits, Z = checksum letter)
- Validate NRICs using the official checksum algorithm
- Generate Code 39 barcodes for validated NRICs
- Pre-generated outputs included for convenience

## Technologies Used

- Python 3
- python-barcode (for Code 39 barcode generation)
- ImageWriter (for barcode image output)

## Installation

```bash
# Clone the repository
git clone https://github.com/bryanseah234/sgNRIC2003.git

# Navigate to project directory
cd sgNRIC2003

# Install dependencies
pip install python-barcode
```

## Usage

```bash
# Step 1: Generate all possible NRIC combinations
python "code/01_generate nric2003.py" > "output/nric2003 text/all nric2003.txt"

# Step 2: Validate NRICs by checking their checksum
python "code/02_validate nric2003.py" > "output/nric2003 text/validated nric2003.txt"

# Step 3: Generate barcodes for each validated NRIC
python "code/03_generate barcodes.py"
```

**Note:** Pre-generated outputs from all steps have been uploaded in the `output/` folder for convenience.

### Requirements

**Software:**
- Python 3.x
- python-barcode module

**Hardware:**
- Laptop / Desktop (Windows or macOS)

**Non-tangibles:**
- Time (at least 24 hours for full barcode generation in Step 3)
- Storage space (at least 3GB for barcode images)
- Electricity (be prepared to leave your device running overnight)

## Demo

View the barcode demo video: [archive/nric2003.mp4](archive/nric2003.mp4)

## Disclaimer

1. FOR EDUCATIONAL PURPOSES ONLY
2. USE AT YOUR OWN DISCRETION

The generation of NRIC numbers itself is legal, as the algorithm is made public. This project serves to demonstrate that it is possible to do so. However, you should not use the NRIC numbers to impersonate anyone as it is an offence. By using this repository, you hereby agree to be responsible for your actions and waive all rights to hold the author liable for any problems arising from your actions.

## License

MIT License

---

**Author:** <a href="https://github.com/bryanseah234">bryanseah234</a>
