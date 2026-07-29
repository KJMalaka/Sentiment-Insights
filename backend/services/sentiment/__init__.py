from .layer1_vader import VaderLayer
from .layer2_sklearn import SklearnLayer
from .layer3_groq import GroqLayer
from typing import Dict, Any, List

# Cap how many comments are sent through the LLM layer per video, so a
# high-comment-count video can't blow through Groq's free-tier tokens-per-minute limit.
MAX_LLM_COMMENTS = 50

def analyze_comments(comments: List[str]) -> List[Dict[str, Any]]:
    vader = VaderLayer()
    sklearn = SklearnLayer()
    groq = GroqLayer()

    # Process layers
    vader_results = vader.analyze_batch(comments)
    sklearn_results = sklearn.analyze_batch(comments)

    # Only the first MAX_LLM_COMMENTS go through the LLM; the rest get the same
    # neutral placeholder Groq itself returns when the key is missing or a batch fails.
    llm_sample = comments[:MAX_LLM_COMMENTS]
    groq_results = groq.analyze_batch(llm_sample)
    if len(comments) > MAX_LLM_COMMENTS:
        groq_results.extend([
            {"label": "neutral", "is_sarcastic": False, "is_mixed": False, "themes": []}
            for _ in range(len(comments) - MAX_LLM_COMMENTS)
        ])

    combined_results = []
    for i in range(len(comments)):
        combined_results.append({
            "text": comments[i],
            "vader": vader_results[i],
            "sklearn": sklearn_results[i],
            "groq": groq_results[i]
        })

    return combined_results
