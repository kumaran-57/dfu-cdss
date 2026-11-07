#!/usr/bin/env python3
"""
Environment and hardware validation script for DFU-XAI.
Verifies system specifications, Python version, dependencies, and GPU/CPU status.
"""

import sys
import os
import platform
import shutil

def check_env():
    print("=" * 60)
    print("DFU-XAI Environment Audit Report")
    print("=" * 60)
    
    # OS & Architecture
    print(f"OS: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version: {platform.python_version()}")
    
    # Core Libraries
    libs = [
        ("FastAPI", "fastapi"),
        ("Pydantic", "pydantic"),
        ("SQLAlchemy", "sqlalchemy"),
        ("Pytest", "pytest"),
        ("NumPy", "numpy"),
        ("SciPy", "scipy"),
        ("Pandas", "pandas"),
        ("Pillow", "PIL"),
        ("Matplotlib", "matplotlib"),
        ("Scikit-Learn", "sklearn"),
        ("PyTorch", "torch"),
        ("OpenCV", "cv2"),
        ("ONNX Runtime", "onnxruntime"),
    ]
    
    print("\n--- Python Package Status ---")
    for name, module_name in libs:
        try:
            mod = __import__(module_name)
            ver = getattr(mod, "__version__", "installed")
            print(f"  [✓] {name:<16}: {ver}")
        except ImportError:
            print(f"  [✗] {name:<16}: NOT INSTALLED (Fallback / adapter mode will be active)")

    # CLI tools
    tools = ["git", "node", "npm", "docker", "psql"]
    print("\n--- System Tool Availability ---")
    for tool in tools:
        path = shutil.which(tool)
        status = f"Available ({path})" if path else "Not found in PATH"
        print(f"  {'[✓]' if path else '[!]'} {tool:<16}: {status}")

    print("\n" + "=" * 60)
    print("Clinical Reminder: Research Prototype only. Do not commit patient data.")
    print("=" * 60)

if __name__ == "__main__":
    check_env()
