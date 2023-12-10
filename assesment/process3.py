import json
import csv
import os
import argparse

def process_json_files(input_dir, output_file):
    data = []

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, 'r') as json_file:
                try:
                    json_data = json.load(json_file)
                    # Extract relevant data and append to the 'data' list
                    # ...

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {file_path}: {e}")

    # Write the extracted data to a CSV file
    with open(output_file, 'w', newline='') as csv_file:
        fieldnames = ['unit', 'trip_id', 'toll_loc_id_start', 'toll_loc_id_end', 'toll_loc_name_start', 'toll_loc_name_end', 'toll_system_type', 'entry_time', 'exit_time', 'tag_cost', 'cash_cost', 'license_plate_cost']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract toll information from JSON files.")
    parser.add_argument("--to_process", required=True, help="Path to the JSON responses folder.")
    parser.add_argument("--output_file", required=True, help="Path to the output CSV file.")
    args = parser.parse_args()

    process_json_files(args.to_process, args.output_file)
