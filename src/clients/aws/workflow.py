"""DynamoDB conditional state transitions for idempotent outbound effects."""
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError
from config import settings

def _table():
    return boto3.resource("dynamodb", region_name=settings.aws_region).Table(settings.workflow_table_name)

def claim(draft_id: str) -> bool:
    """Claim once; concurrent workers cannot both send the same draft."""
    now = datetime.now(timezone.utc).isoformat()
    try:
        _table().update_item(
            Key={"id": draft_id},
            UpdateExpression="SET #s = :processing, updated_at = :now",
            ConditionExpression="attribute_not_exists(#s) OR #s IN (:approved, :failed)",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":processing": "PROCESSING", ":approved": "APPROVED", ":failed": "FAILED", ":now": now},
        )
        return True
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
            return False
        raise

def finish(draft_id: str, status: str) -> None:
    _table().update_item(
        Key={"id": draft_id},
        UpdateExpression="SET #s = :status, updated_at = :now",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":status": status, ":now": datetime.now(timezone.utc).isoformat()},
    )
