from src.agents.chat.agent import run

def lambda_handler(event, context): return run(event)
