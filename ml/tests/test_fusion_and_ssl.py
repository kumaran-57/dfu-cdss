"""
Multimodal clinical fusion and SSL representation benchmark tests.
"""

import numpy as np
from ml.models.fusion.clinical_fusion import (
    MultimodalClinicalFusion,
    run_multimodal_comparison,
)
from ml.models.encoders.ssl_adapters import (
    MockOrPretrainedSSLEncoder,
    run_ssl_linear_probe,
)

def test_multimodal_fusion_ablation():
    np.random.seed(42)
    n_train, n_test = 80, 20
    
    # Synthetic image features (area, Feret dims, tissue %)
    img_train = np.random.uniform(1.0, 15.0, (n_train, 6))
    img_test = np.random.uniform(1.0, 15.0, (n_test, 6))

    # Synthetic clinical features (age, hba1c, neuropathy, etc.)
    clin_train = np.random.uniform(0.0, 10.0, (n_train, 7))
    clin_test = np.random.uniform(0.0, 10.0, (n_test, 7))

    # Binary labels (e.g. stalled vs healed)
    y_train = np.random.randint(0, 2, n_train)
    y_test = np.random.randint(0, 2, n_test)

    results = run_multimodal_comparison(
        img_train, clin_train, y_train,
        img_test, clin_test, y_test,
    )

    assert "image_only" in results
    assert "clinical_only" in results
    assert "fused_multimodal" in results
    assert "roc_auc" in results["fused_multimodal"]
    assert "brier_score" in results["fused_multimodal"]

def test_ssl_encoder_feature_extraction_and_probing():
    encoder = MockOrPretrainedSSLEncoder("dinov2_mock", embedding_dim=128)
    
    train_imgs = np.random.randint(0, 255, (20, 64, 64, 3), dtype=np.uint8)
    train_labels = np.array([0, 1] * 10)
    test_imgs = np.random.randint(0, 255, (10, 64, 64, 3), dtype=np.uint8)
    test_labels = np.array([0, 1] * 5)

    res = run_ssl_linear_probe(encoder, train_imgs, train_labels, test_imgs, test_labels)

    assert res["encoder"] == "dinov2_mock"
    assert res["embedding_dim"] == 128
    assert "macro_f1" in res
    assert 0.0 <= res["macro_f1"] <= 1.0
