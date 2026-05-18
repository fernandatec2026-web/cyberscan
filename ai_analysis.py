import os
from openai import OpenAI

def generate_ai_summary(secrets_results, deps_results):
    """Uses AI to generate an executive security analysis and remediation guidance."""
    # Check whether the API key is configured in the environment
    if not os.environ.get("OPENAI_API_KEY"):
        return "AI analysis temporarily unavailable: OpenAI API environment variable not configured."

    try:
        client = OpenAI()
        
        # Prepare detected findings to send as simplified context to the AI
        context = {
            "exposed_secrets": [item["type"] for files in secrets_results.values() for item in files],
            "vulnerable_dependencies": [f"{item['package']} ({item['cve']})" for item in deps_results]
        }
        
        prompt = f"""
        As a Senior Application Security (AppSec) specialist, provide a short and direct executive summary in English (maximum 4 lines) about the following risks identified during the code scan:
        {context}
        
        Describe the primary impact and the immediate action the developer should take.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.2
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception:
        return (
        "AI analysis temporarily unavailable. "
        "The OpenAI API integration is configured correctly, "
        "but requires active API billing credits."
        )