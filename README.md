# Web Map Inventory Script

## Overview

This script is designed to create a relational CSV file that shows the dependencies between web maps and map/feature services. It connects to multiple ArcGIS Online organizations, retrieves web map information, and generates backup JSON files for each web map. Additionally, it produces CSV reports detailing the dependencies and any discrepancies found.

## Features

- Connects to multiple ArcGIS Online organizations.
- Retrieves all web maps from the specified organizations.
- Creates JSON backup files for each web map.
- Generates CSV files showing web map dependencies.
- Identifies and reports discrepancies between web maps and their dependencies.

## Requirements

- Python
- ArcGIS API for Python
- pandas library

## Installation

1. Ensure you have Python installed on your system.

2. Install the required libraries:

   ```bash
   pip install arcgis pandas
   ```

## Usage

1. Modify the script to include your ArcGIS Online organization URLs and login credentials:

   ```python
   codema = r'https://org1.maps.arcgis.com'
   maUN = 'admin1'
   maPW = 'password'
   aa = r'https://org2.maps.arcgis.com'
   aaUN = 'admin2'
   aaPW = 'password'
   ```

2. Run the script:

   ```bash
   python c_WebMapInventory.py
   ```

## Script Details

- **Organizations Setup:** The script sets up a dictionary of organization URLs with their corresponding usernames, passwords, and abbreviations.
- **Web Map Retrieval:** For each organization, the script logs in and retrieves up to 10,000 web maps.
- **Backup Creation:** It creates a JSON backup file for each web map in a shared directory.
- **Dependency Analysis:** The script analyzes each web map to identify operational layers and other dependencies, storing this information in CSV files.
- **Discrepancy Reporting:** It generates CSV files highlighting web maps with missing dependencies or other discrepancies.

## Output

The script produces the following files in the specified shared directory:

- `Organization_webMapDependencies.csv`: Detailed dependency information for each organization's web maps.
- `Organization_maps.csv`: List of all web maps for each organization.
- `Organization_missingDependencies.csv`: List of web maps with missing dependencies for each organization.
- `master_webMap.csv`: Consolidated list of all web maps across all organizations.
- `master_webMapDependencies.csv`: Consolidated dependency information across all organizations.
- `master_missingDependencies.csv`: Consolidated list of web maps with missing dependencies across all organizations.

## License

This script is provided "as-is" without any warranty. Use at your own risk.
