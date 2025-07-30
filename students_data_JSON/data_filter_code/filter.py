import pandas as pd
import json
import re

# -------- USER INPUT --------
file_path = input("Enter Excel file path (e.g. studentsData.xlsx): ").strip()
selected_year = input("Enter year to process (I or II): ").strip()  # "I" or "II"

# Determine sheet name based on year
sheet_name = "I st year" if selected_year == "I" else "II year"
sheets = pd.read_excel(file_path, sheet_name=[sheet_name])

def process_sheet(df):
    result = {}
    required_columns = ["Roll No", "Student Name", "Section", "year"]

    # Ensure required columns exist
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""  # Fill missing column with empty string

    # Process rows
    for _, row in df.iterrows():
        roll_no = str(row.get("Roll No", "")).strip()
        if roll_no:  # skip empty roll numbers
            result[roll_no] = {
                "studentName": str(row.get("Student Name", "")).strip(),
                "section": str(row.get("Section", "")).strip(),
                "year": str(row.get("year", "")).strip()  # keep existing year first
            }
    return result

# -------- PROCESS SHEET --------
student_json = process_sheet(sheets[sheet_name])

# -------- STEP 1: UPDATE YEAR --------
update_year = input("Do you want to update the 'year' field? (yes/no): ").strip().lower()
if update_year == "yes":
    new_year = input(f"Enter new year for {selected_year} year students (e.g. 2024): ").strip()
    for details in student_json.values():
        details["year"] = new_year
    print("✅ Year updated successfully!")

# -------- STEP 2: CONVERT SECTION I→II OR II→III --------
update_section = input("Do you want to update sections (I→II, II→III)? (yes/no): ").strip().lower()
if update_section == "yes":
    for details in student_json.values():
        section = details.get("section", "")
        if re.match(r"^I\b", section):
            details["section"] = re.sub(r"^I\b", "II", section)
        elif re.match(r"^II\b", section):
            details["section"] = re.sub(r"^II\b", "III", section)
    print("✅ Sections updated successfully!")

# -------- SAVE JSON --------
output_file = "first_year.json" if selected_year == "I" else "second_year.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(student_json, f, indent=4)

print(f"✅ JSON file '{output_file}' created successfully!")
