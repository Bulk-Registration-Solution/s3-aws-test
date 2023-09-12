import json
import boto3
import botocore

class S3Uploader:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        
        self.aws_access_key_id = config["aws_access_key_id"]
        self.aws_secret_access_key = config["aws_secret_access_key"]
        self.file_path = config["upload_file"]
        self.bucket_name = config["bucket_name"]
        self.destination_key = config["destination_key"]
        self.s3 = self._s3_connection(self.aws_access_key_id, self.aws_secret_access_key)

        if not self.s3:
            raise Exception("Unable to establish connection with S3.")

    def _s3_connection(self, access_key, secret_key):
        try:
            s3 = boto3.client(
                service_name="s3",
                region_name="us-east-2",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
        except Exception as e:
            print(e)
            return None
        else:
            print("s3 bucket connected!")
            return s3

    def upload_file(self):
        try:
            self.s3.upload_file(self.file_path, self.bucket_name, self.destination_key)

            # Generate uploaded file's URL
            s3_url = self.s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': self.bucket_name, 'Key': self.destination_key},
                ExpiresIn=3600  # URL expiration time (in seconds)
            )
            print("File uploaded successfully.")
            print("File URL:", s3_url)
            return s3_url

        except botocore.exceptions.ClientError as e:
            print("Error uploading file:", e.response["Error"]["Message"])
            return None

def main():
    try:
        uploader = S3Uploader()
        uploader.upload_file()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
