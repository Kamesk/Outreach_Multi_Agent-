from typing import TypedDict, Optional, List, Dict
class AgentState(TypedDict, total=False):
    user_id: str
    channel_id: str
    conversation_id: str
    message: str
    intent: str
    response: str
    selected_tool: str
    tool_history: List[str]
    metadata: Dict[str, str]
    timestamp: str
