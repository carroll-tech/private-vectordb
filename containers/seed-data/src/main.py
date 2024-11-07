import asyncio
import boto3
import os
import lance
import lancedb
from dotenv import load_dotenv

def safe_load_env_var(var_name):
    value = os.getenv(var_name)
    if value is None or value == "":
        raise EnvironmentError(f"The environment variable '{var_name}' is not set.")
    return value

def download_s3_folder(bucket_name, folder_name, local_dir):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    
    # Ensure the local directory exists
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    
    try:
        # Paginate through the S3 objects within the folder
        for page in paginator.paginate(Bucket=bucket_name, Prefix=folder_name):
            for obj in page.get('Contents', []):
                # Define the local path for each file
                s3_key = obj['Key']
                local_path = os.path.join(local_dir, os.path.relpath(s3_key, folder_name))
                
                # Create the directory path if it doesn't exist
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                # Download the file
                print(f"Downloading {s3_key} to {local_path}")
                s3.download_file(bucket_name, s3_key, local_path)
        print("All files downloaded successfully")
        return os.path.abspath(local_dir)
                
    except s3.exceptions.NoSuchBucket:
        print(f"Error: The bucket '{bucket_name}' does not exist.")
        exit(1)
    except s3.exceptions.ClientError as e:
        print(f"Client error: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
        
def load_dataframe_from_lance(path: str):
    try:
        ds = lance.dataset(path)
        return ds.to_table().to_pandas()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
        
async def get_lancedb_client(bucket_name: str, access_key: str, secret_access_key: str, endpoint: str):
    try:
        db = await lancedb.connect_async(
            f"s3://{bucket_name}",
            storage_options={
                "region": "us-east-1",
                "aws_access_key_id": access_key,
                "aws_secret_access_key": secret_access_key,
                "endpoint": endpoint,
                "allow_http": "true"
            }
        )
        print("LanceDB client initialized")
        return db
    except Exception as e:
        print(f"An error occurred while initializing LanceDB client: {e}")
        exit(1)
    
async def create_table(client, table_name, dataframe):
    try:
        print(f"Creating table {table_name}")
        table = await client.create_table(table_name, dataframe)
        print(f"{table_name} created successfully")
        return table
    except Exception as e:
        print(f"An error occurred while creating {table_name}: {e}")
        exit(1)

def main():
    load_dotenv()
    
    # Download example data
    seed_bucket_name = os.getenv("SEED_BUCKET_NAME", "pvdb-lance-seed")
    seed_folder_name = os.getenv("SEED_FOLDER_NAME", "vec_data.lance/")
    seed_local_dir = "./data.lance"
    
    path = download_s3_folder(seed_bucket_name, seed_folder_name, seed_local_dir)
    
    # Load lance data as pandas dataframe
    df = load_dataframe_from_lance(path)
    
    # Get LanceDB client
    bucket_name = safe_load_env_var("BUCKET_NAME")
    bucket_host = safe_load_env_var("BUCKET_HOST")
    bucket_port = safe_load_env_var("BUCKET_PORT")
    bucket_access_key = safe_load_env_var("CEPH_ACCESS_KEY_ID")
    bucket_secret_access_key = safe_load_env_var("CEPH_SECRET_ACCESS_KEY")
    bucket_endpoint = f"http://{bucket_host}:{bucket_port}"
    
    db = asyncio.run(get_lancedb_client(bucket_name, bucket_access_key, bucket_secret_access_key, bucket_endpoint))
    
    # Create table
    table = asyncio.run(create_table(db, "test_table_1", df))
    
    # Query table
    print(asyncio.run(table.query().limit(5).to_arrow()))

if __name__ == "__main__":
    main()