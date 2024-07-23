import os
import json
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

def analyze_code(file_content):
    anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    prompt = f"{HUMAN_PROMPT} Please provide a brief code review for the following code. Focus on the most important 2-3 points. Be concise and direct, as if you're a developer leaving a quick comment on a pull request:\n\n{file_content}\n{AI_PROMPT}"
    
    response = anthropic.completions.create(
        prompt=prompt,
        max_tokens_to_sample=150, 
        model="claude-2.0",
        temperature=0.7, 
    )
    
    return response.completion.strip()

def main():
    comments = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".js")):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                feedback = analyze_code(code)
                comments.append(f"Review for {file_path}:\n\n{feedback}")

    with open('comments.json', 'w') as outfile:
        json.dump(comments, outfile)

if __name__ == "__main__":
    main()