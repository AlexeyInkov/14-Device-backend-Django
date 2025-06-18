import glob
import os
from pathlib import Path

dir_path = Path(__file__).resolve().parent
counter = 0
for dir_pr in ("apps", "config", "templates", "utils"):
    for filepath in glob.glob(
        os.path.join(dir_path, "core", dir_pr, "**"), recursive=True
    ):
        if os.path.isfile(filepath) and (
            filepath.endswith(".py") or filepath.endswith(".html")
        ):
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                print(f"{filepath}: {len(lines)}")
                counter += len(lines)
print("Total lines:", counter)
