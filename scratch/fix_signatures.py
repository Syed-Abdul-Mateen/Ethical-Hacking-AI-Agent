import os
from pathlib import Path

detectors_root = Path("d:/Projects/Ethical Hacking AI Agent/src/detectors")

TARGET_SIGNATURE = "def run(self, parsed_data: dict) -> list:"
NEW_SIGNATURE = "def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:"

# Necessary imports to add if missing
REQUIRED_IMPORTS = [
    "from typing import List, Dict",
    "from pathlib import Path",
    "from src.detectors.base_detector import BaseDetector, Finding",
    "from src.parsers.base_parser import ParsedFile"
]

for root, dirs, files in os.walk(detectors_root):
    for file in files:
        if file.endswith(".py"):
            file_path = Path(root) / file
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if TARGET_SIGNATURE in content:
                print(f"Fixing {file_path}")
                # 1. Replace signature
                new_content = content.replace(TARGET_SIGNATURE, NEW_SIGNATURE)
                
                # 2. Ensure imports (simplistic approach: add to top if not present)
                lines = new_content.splitlines()
                
                # Check for typing imports
                if "from typing import" not in new_content:
                    lines.insert(0, "from typing import List, Dict, Any, Optional")
                else:
                    # Update existing typing import if it's too narrow
                    for i, line in enumerate(lines):
                        if "from typing import" in line and "Dict" not in line:
                            lines[i] = "from typing import List, Dict, Any, Optional"
                
                # Check for Path import
                if "from pathlib import Path" not in new_content:
                    lines.insert(0, "from pathlib import Path")
                
                # Check for base class imports
                if "from src.detectors.base_detector" not in new_content:
                    lines.insert(5, "from src.detectors.base_detector import BaseDetector, Finding")
                
                if "from src.parsers.base_parser" not in new_content:
                    lines.insert(6, "from src.parsers.base_parser import ParsedFile")
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines) + "\n")
