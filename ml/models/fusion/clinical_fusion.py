"""
Multimodal Clinical Feature Fusion (Experiment E7).
Compares:
1. Image-only features
2. Clinical-only features
3. Fused multimodal representations
Using Logistic Regression and Gradient Boosting with strict training-only fitting.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, brier_score_loss, f1_score

class MultimodalClinicalFusion:
    """
    Fits and compares Image-only, Clinical-only, and Multimodal Fused classifiers.
    Prevents data leakage by fitting preprocessing scalers exclusively on training splits.
    """

    def __init__(self, model_type: str = "gradient_boosting"):
        self.model_type = model_type
        self.imputer = SimpleImputer(strategy="median")
        self.scaler = StandardScaler()
        
        if model_type == "logistic":
            self.model = LogisticRegression(max_iter=1000, random_state=42)
        else:
            self.model = GradientBoostingClassifier(n_estimators=100, random_state=42)

    def fit_and_evaluate(
        self,
        train_features: np.ndarray,
        train_labels: np.ndarray,
        test_features: np.ndarray,
        test_labels: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Fits on train partition and evaluates on test partition.
        """
        # Fit imputer & scaler on train only
        x_train = self.imputer.fit_transform(train_features)
        x_train = self.scaler.fit_transform(x_train)

        # Transform test using train parameters
        x_test = self.imputer.transform(test_features)
        x_test = self.scaler.transform(x_test)

        # Train classifier
        self.model.fit(x_train, train_labels)

        # Predict
        preds = self.model.predict(x_test)
        probs = self.model.predict_proba(x_test)[:, 1]

        auc = float(roc_auc_score(test_labels, probs)) if len(np.unique(test_labels)) > 1 else 0.5
        brier = float(brier_score_loss(test_labels, probs))
        f1 = float(f1_score(test_labels, preds, average="macro"))

        return {
            "model_type": self.model_type,
            "roc_auc": round(auc, 4),
            "brier_score": round(brier, 4),
            "macro_f1": round(f1, 4),
        }

def run_multimodal_comparison(
    image_feats_train: np.ndarray,
    clinical_feats_train: np.ndarray,
    labels_train: np.ndarray,
    image_feats_test: np.ndarray,
    clinical_feats_test: np.ndarray,
    labels_test: np.ndarray,
) -> Dict[str, Any]:
    """
    Controlled 3-way ablation:
    - Image-only
    - Clinical-only
    - Fused (Image + Clinical concatenated)
    """
    fused_train = np.hstack([image_feats_train, clinical_feats_train])
    fused_test = np.hstack([image_feats_test, clinical_feats_test])

    evaluator_image = MultimodalClinicalFusion(model_type="gradient_boosting")
    evaluator_clinical = MultimodalClinicalFusion(model_type="gradient_boosting")
    evaluator_fused = MultimodalClinicalFusion(model_type="gradient_boosting")

    res_image = evaluator_image.fit_and_evaluate(image_feats_train, labels_train, image_feats_test, labels_test)
    res_clinical = evaluator_clinical.fit_and_evaluate(clinical_feats_train, labels_train, clinical_feats_test, labels_test)
    res_fused = evaluator_fused.fit_and_evaluate(fused_train, labels_train, fused_test, labels_test)

    return {
        "image_only": res_image,
        "clinical_only": res_clinical,
        "fused_multimodal": res_fused,
    }
