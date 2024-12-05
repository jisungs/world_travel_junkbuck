import os
from django.db import models
from django.utils import timezone

# Create your models here.


def photo_upload_path(instance, filename):
    """
    Generate a unique upload path for photos based on creation date
    
    Args:
        instance (PhotoMetadata): The model instance
        filename (str): Original filename of the uploaded image
    
    Returns:
        str: A path where the photo will be saved
    """
    # Use the photo's created date to create a folder structure
    date = instance.created_at.strftime("%Y/%m/%d")
    
    # Generate a unique filename to prevent overwriting
    # Combines timestamp and original filename
    unique_filename = f"{instance.created_at.strftime('%Y%m%d_%H%M%S')}_{filename}"
    
    # Construct the full path
    return os.path.join('media', date, unique_filename)

class PhotoMetadata(models.Model):
    """
    Model to store detailed information about photos
    """
    name = models.CharField(
        max_length=255, 
        verbose_name="Photo Name",
        help_text="이 사진의 이름을 입력해주세요."
    )
    memo = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Photo Description",
        help_text="이 사진과 관련된 기억을 기록해 보세요"
    )
    created_at = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Creation Timestamp",
        help_text="사진을 찍은 날짜는 어떨게 되나요?"
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True, 
        verbose_name="Latitude",
        help_text="GPS Latitude coordinate"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True, 
        verbose_name="Longitude", 
        help_text="GPS Longitude coordinate"
    )
    # Optional: Photo file upload
    photo_file = models.ImageField(
        upload_to='photos/', 
        blank=True, 
        null=True, 
        verbose_name="Photo File",
        help_text="Actual photo file upload"
    )

    photo_file = models.ImageField(
        upload_to=photo_upload_path, #이 부분의 인스턴스는 django가 자동으로 입력해줌
        blank=True, 
        null=True, 
        verbose_name="Photo File",
        help_text="Actual photo file upload"
    )
    def __str__(self):
        """
        String representation of the photo metadata
        """
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Photo Metadata"
        verbose_name_plural = "Photos Metadata"
        ordering = ['-created_at']