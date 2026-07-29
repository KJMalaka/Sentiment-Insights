import os
import json
import time
from typing import Dict, Any, List
from groq import Groq
from .base import SentimentLayer
import re

class GroqLayer(SentimentLayer):
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            self.client = None
            print("Warning: GROQ_API_KEY is missing. Groq layer will return mock data.")
        else:
            self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"  # Fast Llama model

    def analyze(self, comment: str) -> Dict[str, Any]:
        if not self.client:
            return {"label": "neutral", "is_sarcastic": False, "is_mixed": False, "themes": []}

        return self.analyze_batch([comment])[0]

    def analyze_batch(self, comments: List[str]) -> List[Dict[str, Any]]:
        if not self.client:
            return [{"label": "neutral", "is_sarcastic": False, "is_mixed": False, "themes": []} for _ in comments]

        # Process in batches of 10 to avoid overwhelming the model or prompt length limits
        batch_size = 10
        all_results = []

        for i in range(0, len(comments), batch_size):
            batch = comments[i:i + batch_size]
            prompt = self._build_prompt(batch)

            # Small pacing delay between requests (skip before the first) to stay
            # well under the free-tier tokens-per-minute limit on bulk analysis.
            if i > 0:
                time.sleep(1.2)

            try:
                response = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a JSON-only sentiment analysis API. You MUST output an array of JSON objects, one for each comment. Do not output any markdown formatting, no intro, no outro, ONLY the raw JSON array."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model=self.model,
                    temperature=0.1,
                    # We can't guarantee JSON mode across all models, so we prompt strictly and parse defensively
                )

                content = response.choices[0].message.content.strip()

                # Defensively extract JSON array using regex if the model wrapped it in markdown
                match = re.search(r'\[.*\]', content, re.DOTALL)
                if match:
                    content = match.group(0)

                batch_results = json.loads(content)

                # Validate and fill missing fields
                for result in batch_results:
                    all_results.append({
                        "label": result.get("label", "neutral").lower() if result.get("label", "neutral").lower() in ["positive", "negative", "neutral"] else "neutral",
                        "is_sarcastic": bool(result.get("is_sarcastic", False)),
                        "is_mixed": bool(result.get("is_mixed", False)),
                        "themes": result.get("themes", [])[:2]
                    })
            except Exception as e:
                print(f"Error calling Groq API: {e}")
                # Fallback for failed batch
                all_results.extend([{"label": "neutral", "is_sarcastic": False, "is_mixed": False, "themes": []} for _ in batch])

        return all_results

    def _build_prompt(self, comments: List[str]) -> str:
        prompt = "Analyze the sentiment of the following comments.\n"
        prompt += "Return a JSON array of objects. Each object corresponds to the comment in the same order.\n"
        prompt += "Each object must have these exactly 4 keys:\n"
        prompt += "- label: string, exactly one of 'positive', 'negative', or 'neutral'\n"
        prompt += "- is_sarcastic: boolean, true if the comment appears sarcastic\n"
        prompt += "- is_mixed: boolean, true if the comment has both positive and negative sentiment\n"
        prompt += "- themes: array of up to 2 strings, brief 1-3 word themes/topics mentioned in the comment\n\n"

        prompt += "Comments:\n"
        for i, comment in enumerate(comments):
            # Clean up newlines and quotes to not break the prompt
            cleaned_comment = comment.replace('\n', ' ').replace('"', "'")
            prompt += f"{i+1}. \"{cleaned_comment}\"\n"

        return prompt
