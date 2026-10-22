import csv

reports = []
seen_employees = []
cleaned_data = []

original_rows = 0
duplicates_removed = 0
missing_values = 0
invalid_values = 0

with open("employees_messy.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        for key in row:
            row[key] = row[key].strip()
            
        clean_name = row["Name"].lower()
        if clean_name in seen_employees:
            print(row["Name"] + " is a duplicate")
            continue
        seen_employees.append(clean_name)

        print(row)
        
        Name = row["Name"]
        if Name == Name.lower() or Name == Name.upper() or Name == Name.title():
            pass
        else:
            print(Name.title())
                
                
        row["Name"] = row["Name"].title()
        row["Email"] = row["Email"].lower()
        print(row["Email"])
        
        row["Department"] = row["Department"].upper()
        if row["Department"] == "IT" or row["Department"] == "it" or row["Department"] == "It" or row["Department"] == "iT":
            print("IT")
        elif row["Department"] == "HR" or row["Department"] == "hr" or row["Department"] == "Hr" or row["Department"] == "hR":
            print("HR")
        else:
            print(row["Department"].capitalize())
                
        row["City"] = row["City"].title()
 
        if not row["Phone"]:
            missing_values += 1
            reports.append(f"Missing phone: {row['Name']}")
        
        if not row["Salary"].isdigit():
            invalid_values += 1
            reports.append(
                f"Invalid salary: {row['Name']} -> {row['Salary']}"
            )
                
        cleaned_data.append(row)
        
        
#==================================
# Save Cleaned Data in New CSV File
#==================================

with open(
    "employees_clean.csv",
    mode="w",
    encoding="utf-8",
    newline=""
) as file:

    fieldnames = [
        "Name",
        "Email",
        "Phone",
        "Department",
        "Salary",
        "City"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(cleaned_data)
        
    print("cleaned_data saved in employees_cleaned.csv file")
    
#==================================
# Save Reports in New Text File
#==================================
with open(
    "cleaning_report.txt",
    mode="w",
    encoding="utf-8"
) as report_file:

    report_file.write("DATA CLEANING REPORT\n")
    report_file.write("====================\n\n")

    report_file.write(f"Original rows: {original_rows}\n")
    report_file.write(f"Clean rows: {len(cleaned_data)}\n")
    report_file.write(
        f"Duplicates removed: {duplicates_removed}\n"
    )
    report_file.write(
        f"Missing values: {missing_values}\n"
    )
    report_file.write(
        f"Invalid values: {invalid_values}\n\n"
    )

    report_file.write("Issues Found:\n")

    if reports:
        report_file.writelines(f"- {report}\n" for report in reports)
    else:
        report_file.write("- No issues found.\n")
        
print("reports saved in reports.txt file")

#==================================
# Terminal summary
#==================================

print("Cleaning completed!")
print()
print(f"Original rows: {original_rows}")
print(f"Clean rows: {len(cleaned_data)}")
print(f"Duplicates removed: {duplicates_removed}")
print(f"Missing values: {missing_values}")
print(f"Invalid values: {invalid_values}")
print()
print("Output:")
print("employees_clean.csv")
print("cleaning_report.txt")