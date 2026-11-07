"""
Abstract base class for DFU wound and tissue segmentation models.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
import numpy as np

class BaseSegmentationModel(ABC):
    """
    Standard interface for wound boundary and tissue composition segmentation models.
    """

    def __init__(self, model_name: str, num_classes: int = 1):
        self.model_name = model_name
        self.num_classes = num_classes
        self.is_loaded = False

    @abstractmethod
    def load_weights(self, weights_path: str):
        """Loads model checkpoint weights."""
        pass

    @abstractmethod
    def predict(
        self,
        image_array: np.ndarray,
        return_uncertainty: bool = True,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Runs inference on RGB input image.
        Returns:
            binary_or_multiclass_mask: (H, W) array of predicted class indices
            metadata: dict with pixel_area, tissue percentages, uncertainty_score
        """
        pass
