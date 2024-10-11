import boto3
import pandas as pd
import mysql.connector
from io import StringIO

s3_bucket_name = "textextractionfrompdf"
s3_folder = "GAIA-Dataset/"
s3_csv_file = "gaia_test_dataset"
s3_key = s3_folder + s3_csv_file

# AWS Credentials
aws_access_key_id = "AKIAXAJL2BESDJ3GUI5V"
aws_secret_access_key = "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"

# Amazon RDS Configuration
rds_endpoint = "database-1.cb4iuicksa3s.us-east-2.rds.amazonaws.com"
db_user = "admin"
db_password = "damg7245bigdata"
db_name = "textextraction"
table_name = 'test_dataset'

# Step 1: Read the CSV file from S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-2'
)

response = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_key)
csv_content = response['Body'].read().decode('utf-8')

# Step 2: Convert CSV content to DataFrame
csv_data = pd.read_csv(StringIO(csv_content))

# Print initial row count for reference
print(f"Total rows in original DataFrame: {csv_data.shape[0]}")

# Step 3: Replace NaN values with None (for MySQL NULL compatibility)
csv_data = csv_data.where(pd.notnull(csv_data), None)

# Print to check the number of rows with NaN replaced
print(f"Number of rows after replacing NaN with None: {csv_data.shape[0]}")

# Step 4: Rename DataFrame Columns to Match Table Schema
csv_data.columns = ['task_id', 'Question', 'Level', 'final_answer', 'file_name', 'file_path', 'annotator_metadata']

# Step 5: Establish a connection to the RDS instance
db_connection = mysql.connector.connect(
    host=rds_endpoint,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = db_connection.cursor()

# Step 6: Insert data into the MySQL table
# Wrap each column name in backticks in case of special characters or reserved keywords
columns = ', '.join([f'`{col}`' for col in csv_data.columns])  
placeholders = ', '.join(['%s'] * len(csv_data.columns))

# Prepare the SQL INSERT statement
insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

# Create a list of tuples for the SQL INSERT statement
records = [tuple(row) for row in csv_data.values]

# Execute the INSERT statement row-by-row to catch errors
total_inserted = 0
failed_inserts = 0

for record in records:
    try:
        cursor.execute(insert_query, record)
        total_inserted += 1
    except mysql.connector.Error as err:
        print(f"Failed to insert record: {record}\nError: {err}")
        failed_inserts += 1

# Commit the successful transactions
db_connection.commit()
print(f"Successfully inserted {total_inserted} records out of {len(records)}.")
print(f"Number of failed inserts: {failed_inserts}")

# Step 7: Close the connection
cursor.close()
db_connection.close()
