from src.agents.ingestion.agent import run

def lambda_handler(event, context): return run(event)
