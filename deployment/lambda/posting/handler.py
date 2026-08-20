from src.agents.posting.agent import run

def lambda_handler(event, context): return run(event)
