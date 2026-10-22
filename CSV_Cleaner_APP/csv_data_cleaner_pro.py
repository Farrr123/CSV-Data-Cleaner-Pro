import csv
import os
import platform
import subprocess
import tkinter as tk
from collections import Counter
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


APP_NAME = "CSV Data Cleaner Pro"
APP_VERSION = "3.0"
BG = "#171923"
PANEL = "#222637"
PANEL_ALT = "#292f43"
TEXT = "#f4f6fb"
MUTED = "#aab2c5"
ACCENT = "#6485f5"
SUCCESS = "#22c995"
WARNING = "#f2b84b"
DANGER = "#ff657a"


class CSVDataCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} | v{APP_VERSION}")
        self.root.geometry("820x700")
        self.root.minsize(720, 620)
        self.root.configure(bg=BG)

        self.input_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready. Choose a CSV file to get started.")
        self.summary_text = tk.StringVar(value="No file processed yet.")

        self._configure_styles()
        self._build_ui()

    def _configure_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Cleaner.Horizontal.TProgressbar",
            troughcolor=PANEL_ALT,
            background=SUCCESS,
            bordercolor=PANEL_ALT,
            lightcolor=SUCCESS,
            darkcolor=SUCCESS,
        )
        style.configure(
            "Cleaner.Treeview",
            background=PANEL,
            foreground=TEXT,
            fieldbackground=PANEL,
            rowheight=28,
            borderwidth=0,
        )
        style.configure(
            "Cleaner.Treeview.Heading",
            background=PANEL_ALT,
            foreground=TEXT,
            relief="flat",
            font=("TkDefaultFont", 10, "bold"),
        )
        style.map(
            "Cleaner.Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", "#ffffff")],
        )

    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill=tk.X, padx=28, pady=(24, 14))

        tk.Label(
            header,
            text="CSV DATA CLEANER PRO",
            font=("TkDefaultFont", 21, "bold"),
            bg=BG,
            fg=TEXT,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Clean messy data, remove duplicates, and generate a clear audit report.",
            font=("TkDefaultFont", 10),
            bg=BG,
            fg=MUTED,
        ).pack(anchor="w", pady=(5, 0))

        file_card = self._card(self.root)
        file_card.pack(fill=tk.X, padx=28, pady=8)

        tk.Label(
            file_card, text="INPUT FILE", font=("TkDefaultFont", 9, "bold"),
            bg=PANEL, fg=MUTED
        ).pack(anchor="w", padx=18, pady=(16, 6))

        file_row = tk.Frame(file_card, bg=PANEL)
        file_row.pack(fill=tk.X, padx=18, pady=(0, 12))

        self.file_entry = tk.Entry(
            file_row, textvariable=self.input_path, state="readonly",
            readonlybackground=PANEL_ALT, fg=TEXT, insertbackground=TEXT,
            relief=tk.FLAT, font=("TkDefaultFont", 10)
        )
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=9)

        self._button(file_row, "Browse CSV", self.browse_file, ACCENT).pack(
            side=tk.LEFT, padx=(10, 0)
        )

        tk.Label(
            file_card, text="OUTPUT FOLDER", font=("TkDefaultFont", 9, "bold"),
            bg=PANEL, fg=MUTED
        ).pack(anchor="w", padx=18, pady=(4, 6))

        output_row = tk.Frame(file_card, bg=PANEL)
        output_row.pack(fill=tk.X, padx=18, pady=(0, 17))

        self.output_entry = tk.Entry(
            output_row, textvariable=self.output_dir, state="readonly",
            readonlybackground=PANEL_ALT, fg=TEXT, insertbackground=TEXT,
            relief=tk.FLAT, font=("TkDefaultFont", 10)
        )
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=9)

        self._button(output_row, "Choose Folder", self.choose_output_folder, PANEL_ALT).pack(
            side=tk.LEFT, padx=(10, 0)
        )

        options_card = self._card(self.root)
        options_card.pack(fill=tk.X, padx=28, pady=8)

        tk.Label(
            options_card, text="CLEANING OPTIONS", font=("TkDefaultFont", 9, "bold"),
            bg=PANEL, fg=MUTED
        ).pack(anchor="w", padx=18, pady=(14, 8))

        self.remove_duplicates = tk.BooleanVar(value=True)
        self.normalize_text = tk.BooleanVar(value=True)
        self.validate_email = tk.BooleanVar(value=True)
        self.validate_salary = tk.BooleanVar(value=True)

        options_row = tk.Frame(options_card, bg=PANEL)
        options_row.pack(fill=tk.X, padx=14, pady=(0, 14))

        for label, variable in (
            ("Remove duplicate names", self.remove_duplicates),
            ("Trim whitespace", self.normalize_text),
            ("Check email format", self.validate_email),
            ("Check salary values", self.validate_salary),
        ):
            tk.Checkbutton(
                options_row,
                text=label,
                variable=variable,
                bg=PANEL,
                fg=TEXT,
                activebackground=PANEL,
                activeforeground=TEXT,
                selectcolor=PANEL_ALT,
                font=("TkDefaultFont", 9),
                cursor="hand2",
            ).pack(side=tk.LEFT, padx=5, anchor="w")

        action_row = tk.Frame(self.root, bg=BG)
        action_row.pack(fill=tk.X, padx=28, pady=(10, 8))

        self.clean_button = self._button(
            action_row, "Run Data Cleaning", self.start_cleaning, SUCCESS,
            foreground="#10251e"
        )
        self.clean_button.pack(side=tk.LEFT)

        self.open_button = self._button(
            action_row, "Open Output Folder", self.open_output_folder, PANEL_ALT
        )
        self.open_button.pack(side=tk.LEFT, padx=(10, 0))

        self.progress = ttk.Progressbar(
            self.root, style="Cleaner.Horizontal.TProgressbar",
            orient="horizontal", mode="determinate", maximum=100
        )
        self.progress.pack(fill=tk.X, padx=28, pady=(8, 4))

        results_card = self._card(self.root)
        results_card.pack(fill=tk.BOTH, expand=True, padx=28, pady=8)

        tk.Label(
            results_card, text="RUN SUMMARY", font=("TkDefaultFont", 9, "bold"),
            bg=PANEL, fg=MUTED
        ).pack(anchor="w", padx=18, pady=(13, 4))

        tk.Label(
            results_card, textvariable=self.summary_text, justify=tk.LEFT,
            anchor="w", wraplength=720, bg=PANEL, fg=TEXT,
            font=("TkDefaultFont", 10)
        ).pack(fill=tk.X, padx=18, pady=(0, 12))

        tk.Label(
            self.root, textvariable=self.status_text, anchor="w",
            bg=BG, fg=MUTED, font=("TkDefaultFont", 9)
        ).pack(fill=tk.X, padx=28, pady=(4, 14))

    @staticmethod
    def _card(parent):
        return tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground="#30374d")

    @staticmethod
    def _button(parent, text, command, background, foreground="white"):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=background,
            fg=foreground,
            activebackground=background,
            activeforeground=foreground,
            relief=tk.FLAT,
            borderwidth=0,
            padx=16,
            pady=10,
            font=("TkDefaultFont", 10, "bold"),
            cursor="hand2",
        )

    def browse_file(self):
        selected = filedialog.askopenfilename(
            title="Select a CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if selected:
            self.input_path.set(selected)
            if not self.output_dir.get():
                self.output_dir.set(str(Path(selected).parent))
            self.status_text.set(f"Selected: {Path(selected).name}")
            self.progress["value"] = 0

    def choose_output_folder(self):
        initial = self.output_dir.get() or str(Path.home())
        selected = filedialog.askdirectory(
            title="Choose output folder", initialdir=initial
        )
        if selected:
            self.output_dir.set(selected)
            self.status_text.set("Output folder updated.")

    @staticmethod
    def _normalized_key(value):
        return (value or "").strip().casefold()

    @staticmethod
    def _find_column(fieldnames, candidates):
        lookup = {
            (name or "").strip().casefold(): name
            for name in fieldnames
            if name is not None
        }
        for candidate in candidates:
            if candidate.casefold() in lookup:
                return lookup[candidate.casefold()]
        return None

    @staticmethod
    def _valid_email(value):
        if not value or value.count("@") != 1:
            return False
        local, domain = value.rsplit("@", 1)
        return bool(local and "." in domain and not domain.startswith(".")
                    and not domain.endswith("."))

    def start_cleaning(self):
        input_name = self.input_path.get()
        if not input_name:
            messagebox.showwarning("No input file", "Please select a CSV file first.")
            return

        source = Path(input_name)
        output_dir = Path(self.output_dir.get() or source.parent)

        if not source.is_file():
            messagebox.showerror("File not found", "The selected input file no longer exists.")
            return

        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            self._set_busy(True)
            self.progress["value"] = 0
            self.status_text.set("Reading CSV file...")
            self.root.update_idletasks()

            # utf-8-sig also handles CSV files exported with a UTF-8 BOM.
            with source.open("r", encoding="utf-8-sig", newline="") as file:
                sample = file.read(8192)
                file.seek(0)
                try:
                    dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
                except csv.Error:
                    dialect = csv.excel
                reader = csv.DictReader(file, dialect=dialect)
                original_fieldnames = reader.fieldnames

                if not original_fieldnames:
                    raise ValueError("The selected CSV file is empty or has no header row.")

                fieldnames = [name.strip() if name else name for name in original_fieldnames]
                raw_rows = list(reader)
                # Normalize header keys too, so headers with extra spaces still work.
                rows = [
                    {
                        (key.strip() if isinstance(key, str) else key): value
                        for key, value in raw_row.items()
                    }
                    for raw_row in raw_rows
                ]

            total_rows = len(rows)
            self.progress["value"] = 15
            self.status_text.set(f"Loaded {total_rows:,} rows. Cleaning data...")
            self.root.update_idletasks()

            name_col = self._find_column(fieldnames, ["name", "full name", "employee name"])
            email_col = self._find_column(fieldnames, ["email", "e-mail", "email address"])
            phone_col = self._find_column(fieldnames, ["phone", "phone number", "telephone"])
            salary_col = self._find_column(fieldnames, ["salary", "wage", "annual salary"])
            dept_col = self._find_column(fieldnames, ["department", "dept"])
            city_col = self._find_column(fieldnames, ["city", "town"])

            seen_names = set()
            cleaned_rows = []
            issues = []
            duplicates_removed = 0
            missing_phones = 0
            invalid_salaries = 0
            invalid_emails = 0
            blank_cells = 0
            rows_changed = 0

            for index, original_row in enumerate(rows, start=1):
                row = dict(original_row)
                before = dict(row)

                # Normalize whitespace while preserving the original column names.
                if self.normalize_text:
                    for key, value in row.items():
                        if isinstance(value, str):
                            trimmed = value.strip()
                            if value and not trimmed:
                                blank_cells += 1
                            row[key] = trimmed

                if self.remove_duplicates and name_col:
                    name_key = self._normalized_key(row.get(name_col))
                    if name_key:
                        if name_key in seen_names:
                            duplicates_removed += 1
                            issues.append(f"Duplicate row {index} removed: {row.get(name_col, '')}")
                            continue
                        seen_names.add(name_key)

                if name_col and row.get(name_col):
                    row[name_col] = row[name_col].title()

                if email_col and row.get(email_col):
                    row[email_col] = row[email_col].lower()
                    if self.validate_email and not self._valid_email(row[email_col]):
                        invalid_emails += 1
                        issues.append(f"Invalid email at row {index}: {row[email_col]}")

                if dept_col and row.get(dept_col):
                    dept = row[dept_col].upper()
                    row[dept_col] = dept if dept in {"IT", "HR", "R&D", "QA"} else row[dept_col].capitalize()

                if city_col and row.get(city_col):
                    row[city_col] = row[city_col].title()

                if phone_col and not row.get(phone_col):
                    missing_phones += 1
                    issues.append(f"Missing phone at row {index}: {row.get(name_col, 'Unknown') if name_col else 'Unknown'}")

                if salary_col and row.get(salary_col) and self.validate_salary:
                    salary = row[salary_col].replace(",", "").replace("$", "").strip()
                    try:
                        amount = float(salary)
                        if amount < 0:
                            raise ValueError
                    except ValueError:
                        invalid_salaries += 1
                        issues.append(f"Invalid salary at row {index}: {row[salary_col]}")

                if row != before:
                    rows_changed += 1
                cleaned_rows.append(row)

                if total_rows:
                    progress = 15 + (index / total_rows) * 65
                    self.progress["value"] = progress
                    if index % 100 == 0:
                        self.status_text.set(f"Cleaning row {index:,} of {total_rows:,}...")
                        self.root.update_idletasks()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_csv = output_dir / f"{source.stem}_cleaned_{timestamp}.csv"
            report_txt = output_dir / f"{source.stem}_report_{timestamp}.txt"

            self.status_text.set("Saving cleaned data and report...")
            self.root.update_idletasks()

            with output_csv.open("w", encoding="utf-8-sig", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(cleaned_rows)

            with report_txt.open("w", encoding="utf-8") as report:
                report.write(f"{APP_NAME} - CLEANING REPORT\n")
                report.write("=" * 48 + "\n")
                report.write(f"Input file: {source}\n")
                report.write(f"Processed at: {datetime.now().isoformat(timespec='seconds')}\n\n")
                report.write(f"Original rows: {total_rows}\n")
                report.write(f"Clean rows: {len(cleaned_rows)}\n")
                report.write(f"Duplicate rows removed: {duplicates_removed}\n")
                report.write(f"Rows changed by normalization: {rows_changed}\n")
                report.write(f"Missing phone values: {missing_phones}\n")
                report.write(f"Invalid email values: {invalid_emails}\n")
                report.write(f"Invalid salary values: {invalid_salaries}\n")
                report.write(f"Blank cells normalized: {blank_cells}\n\n")
                report.write("ISSUES LOG\n")
                report.write("-" * 48 + "\n")
                if issues:
                    for issue in issues:
                        report.write(f"- {issue}\n")
                else:
                    report.write("No issues detected by the enabled checks.\n")

            self.progress["value"] = 100
            self.summary_text.set(
                f"Original rows: {total_rows:,}    |    Clean rows: {len(cleaned_rows):,}\n"
                f"Duplicates removed: {duplicates_removed:,}    |    Rows changed: {rows_changed:,}\n"
                f"Missing phones: {missing_phones:,}    |    Invalid emails: {invalid_emails:,}\n"
                f"Invalid salaries: {invalid_salaries:,}    |    Blank cells normalized: {blank_cells:,}\n\n"
                f"Cleaned CSV: {output_csv.name}\nReport: {report_txt.name}"
            )
            self.status_text.set("Completed successfully.")
            messagebox.showinfo(
                "Cleaning complete",
                "The CSV file was cleaned successfully.\n\n"
                f"Rows kept: {len(cleaned_rows):,}\n"
                f"Duplicates removed: {duplicates_removed:,}\n\n"
                f"Files saved to:\n{output_dir}",
            )

        except (OSError, csv.Error, UnicodeError, ValueError) as error:
            self.progress["value"] = 0
            self.status_text.set("Cleaning failed. See the error message.")
            messagebox.showerror("Could not clean CSV", str(error))
        except Exception as error:
            self.progress["value"] = 0
            self.status_text.set("An unexpected error occurred.")
            messagebox.showerror(
                "Unexpected error",
                f"{error}\n\nIf the issue persists, share this error for debugging.",
            )
        finally:
            self._set_busy(False)

    def _set_busy(self, busy):
        self.clean_button.configure(state=tk.DISABLED if busy else tk.NORMAL)
        self.root.configure(cursor="watch" if busy else "")
        self.root.update_idletasks()

    def open_output_folder(self):
        folder = self.output_dir.get()
        if not folder or not Path(folder).is_dir():
            messagebox.showwarning("Output folder unavailable", "Choose a valid output folder first.")
            return

        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(folder)
            elif system == "Darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
        except OSError as error:
            messagebox.showerror("Could not open folder", str(error))


def main():
    root = tk.Tk()
    CSVDataCleanerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
