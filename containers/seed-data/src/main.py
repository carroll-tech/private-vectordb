import boto3
import os
import lance
from dotenv import load_dotenv

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

def main():
    load_dotenv()
    
    # Download example data
    bucket_name = os.getenv("SEED_BUCKET_NAME", "pvdb-lance-seed")
    folder_name = os.getenv("SEED_FOLDER_NAME", "vec_data.lance/")
    local_dir = "./data.lance"
    
    path = download_s3_folder(bucket_name, folder_name, local_dir)
    
    # Load lance data as pandas dataframe
    df = load_dataframe_from_lance(path)
    
    print(df.head())
    
    


if __name__ == "__main__":
    main()