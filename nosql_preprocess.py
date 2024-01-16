from google.cloud import bigtable
from google.cloud import storage
import pandas as pd
from io import BytesIO

# Constants
PROJECT_ID = 'fa23-i535-judonato-project'
BIGTABLE_INSTANCE_ID = 'i5353-donato'
BIGTABLE_TABLE_ID = 'developing_nations_data'
BUCKET_NAME = 'fa23-i535-donato'
FILE_NAME = 'World_Data.csv'

# Authenticate to GCP
# GCP credentials are in a JSON file and the environment variable
# export GOOGLE_APPLICATION_CREDENTIALS='/path/to/credentials.json'

# Initialize Bigtable client
client = bigtable.Client(project=PROJECT_ID, admin=True)
instance = client.instance(BIGTABLE_INSTANCE_ID)
table = instance.table(BIGTABLE_TABLE_ID)

# Initialize Cloud Storage client
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob(FILE_NAME)

# Read the dataset into a pandas DataFrame
content = blob.download_as_string()
df = pd.read_csv(BytesIO(content))

# Function to create the row key
def create_row_key(country_code, series_code, year):
    return f"{country_code}#{series_code}#{year}".encode()

# Function to preprocess and format the DataFrame for Bigtable
def preprocess_data(df):
    preprocessed_data = []
    
    # Define the years to process
    years = [str(year) for year in range(2012, 2023)]
    
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract metadata
        series_name = row['Series Name']
        series_code = row['Series Code']
        country_name = row['Country Name']
        country_code = row['Country Code']
        
        # Process each year
        for year in years:
            year_column = f'{year} [YR{year}]'
            if year_column in row and pd.notnull(row[year_column]):
                # Construct the row key
                row_key = create_row_key(country_code, series_code, year)
                
                # Dictionary for the row's data
                data = {
                    'row_key': row_key,
                    'metadata': {
                        'SeriesName': series_name,
                        'CountryName': country_name
                    },
                    'metrics': {
                        series_code: row[year_column]
                    }
                }
                preprocessed_data.append(data)
    
    return preprocessed_data

# Connect to Bigtable and prepare the data for insertion
def write_to_bigtable(preprocessed_data, table):
    # Ensure the table exists and create if not
    if not table.exists():
        raise ValueError("Table does not exist. Please create the table before proceeding.")

    # Insert rows into Bigtable
    rows = []
    for data in preprocessed_data:
        row_key = data['row_key']
        bt_row = table.direct_row(row_key)
        
        # Set metadata columns
        for qualifier, value in data['metadata'].items():
            bt_row.set_cell('metadata',
                            qualifier.encode(),
                            value.encode(),
                            timestamp=None)

        # Set metrics columns
        for qualifier, value in data['metrics'].items():
            # Assume all metrics are floats, modify if not the case
            bt_row.set_cell('metrics',
                            qualifier.encode(),
                            str(value).encode(),
                            timestamp=None)
        rows.append(bt_row)

    # Sending the data to Bigtable
    statuses = table.mutate_rows(rows)
    for status in statuses:
        if status.code != 0:
            print(f'Failed to insert row: {status}')

# Process the DataFrame
preprocessed_data = preprocess_data(df)

# Write the processed data to Bigtable
write_to_bigtable(preprocessed_data, table)
