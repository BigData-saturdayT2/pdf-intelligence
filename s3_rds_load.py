import os
import pandas as pd
import boto3
from sqlalchemy import create_engine
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')

# Build connection string
connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

try:
    engine = create_engine(connection_string)
    # Test the connection by executing a simple query
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Connection successful: ", result.fetchone())
except OperationalError as e:
    print(f"Error connecting to the database: {e}")



print("Connection string: ", connection_string)


# load_dotenv()

# aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
# aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# db_user = os.getenv('DB_USER')
# db_password = os.getenv('DB_PASSWORD')
# db_host = os.getenv('DB_HOST')
# db_name = os.getenv('DB_NAME')
# db_port = os.getenv('DB_PORT')

# bucket_name = 'gaia-benchmark-data'
# csv_key_1 = 'gaia-dataset/gaia-test-dataset.csv' 
# csv_key_2 = 'gaia-dataset/gaia-validation-dataset.csv' 

# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
# )

# obj1 = s3_client.get_object(Bucket=bucket_name, Key=csv_key_1)
# csv_data_1 = pd.read_csv(obj1['Body'])

# obj2 = s3_client.get_object(Bucket=bucket_name, Key=csv_key_2)
# csv_data_2 = pd.read_csv(obj2['Body'])

# engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# csv_data_1.to_sql('test', engine, if_exists='replace', index=False)
# csv_data_2.to_sql('validation', engine, if_exists='replace', index=False)

# print("Both CSV files have been uploaded into separate tables successfully!")
