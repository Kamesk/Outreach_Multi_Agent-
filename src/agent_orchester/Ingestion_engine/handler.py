import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from agent_orchester.Ingestion_engine.scripts.ingest_artifacts import process_all_files


def lambda_handler(event, context):

    try:
        source_folder = event.get("source_folder", ".github/artifacts")
        force_reindex = event.get("force_reindex", False)

        # You already have ingest_artifacts.py in scripts/
        # This calls your existing ingestion logic
        process_all_files(folder=source_folder)

        return {
            "statusCode": 200,
            "body": {
                "message": "Ingestion completed successfully",
                "source_folder": source_folder,
                "force_reindex": force_reindex
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
