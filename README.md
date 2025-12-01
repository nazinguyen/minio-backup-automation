# Minio-backup-automation

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![MinIO](https://img.shields.io/badge/MinIO-Object%20Storage-red)
![Docker](https://img.shields.io/badge/Docker-Container-blue)
![Linux](https://img.shields.io/badge/Linux-Crontab-green)

## Overview
This project is an automated backup solution. The system performs simulated data dump, packaging, naming by timestamp (for version management) and uploading to the Object Storage server **MinIO** deployed on Docker.

The process is fully automated using **Linux Crontab**, ensuring data integrity and disaster recovery with zero operating costs.

## Key Features
* **Object Storage:** Use MinIO (S3 compatible) as a centralized storage location.
* **Automated Scheduling:** Automatically run daily backups using Crontab Scheduler.
* **Version Control:** Backup files are named with a timestamp (`backup_YYYY-MM-DD_HH-MM.txt`) to avoid overwriting old data.
* **Security:** Manage Credential (Access Key/Secret Key) via environment variables (`.env`), not hardcoded in scripts.
* **Resource Optimization:** Automatically cleanup local files after successful upload to save hard drive space.

## Architecture

1. **Docker:** Run MinIO Server.

2. **Python Script:**
* Connect to MinIO via `boto3` library.

* Create dummy data (simulate database dump).

* Upload file to Bucket `backup-files`.

3. **Crontab:** Trigger script on a preset schedule (e.g. 02:00 AM every day).

## Project Structure

```bash
minio-docker/
├── .env # Contains sensitive information (Access Key, Secret Key)
├── docker-compose.yml # MinIO deployment configuration
├── README.md # Project documentation
└── scripts/
└── backup_s3.py # Python script to handle backup & upload logic
```

## Installation & Configuration
### 1. Prerequisites
Python 3.x
Docker & Docker Compose
Linux OS (Ubuntu/CentOS...)

### 2. Environment Setup
Create a .env file in the root directory and fill in your MinIO information:

#### Code Snippet
```bash
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
AWS_REGION=us-east-1
S3_ENDPOINT_URL=http://localhost:9000
```

### 3. Install Python Library
```bash
pip install boto3 python-dotenv
```

### 4. Deploy MinIO
```bash
docker-compose up -d
```

### Usage
#### Manual Test
To check if the script works properly:
```bash
python3 scripts/backup_s3.py
```
Result: The script will create a file, upload it to MinIO, and delete the local file. Check it on MinIO Console (http://localhost:9001).


#### Automation with Crontab (Automation)
The system is configured to run automatically at 02:00 every day.

Configuring Crontab (crontab -e):
```bash
0 2 * * * /usr/bin/python3 /path/to/your/project/scripts/backup_s3.py >> /var/log/minio_backup.log 2>&1
```
Log file: /var/log/minio_backup.log (Save the running history for debugging).


## Video demo
https://github.com/user-attachments/assets/36b39201-ec81-4c4e-84e5-756562b23e81


