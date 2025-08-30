import os
from typing import Dict
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods

from prompts import EXTRACT_PROMPT, REWRITE_PROMPT, VERIFY_PROMPT, TONE_HINTS

def _get_cfg():
    return {
        "api_key": os.getenv("WATSONX_API_KEY", ""),
        "url": os.getenv("WATSONX_URL", ""),
        "project_id": os.getenv("WATSONX_PROJECT_ID", ""),
        "model_id": os.getenv("WATSONX_MODEL_ID", "ibm/granite-13b-instruct-v2"),
    }

def get_wx_model():
    cfg = _get_cfg()
    if not all([cfg["api_key"], cfg["url"], cfg["project_id"], cfg["model_id"]]):
        raise RuntimeError("Missing watsonx.ai environment variables.")
    params = {
        GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
        GenParams.MAX_NEW_TOKENS: 900,
        GenParams.TEMPERATURE: 0.25,
        GenParams.REPETITION_PENALTY: 1.05,
    }
    model = Model(
        model_id=cfg["model_id"],
        params=params,
        credentials={"url": cfg["url"], "apikey": cfg["api_key"]},
        project_id=cfg["project_id"],
    )
    return model

def _gen_text(model: Model, prompt: str) -> str:
    resp = model.generate_text(prompt=prompt)
    if isinstance(resp, dict):
        return resp.get("results", [{}])[0].get("generated_text", "").strip()
    return str(resp).strip()

def rewrite_with_tone(source: str, tone: str) -> Dict[str, str]:
    model = get_wx_model()
    facts = _gen_text(model, EXTRACT_PROMPT.format(source=source))
    tone_hint = TONE_HINTS.get(tone, "")
    rewrite_prompt = REWRITE_PROMPT.format(source=source, facts=facts, tone=f"{tone} ({tone_hint})")
    rewrite = _gen_text(model, rewrite_prompt)
    issues = _gen_text(model, VERIFY_PROMPT.format(source=source, facts=facts, rewrite=rewrite))
    if issues.strip().upper() != "OK":
        model.params[GenParams.TEMPERATURE] = 0.0
        rewrite = _gen_text(model, rewrite_prompt)
    return {"facts": facts, "rewrite": rewrite}