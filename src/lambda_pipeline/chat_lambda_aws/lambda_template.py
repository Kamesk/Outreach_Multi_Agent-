"""
Lambda Project Template Generator

Creates a modular AWS Lambda project structure with:
- Clean service separation
- Config isolation
- Handler isolation
- CI/CD compatibility
- src-based packaging

Usage:
    python scaffold.py --name calendar_service
"""

import argparse
import logging
from pathlib import Path
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

def build_structure(project_name: str) -> List[str]:
    base = f"src/{project_name}"

    return [
        # CI/CD
        ".github/workflows/.gitkeep",

        # Core package
        f"{base}/__init__.py",
        f"{base}/handler.py",

        # Gaurdrail
        f"{base}/__init__.py",
        f"{base}/guardrails/gaurdrails.py",

        # Config
        f"{base}/config/__init__.py",
        f"{base}/config/settings.py",

        # Services Layer
        f"{base}/services/__init__.py",
        f"{base}/services/auth_service.py",
        f"{base}/services/graph_service.py",
        f"{base}/services/availability_service.py",
        f"{base}/services/notification_service.py",

        # Utils
        f"{base}/utils/__init__.py",
        f"{base}/utils/time_utils.py",
        f"{base}/utils/response.py",
        f"{base}/utils/logger.py",

        #core
        f"{base}/core/slot_engine.py",

        # Tests
        f"tests/test_{project_name}.py",

    ]

def create_files(files: List[str]) -> None:
    for filepath in files:
        path = Path(filepath)

        if path.parent:
            path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.touch()
            logger.info(f"Created: {path}")
        else:
            logger.info(f"Exists: {path}")

def main():
    parser = argparse.ArgumentParser(
        description="AWS Lambda structure"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Project name (e.g. calendar, chat, agent_service)",
    )

    args = parser.parse_args()
    project_name = args.name.lower()

    logger.info(f"Generating Lambda template for: {project_name}")

    files = build_structure(project_name)
    create_files(files)

    logger.info("Project scaffolding complete.")


if __name__ == "__main__":
    main()
