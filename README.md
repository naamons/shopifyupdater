
# Shopify Price Update Tool

This project contains Python scripts for automating product price updates in a Shopify store, based on external data. It downloads price data from a website, processes it, compares it with Shopify's current prices, updates discrepancies, and generates a change report.

## Features
- **Web Downloader**: Automates login and Excel file download with SKU and price data.
- **Excel Reader**: Processes SKU and price data, applying necessary adjustments.
- **Shopify SKU Check**: Updates Shopify prices based on the processed data.
- **Report Generator**: Summarizes price updates in a CSV report.

## Usage
1. **Configuration**: Fill out `config.ini` with URLs, credentials, and paths.
2. **Execution**: Run `main.py` to start the automated process.

## Requirements
- Python 3.x
- Libraries: `pandas`, `requests`, `configparser`, `csv`

## Setup
Install required libraries:
```
pip install pandas requests configparser
```

## Configuration
- `config.ini`: Central to the tool, contains URLs, credentials, paths, and more. Securely manage this file as it contains sensitive information.

## License
Apache 2.0
