import openai, os, pathlib

openai.api_key = os.getenv("OPENAI_API_KEY")      # KEY aus Env-Var
PROMPTS = pathlib.Path("prompts")                 # Ordner mit .txt-Dateien

def _fill(template: str, mapping: dict) -> str:
    return (PROMPTS / template).read_text(encoding="utf-8").format(**mapping)

def get_analysis(profile: dict) -> str:
    prompt = _fill("analysis_prompt.txt", profile)
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

def get_plan(analysis_text: str) -> str:
    prompt = _fill("plan_prompt.txt",
                   {"Spieleranalyse_von_Prompt_1": analysis_text})
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()
