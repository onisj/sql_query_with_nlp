import os
import shutil

# Download Database (Chinook MySQL)
sql_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/Mauh_UvY4eK2SkcHj_b8Tw/chinook-mysql.sql'
sql_file = 'data/init.sql'

# Create the data directory if it doesn't exist
os.makedirs(os.path.dirname(sql_file), exist_ok=True)

# If init.sql exists as a directory, remove it
if os.path.isdir(sql_file):
    shutil.rmtree(sql_file)

# Use os.system to download the SQL file
os.system(f"wget {sql_url} -O {sql_file}")

print(f"Downloaded SQL file from {sql_url} and saved as {sql_file}")

# Verify that the file was created and is not a directory
if os.path.isfile(sql_file):
    print(f"{sql_file} is a valid file.")
else:
    print(f"Error: {sql_file} is not a valid file.")
