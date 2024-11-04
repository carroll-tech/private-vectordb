from kubernetes import client, config
import os
import time
from dotenv import load_dotenv

def load_kubernetes_config():
    try:
        config.load_incluster_config()
    except Exception as e:
        print("Exception while loading kubeconfig: %s\n" % e)
        print("Exiting...")
        exit(1)

def main():
    load_dotenv()
    
    load_kubernetes_config()
    
    group = 'objectbucket.io'
    version = 'v1alpha1'
    namespace = os.getenv('BUCKET_NAMESPACE', 'default')
    plural = 'objectbucketclaims'
    name = os.getenv('BUCKET_NAME')
    
    if name == "": raise RuntimeError("'BUCKET_NAME' environment variable not set")
    
    # Create an instance of CustomObjectsApi
    custom_api = client.CustomObjectsApi()
    
    retries = int(os.getenv('RETRY_COUNT', 5))
    interval = int(os.getenv('RETRY_INTERVAL', 15))
    counter = 0
    
    while True:
        bucket_status = None
        # Retrieve the specified CRD object
        try:
            crd_instance = custom_api.get_namespaced_custom_object(
                group=group,
                version=version,
                namespace=namespace,
                plural=plural,
                name=name
            )
            bucket_status = crd_instance["status"]["phase"]
        except client.exceptions.ApiException as e:
            print("Exception when fetching CRD object: %s\n" % e)
            bucket_status = None
            
        print(f"Attempt: {counter} - Status: {bucket_status}")
        
        if bucket_status == "Bound":
            print(f"{name} bucket is ready")
            exit(0)
        elif counter == retries:
            print("Retry count hit without successful status...exiting")
            exit(1)
        else:
            counter += 1
        time.sleep(interval)
            

if __name__ == "__main__":
    main()
