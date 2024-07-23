import os
import json
import subprocess
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import logging

logging.basicConfig(level=logging.INFO)

def get_changed_files():
    result = subprocess.run(['git', 'diff', '--name-only', 'origin/main...HEAD'], capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def get_file_diff(file_path):
    result = subprocess.run(['git', 'diff', 'origin/main...HEAD', '--', file_path], capture_output=True, text=True)
    return result.stdout

def analyze_code(file_content):
    anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    prompt = f"{HUMAN_PROMPT} Please review the following code changes and provide feedback. Focus on the most important 2-3 points. Be concise and direct, as if you're a developer leaving a quick comment on a pull request. Only comment on the changes shown, not on existing code:\n\n{file_content}\n{AI_PROMPT}"
    
    response = anthropic.completions.create(
        prompt=prompt,
        max_tokens_to_sample=150,
        model="claude-2.0",
        temperature=0.7,
    )
    
    feedback = response.completion.strip()
    logging.info(f"Claude's feedback: {feedback}")
    return feedback

def main():
    comments = []
    changed_files = get_changed_files()
    for file_path in changed_files:
        if file_path.endswith((".js")):
            logging.info(f"Analyzing changes in file: {file_path}")
            diff = get_file_diff(file_path)
            if diff:
                feedback = analyze_code(diff)
                comments.append(f"Review for changes in {file_path}:\n\n{feedback}")
            else:
                logging.info(f"No changes found in {file_path}")

    with open('comments.json', 'w') as outfile:
        json.dump(comments, outfile)
    logging.info(f"Comments saved to comments.json: {comments}")

if __name__ == "__main__":
    main()