
# CSV Data Cleaner

A Python desktop application for cleaning CSV datasets, removing duplicates, normalizing text, validating emails and salaries, and generating audit reports.

## Project Structure

```text
CSV-Data-Cleaner-Pro/
├── CSV_Cleaner_APP/
│   ├── csv_data_cleaner_pro.py
│   ├── employees_messy.csv
│   └── employees_clean.csv
│
├── CSV_Cleaner_Standard/
│   └── Real Data Cleaning.py
│
├── CSV_Generator/
│   ├── generate_data.py
│   └── employees_messy.csv
│
├── .github/
├── .gitignore
└── README.md
```

## Features

- Clean messy CSV datasets.
- Remove duplicate rows.
- Normalize whitespace and text.
- Detect and validate email addresses.
- Validate salary values.
- Generate cleaned CSV files.
- Create audit reports.
- Desktop GUI built with Python Tkinter.

## Requirements

- Python 3.8 or higher.
- Tkinter (usually included with Python).
- No external Python packages required.

## How to Run

### 1. Desktop Application (GUI)

```bash
cd CSV_Cleaner_APP
python3 csv_data_cleaner_pro.py
```

### 2. CSV Data Generator

```bash
cd CSV_Generator
python3 generate_data.py
```

### 3. Standard Version

```bash
cd CSV_Cleaner_Standard
python3 "Real Data Cleaning.py"
```

## Author

Developed with Python on Pop!_OS Linux.

Contributions, issues, and suggestions are welcome.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.