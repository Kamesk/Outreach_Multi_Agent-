from config import Settings
from application.orchestrator import PostOrchestrator


def lambda_handler(event, context):
    """
    Agent-callable entrypoint.
    """
    try:
        Settings.validate()

        prompt_path = event.get("prompt_path", "prompt.yaml")

        orchestrator = PostOrchestrator()
        result = orchestrator.execute(prompt_path)

        return {
            "statusCode": 200,
            "body": result
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }
