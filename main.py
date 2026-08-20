from src.orchestrator.agent import run

def main():
    print('=== Outreach Multi-Agent Controller ===')
    while True:
        message=input('You: ').strip()
        if message.lower() in {'exit','quit'}: break
        try: print('Agent:',run(message))
        except Exception as exc: print('Error:',exc)

def lambda_handler(event,context):
    message=event.get('message')
    if not message:return {'statusCode':400,'body':'Missing message'}
    return run(message,event)

if __name__=='__main__': main()
