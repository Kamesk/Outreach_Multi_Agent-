from config import Settings
from application.posting_orchestrator import PostingOrchestrator
from utils.response import success, failure


def lambda_handler(event, context):
    try:
        Settings.validate()

        orchestrator = PostingOrchestrator(Settings)
        result = orchestrator.execute()

        return success(result)

    except Exception as e:
        return failure(e)
