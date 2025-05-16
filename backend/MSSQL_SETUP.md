# Setting up Microsoft SQL Server for this Application

This guide will help you set up Microsoft SQL Server to work with this application.

## Prerequisites

1. Microsoft SQL Server installed (Express edition or higher)
2. SQL Server Management Studio (SSMS) or Azure Data Studio
3. Python 3.7+ installed
4. ODBC Driver for SQL Server

## Installing SQL Server and ODBC Driver

### Windows

1. Download and install [SQL Server Express](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
2. Download and install [SQL Server Management Studio (SSMS)](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms)
3. Download and install the [ODBC Driver for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

### macOS/Linux

1. Use Docker to run SQL Server:
   ```
   docker pull mcr.microsoft.com/mssql/server:2019-latest
   docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrong@Passw0rd" \
      -p 1433:1433 --name sql1 -d mcr.microsoft.com/mssql/server:2019-latest
   ```
2. Install the ODBC Driver:
   - macOS: [Instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server)
   - Linux: [Instructions](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server)

## Database Setup

1. Connect to your SQL Server instance using SSMS or Azure Data Studio
2. Create a new database:
   ```sql
   CREATE DATABASE your_database_name;
   ```
3. Create a login and user:
   ```sql
   CREATE LOGIN your_username WITH PASSWORD = 'your_password';
   USE your_database_name;
   CREATE USER your_username FOR LOGIN your_username;
   ALTER ROLE db_owner ADD MEMBER your_username;
   ```

## Updating Your .env File

Update your .env file with the SQL Server connection string:

```
DATABASE_URL=mssql+pyodbc://username:password@server_name/database_name?driver=ODBC+Driver+17+for+SQL+Server
```

Replace:
- `username` with your SQL Server username
- `password` with your SQL Server password
- `server_name` with your server name (e.g., `localhost` or `localhost\\SQLEXPRESS`)
- `database_name` with your database name

## Creating the Required Tables

Run the following SQL in SSMS or Azure Data Studio to create the necessary tables:

```sql
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(120) NOT NULL UNIQUE,
    username NVARCHAR(80) NOT NULL UNIQUE,
    password_hash NVARCHAR(256) NOT NULL,
    is_admin BIT DEFAULT 0,
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE()
);
```

## Creating an Admin User

You can create an admin user directly in the database using:

```sql
INSERT INTO users (email, username, password_hash, is_admin, created_at, updated_at)
VALUES ('admin@example.com', 'admin', 'your_password_hash', 1, GETUTCDATE(), GETUTCDATE());
```

Or you can run the provided `create_admin.py` script after setting up your database connection.

## Testing Your Connection

After setting everything up, you can run the application to verify that it can connect to the database successfully.

## Troubleshooting

### Common Issues

1. **Connection Errors**: Make sure your server name, username, and password are correct in the connection string.

2. **Driver Issues**: Ensure you've installed the correct ODBC driver and specified it correctly in the connection URL.

3. **Firewall Problems**: Make sure port 1433 (default SQL Server port) is open if connecting to a remote server.

4. **Authentication**: If using Windows authentication, your connection string will look different. Consult the SQLAlchemy documentation for details. 