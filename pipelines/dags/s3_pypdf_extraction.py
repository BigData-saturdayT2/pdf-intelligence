from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime
from PyPDF2 import PdfReader
import os
import logging

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 8),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    's3_pdf_processing',
    default_args=default_args,
    description='A DAG to process PDFs from S3',
    schedule_interval='@daily',
)

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Function to list PDF files in both S3 folders
def list_s3_files_combined(**kwargs):
    hook = S3Hook(aws_conn_id='aws_default')
    bucket_name = 'gaia-benchmark-data'
    prefixes = ['2023/test/', '2023/validation/']
    
    pdf_files = []

    for prefix in prefixes:
        logging.info(f"Listing files in bucket: {bucket_name}, prefix: {prefix}")
        all_files = hook.list_keys(bucket_name=bucket_name, prefix=prefix)
        pdf_files.extend([file for file in all_files if file.endswith('.pdf')])

    if not pdf_files:
        logging.warning("No PDF files found.")
    
    ti = kwargs['ti']
    ti.xcom_push(key='pdf_files', value=pdf_files)
    
    return pdf_files

# Function to download and process PDF files
def process_pdf(**kwargs):
    hook = S3Hook(aws_conn_id='aws_default')
    bucket_name = 'gaia-benchmark-data'
    
    # Retrieve the list of PDF files from XCom
    ti = kwargs['ti']
    pdf_files = ti.xcom_pull(task_ids='list_s3_files', key='pdf_files')
    
    if not pdf_files:
        logging.info("No PDF files to process.")
        return
    
    for file_key in pdf_files:
        logging.info(f"Processing file: {file_key}")
        
        try:
            # Download file from S3
            local_path = '/tmp/' + os.path.basename(file_key)
            obj = hook.get_key(file_key, bucket_name=bucket_name)
            obj.download_file(local_path)
            
            # Extract text using PyPDF2
            reader = PdfReader(local_path)
            text_content = ''
            
            for page in reader.pages:
                text_content += page.extract_text() or ''
            
            # Save extracted text back to S3 under a different folder
            output_key = 'extracts/' + os.path.basename(file_key).replace('.pdf', '.txt')
            hook.load_string(text_content, key=output_key, bucket_name=bucket_name, replace=True)
            
            logging.info(f"Successfully processed and uploaded: {output_key}")
            
        except Exception as e:
            logging.error(f"Error processing file {file_key}: {e}")
        finally:
            if os.path.exists(local_path):
                os.remove(local_path)

# Task to list files in S3
list_files_task = PythonOperator(
    task_id='list_s3_files',
    python_callable=list_s3_files_combined,
    dag=dag,
)

# Task to process each PDF file
process_files_task = PythonOperator(
    task_id='process_pdf_files',
    python_callable=process_pdf,
    dag=dag,
)

# Set the task dependencies
list_files_task >> process_files_task
