"""
Image storage service with EXIF metadata stripping and integrity verification.
"""

import os
import io
import hashlib
from typing import Tuple
from PIL import Image as PILImage
from fastapi import HTTPException, status
from backend.app.core.config import settings

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}

def secure_save_image(
    file_bytes: bytes,
    original_filename: str,
    visit_id: str,
) -> Tuple[str, str, int, int, str]:
    """
    Validates, strips all EXIF metadata, computes SHA256, and securely saves the research image.
    Returns: (saved_relative_path, mime_type, width, height, sha256_hash)
    """
    # 1. Size Check
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    # 2. SHA256 Hash
    sha256_hash = hashlib.sha256(file_bytes).hexdigest()

    # 3. Validation and EXIF stripping via PIL
    try:
        with PILImage.open(io.BytesIO(file_bytes)) as pil_img:
            format_name = pil_img.format
            if format_name == "JPEG":
                mime_type = "image/jpeg"
                ext = ".jpg"
            elif format_name == "PNG":
                mime_type = "image/png"
                ext = ".png"
            elif format_name == "WEBP":
                mime_type = "image/webp"
                ext = ".webp"
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported image format: {format_name}. Only JPEG and PNG are permitted.",
                )

            width, height = pil_img.size

            # Create clean copy without EXIF tags
            clean_image = PILImage.new(pil_img.mode, pil_img.size)
            clean_image.paste(pil_img)

            # Ensure upload folder exists
            visit_dir = os.path.join(settings.UPLOAD_DIR, visit_id)
            os.makedirs(visit_dir, exist_ok=True)

            filename = f"{sha256_hash[:16]}{ext}"
            file_path = os.path.join(visit_dir, filename)

            # Save clean image without any EXIF / camera metadata
            if mime_type == "image/jpeg":
                clean_image.save(file_path, "JPEG", quality=95)
            elif mime_type == "image/png":
                clean_image.save(file_path, "PNG", optimize=True)
            else:
                clean_image.save(file_path, "WEBP")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Corrupt or invalid image file: {str(e)}",
        )

    return file_path, mime_type, width, height, sha256_hash
