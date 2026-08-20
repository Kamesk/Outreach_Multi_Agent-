def test_core_imports():
    from config import settings
    from src.orchestrator.agent import run
    from src.agents.calendar.agent import run as calendar_run
    from src.agents.posting.agent import run as posting_run
    from src.agents.ingestion.agent import run as ingestion_run
