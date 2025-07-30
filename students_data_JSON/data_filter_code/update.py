import json
import re

# Read the JSON file
with open("students_data_JSON/second_year.json", "r") as file:
    data = json.load(file)

# Update sections
for roll_no, details in data.items():
    section = details.get("section", "")
    
    # Replace only at the beginning (I -> II, II -> III)
    if re.match(r"^I\b", section):
        details["section"] = re.sub(r"^I\b", "II", section)
    elif re.match(r"^II\b", section):
        details["section"] = re.sub(r"^II\b", "III", section)

# Write the updated JSON back
with open("students_data_JSON/second_year.json", "w") as file:
    json.dump(data, file, indent=4)

print("✅ Sections updated successfully!")
