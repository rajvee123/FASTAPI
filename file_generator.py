import pandas as pd
import pyarrow.parquet as pq
# Create sample data
data = {
    "roll_no": [101, 102, 103],
    "year_of_study": ["1st Year", "2nd Year", "3rd Year"],
    "name": ["Raj", "Sam", "Priya"],
    "major": ["Computer Engg", "Civil Engg", "Mechanical"],
    "year_of_passout": [2028, 2027, 2026],
    "cgpa": [8.5, 7.9, 9.0]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save as Parquet
df.to_parquet("students.parquet", engine="pyarrow")

print("Parquet file 'students.parquet' created successfully!")
