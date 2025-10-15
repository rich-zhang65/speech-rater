import boto3
from botocore.exceptions import ClientError
from app.config import settings
from datetime import datetime
import uuid


class StorageService:
    """Service for handling file storage in AWS S3."""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.S3_BUCKET_NAME
    
    async def upload_audio(self, audio_data: bytes, user_id: str, filename: str) -> str:
        """
        Upload audio file to S3 and return the file key.
        
        Args:
            audio_data: Raw audio file bytes
            user_id: User identifier
            filename: Original filename
            
        Returns:
            S3 object key
        """
        try:
            # Generate unique filename
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            file_extension = filename.split('.')[-1] if '.' in filename else 'wav'
            s3_key = f"audio/{user_id}/{timestamp}_{unique_id}.{file_extension}"
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=audio_data,
                ContentType='audio/wav'
            )
            
            return s3_key
        
        except ClientError as e:
            print(f"Error uploading to S3: {str(e)}")
            raise Exception(f"Failed to upload audio: {str(e)}")
    
    async def get_audio_url(self, s3_key: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for accessing an audio file.
        
        Args:
            s3_key: S3 object key
            expiration: URL expiration time in seconds (default 1 hour)
            
        Returns:
            Presigned URL
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )
            return url
        
        except ClientError as e:
            print(f"Error generating presigned URL: {str(e)}")
            raise Exception(f"Failed to generate URL: {str(e)}")

