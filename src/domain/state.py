from typing import TypedDict, Any

class AgentState(TypedDict, total=False):
    user_id: str
    channel_id: str
    conversation_id: str
    message: str
    intent: str
    response: str
    tool_history: list[str]
    metadata: dict[str, Any]
    timestamp: str
