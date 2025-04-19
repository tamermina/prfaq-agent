import re

def prfaq_to_safefeatures(text: str):
    """
    Very light parser to turn a PRFAQ into one Epic and many Features.
    Improve later with a proper LLM transform.
    """
    # Epic comes from the Headline line
    first_line = text.splitlines()[0].strip()
    epic = {
        "name": first_line[:80],
        "description": text
    }

    # Each Q: becomes a Feature
    blocks = re.findall(r"Q:\s*(.*?)\nA:\s*([\s\S]*?)(?=\nQ:|\Z)", text)
    features = []
    for q, a in blocks:
        features.append({
            "name": q[:80],
            "description": a.strip(),
            "benefitHypothesis": a.split(".")[0]
        })

    if not features:
        raise ValueError("No FAQ pairs found.")

    return {"epic": epic, "features": features}