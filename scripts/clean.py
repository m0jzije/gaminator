import csv
import ast

input_file = "Export.csv"
output_file = "Cleaned_Export.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write header
    writer.writerow(["id", "name", "popularity", "positive_review_percentage", "release_date", "price", "tags", "steam_link"])

    for row in reader:
        if len(row) == 8:
            # Try to parse ID as integer
            try:
                int(row[0])
                writer.writerow(row)
            except ValueError:
                print(f"Skipping invalid row: {row}")
        else:
            print(f"Skipping incomplete/malformed row: {row}")