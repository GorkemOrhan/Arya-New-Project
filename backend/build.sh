#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies for pyodbc and MS SQL Server connection
apt-get update
apt-get install -y --no-install-recommends \
    unixodbc \
    unixodbc-dev \
    gnupg \
    curl

# Add Microsoft repository key
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Add Microsoft repository for Debian 11 (Render uses Debian-based images)
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Install Python dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# Make the script executable
chmod +x build.sh 
