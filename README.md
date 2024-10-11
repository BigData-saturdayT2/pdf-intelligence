# pdf-intelligence

Based on the structure from your GitHub repository shown in the screenshot, here’s an updated **README** file that aligns with your project:

---

# Assignment 2: PDF Extractor with IBM Watson and FastAPI Integration

## Project Overview
This repository contains the implementation of **Assignment 2**: a PDF extraction and query tool, which automates the extraction of data from PDF files using PyPDF2 and IBM Watson Discovery API. The system is designed to allow users to securely interact with the extracted data through a client-facing application built with **Streamlit** and **FastAPI**. Apache Airflow orchestrates the data pipelines for efficient automation.

## Live Application Links
- **Deployed Application**: [Streamlit App Link]
- **Google Codelabs**: [[code labs](https://codelabs-preview.appspot.com/?file_id=11XVdlzZ8DJotFKU9-hZb4OrUASjitlK7xsWqiVxxNzg#0)]
- **GitHub Repository**: [[GitHub Repo Link](https://github.com/BigData-saturdayT2/pdf-intelligence)]

## Problem Statement
The primary goal is to automate the extraction and processing of text from PDF files, making it easily accessible for querying and analysis. The project reduces the need for manual data extraction, enhancing efficiency and user interaction.

## Project Goals
- **Automated Text Extraction**: Implement extraction pipelines using PyPDF2 (open-source) and IBM Watson (enterprise) tools.
- **User Authentication**: Secure user access with FastAPI and JWT authentication.
- **Data Storage**: Store extracted text in AWS S3 and RDS for structured queries.
- **User Interface**: Build a Streamlit-based interface to allow users to interact with the extracted data.
- **Deployment**: Use Docker Compose to containerize the application for deployment.

## Technologies Used
- **Apache Airflow**: Orchestrates the ETL pipeline for PDF processing.
- **IBM Watson Discovery**: Extracts structured data from PDFs.
- **AWS S3 & RDS**: Stores both raw and processed data.
- **FastAPI**: Manages user authentication and backend logic.
- **Streamlit**: Provides the frontend interface for data querying and interaction.
- **Docker**: Containerizes and deploys the system.
- **PyPDF2**: Performs open-source PDF text extraction.

## Repository Structure
```
├── Streamlit/                          # Streamlit application for frontend UI
├── fastapi/                            # FastAPI backend for user management and API services
├── images/                             # Project images and architecture diagrams
├── pipelines/                          # Airflow pipelines for PDF processing (PyPDF2 & IBM Watson)
├── .gitignore                          # Git ignore file
├── LICENSE                             # License information
├── README.md                           # Project documentation file
├── airflow_etl.ipynb                   # Jupyter notebook for ETL pipeline walkthrough
├── requirements.txt                    # Dependencies required for the project
└── s3_hf_gaia_data.py                  # Script for handling S3 data transfers
```

## Instructions for Running Locally
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```
2. **Create a virtual environment**:
   ```bash
   python -m venv myenv
   source myenv/bin/activate
   ```
3. **Install the requirements**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Streamlit application**:
   ```bash
   streamlit run Streamlit/dashboard.py
   ```

## Deployment
The application is containerized using Docker Compose. Run the following command to deploy:
```bash
docker-compose up
```

## Documentation
- **Codelabs**: [[Codelabs](https://codelabs-preview.appspot.com/?file_id=11XVdlzZ8DJotFKU9-hZb4OrUASjitlK7xsWqiVxxNzg#0)]
- **Video Walkthrough**: [Video Link]

## Contribution
All team members contributed equally to this project. We attest that no external work was used.

| Name     | Work Done                                                                                           |
|----------|-----------------------------------------------------------------------------------------------------|
| Abhinav  | Worked on Airflow pipelining, open-source data extraction, IBM extraction, Docker-Compose setup, S3 configurations and data loading |
| Dheer    | Worked on IBM extraction, RDS table creation, S3 text file data extraction to RDS, documentation                 |
| Nishita  | Worked on architecture diagram creation, FastAPI, Streamlit and openai integration, RDS configurations and CSV loading, documentation |



--- 

This updated README should reflect the structure shown in your screenshot. Let me know if you need any adjustments!
