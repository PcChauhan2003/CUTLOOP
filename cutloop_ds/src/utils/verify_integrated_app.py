import sys
import os
sys.path.insert(0, r"c:\Users\dhruv\OneDrive\Desktop\ds\CUTLOOP\cutloop-ai")
from app.main import app
print("App routes count:", len(app.routes))
for r in app.routes:
    if hasattr(r, "path") and "ds" in r.path:
        print("  DS Route:", r.path, r.methods if hasattr(r, "methods") else "")
print("Verification complete!")
