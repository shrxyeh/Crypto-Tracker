# Cryptocurrency Live Data Tracker
A Python-based system that tracks and analyzes the top 50 cryptocurrencies in real-time.

## Project Structure
```
Crypto_Tracker_Submission/
├── crypto_tracker.py        # Main Python script
├── Analysis_Report.pdf      # Detailed market analysis report
└── README.md               # This file
```

## Features
- Real-time tracking of top 50 cryptocurrencies
- Live-updating Excel dashboard
- Automated market analysis
- Cloud synchronization support

## Requirements
- Python 3.12 or higher
- Microsoft Excel
- Internet connection
- Required Python packages:
  - requests
  - pandas
  - xlwings

## Installation
1. Install required packages:
```bash
pip install requests pandas xlwings
```

2. Clone or download the project files
3. Set up sync (for live sheet sharing)

## Usage
1. Run the tracker:
```bash
python crypto_tracker.py
```

2. Access live data:
- Local Excel file: `crypto_live_data.xlsx`
- Shared link: [Live Cryptocurrency Data](https://docs.google.com/spreadsheets/d/1xVh43WdQ_1TiE5aBx4Ecx9MsXh_se9tPsKTF6HdTmqg/edit?gid=0#gid=0)

## Live Data Access
The Excel sheet is continuously updated and can be accessed at:
[Live Cryptocurrency Tracker](https://docs.google.com/spreadsheets/d/1xVh43WdQ_1TiE5aBx4Ecx9MsXh_se9tPsKTF6HdTmqg/edit?gid=0#gid=0)

## Author
[Shreyash Naik]
[shreyashnaik304@gmail.com]
[shreyashnaik39@gmail.com]
[+91-8669857123]

## Notes
- Data updates every 5 minutes
- Requires active internet connection
- Uses CoinGecko API for market data
