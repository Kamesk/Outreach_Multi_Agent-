from config import settings

def generate_text(system_prompt,user_prompt,model="gpt-5.4-nano",**kwargs):
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    from openai import OpenAI
    client=OpenAI(api_key=settings.openai_api_key)
    r=client.chat.completions.create(model=model,messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],**kwargs)
    return r.choices[0].message.content.strip()
