import os
import json
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

def analyze_code(file_content):
    anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    prompt = f"{HUMAN_PROMPT} Please review the following code and provide feedback and suggestions:\n\n{file_content}\n{AI_PROMPT}"
    
    response = anthropic.completions.create(
        prompt=prompt,
        max_tokens_to_sample=300,
        model="claude-2.0",
        temperature=0.5,
    )
    
    return response.completion.strip()

def main():
    comments = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".css", ".html")):  # Add or remove file types as needed
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                feedback = analyze_code(code)
                comments.append(f"Review for {file_path}:\n\n{feedback}")

    with open('comments.json', 'w') as outfile:
        json.dump(comments, outfile)

if __name__ == "__main__":
    main()