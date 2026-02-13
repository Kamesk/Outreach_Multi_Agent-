"""
python scaffold.py --name post_generation
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
    base = project_name  # No src/ prefix — root-level service

    return [
        # Root-level core
        f"{base}/handler.py",
        f"{base}/config.py",
        f"{base}/bootstrap.py",

        # Application Layer
        f"{base}/application/__init__.py",
        f"{base}/application/orchestrator.py",

        # Domain Layer
        f"{base}/domain/__init__.py",
        f"{base}/domain/models.py",

        # Services Layer
        f"{base}/services/__init__.py",
        f"{base}/services/prompt_service.py",
        f"{base}/services/text_generation_service.py",
        f"{base}/services/image_generation_service.py",
        f"{base}/services/metadata_service.py",
        f"{base}/services/excel_service.py",
        f"{base}/services/s3_service.py",

        # Infrastructure Layer
        f"{base}/infra/__init__.py",
        f"{base}/infra/openai_client.py",
        f"{base}/infra/fal_client_wrapper.py",
        f"{base}/infra/aws_client.py",

        # Utilities
        f"{base}/utils/__init__.py",
        f"{base}/utils/file_utils.py",
        f"{base}/utils/logger.py",

        # Watcher (dev mode only)
        f"{base}/watcher/__init__.py",
        f"{base}/watcher/prompt_watcher.py",
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
        description="Post Generation Agent Structure"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Project directory name (e.g. post_generation)",
    )

    args = parser.parse_args()
    project_name = args.name.lower()

    logger.info(f"Generating structure for: {project_name}")

    files = build_structure(project_name)
    create_files(files)

    logger.info("Project scaffolding complete.")


if __name__ == "__main__":
    main()
