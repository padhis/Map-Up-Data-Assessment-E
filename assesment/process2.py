import os
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()



# Get TollGuru API key and URL from environment variables
tollguru_api_key = os.getenv("TOLLGURU_API_KEY")
tollguru_api_url = os.getenv("TOLLGURU_API_URL")

def process_csv_file(file_path, output_dir):
    # Build the API endpoint URL
    url = 'https://apis.tollguru.com/toll/v2/gps-tracks-csv-upload?mapProvider=osrm&vehicleType=5AxlesTruck'
    # Set headers with API key and content type
    headers = {'x-api-key': tollguru_api_key, 'Content-Type': 'text/csv'}

    # Get the file name from the path
    file_name = os.path.basename(file_path)

    # Open the CSV file in binary mode
    with open(file_path, 'rb') as file:
        # Send a POST request to the TollGuru API
        response = requests.post(url, data=file, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the JSON response to the output directory with the same file name
            json_output_path = os.path.join(output_dir, f"{file_name}.json")
            with open(json_output_path, 'w') as json_file:
                json_file.write(response.text)
            print(f"Processed: {file_name}")
        else:
            print(f"Error processing {file_name}. Status code: {response.status_code}")

output_dir = 'C:/Users/ADMIN/Downloads/assesment/evaluation data/output/process 2'
file_path = 'C:/Users/ADMIN/Downloads/assesment/evaluation data/output/process 1/1000_0.csv'
process_csv_file(file_path, output_dir)

def process_files_in_directory(directory, output_dir):
    # List all CSV files in the specified directory
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Use ThreadPoolExecutor for concurrent processing
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Process each CSV file concurrently
        executor.map(lambda file: process_csv_file(os.path.join(directory, file), output_dir), csv_files)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process CSV files and interact with the TollGuru API.")
    parser.add_argument("--to_process", required=True, help="Path to the CSV folder.")
    parser.add_argument("--output_dir", required=True, help="The folder where JSON files will be stored.")
    args = parser.parse_args()

    # Process CSV files and interact with the TollGuru API
    process_files_in_directory(args.to_process, args.output_dir)


