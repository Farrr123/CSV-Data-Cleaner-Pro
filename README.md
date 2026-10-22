# CSV Data Cleaner Pro

An advanced, user-friendly Python desktop application and data processing toolkit designed to clean messy CSV datasets, handle missing values, remove duplicates, normalize text, validate emails and salaries, and generate detailed audit reports.

---

## Project Structure

This repository is structured into three main evolution stages of the project:

1. **`pro/`**: The ultimate GUI desktop application built with Python Tkinter (`CSV Data Cleaner Pro`). Features a modern dark theme, real-time progress bars, custom cleaning options, and automatic report generation.
2. **`standard/`**: The initial command-line / script-based version of the data cleaner (`Real Data Cleaning.py`), showcasing the core foundational logic before scaling up to an advanced GUI tool.
3. **`generator/`**: A mock data generator script (`generate_data.py`) accompanied by sample messy datasets (`employees_messy.csv`) to test and evaluate the cleaning algorithms.

---

## Features (Pro GUI Version)

- **Modern Dark UI**: Sleek desktop interface built using Tkinter with custom professional styling.
- **Smart Column Detection**: Automatically identifies name, email, phone, salary, department, and city columns regardless of casing or header variations.
- **Robust Data Cleaning Pipeline**:
  - Whitespace trimming & blank cell normalization.
  - Case normalization (e.g., Title Case for names/cities, UPPERCASE for departments).
  - Duplicate row detection and removal.
  - Email format validation.
  - Salary value verification and error flagging.
- **Comprehensive Audit Reports**: Automatically generates a timestamped `.txt` summary report alongside the cleaned CSV file.

---

## How to Run

### Requirements
- Python 3.8 or higher.
- Built-in Python standard libraries (`csv`, `tkinter`, `pathlib`, `datetime`, `collections`, `platform`, `subprocess`) — **no external pip packages required!**

### 1. Run the Pro GUI Application
```bash
cd pro
python3 csv_data_cleaner_pro.py
```

### 2. Run the Data Generator
```bash
cd generator
python3 generate_data.py
```

### 3. Run the Standard Version
```bash
cd standard
python3 "Real Data Cleaning.py"
```

## Author
Developed with passion on Pop!_OS Linux. Contributions, issues, and feature requests are welcome!

## License
This project is open-source and available under the MIT License.
