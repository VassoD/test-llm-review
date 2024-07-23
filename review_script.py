import os
import json
import subprocess
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import logging

logging.basicConfig(level=logging.INFO)

def get_changed_files():
    result = subprocess.run(['git', 'diff', '--name-status', 'origin/main...HEAD'], capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def get_file_diff(file_path):
    result = subprocess.run(['git', 'diff', 'origin/main...HEAD', '--', file_path], capture_output=True, text=True)
    return result.stdout

def get_previous_comments(file_path):
    try:
        with open('previous_comments.json', 'r') as f:
            all_comments = json.load(f)
        return all_comments.get(file_path, "")
    except FileNotFoundError:
        return ""

def save_comments(comments):
    with open('previous_comments.json', 'w') as f:
        json.dump(comments, f)

def analyze_code(file_content, previous_comments):
    anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    prompt = f"""{HUMAN_PROMPT} As a senior developer, provide a brief, easy-to-read code review for the following changes. Focus on:
1. Key improvements or good practices implemented
2. The most important suggestion for further improvement

Guidelines:
- Be concise. Limit your review to 2-3 short paragraphs.
- Prioritize the most impactful feedback.
- Avoid repeating suggestions from previous reviews unless they're critical and unaddressed.

Previous review summary:
{previous_comments}

Code to review:
{file_content}

Provide your review in this format:
1. Positive point(s): [Very brief mention of good changes]
2. Top suggestion: [One key suggestion with a very short explanation]
3. Overall: [One-sentence summary of the code quality]

{AI_PROMPT}"""
    
    response = anthropic.completions.create(
        prompt=prompt,
        max_tokens_to_sample=400,
        model="claude-2.0",
        temperature=0.7,
    )
    
    feedback = response.completion.strip()
    logging.info(f"Claude's feedback: {feedback}")
    return feedback

def main():
    comments = {}
    changed_files = get_changed_files()
    
    for change in changed_files:
        status, file = change.split('\t')
        if status in ['A', 'M']:  # Only consider Added or Modified files
            if file.endswith((".js")):
                logging.info(f"Analyzing changes in file: {file}")
                diff = get_file_diff(file)
                if diff:
                    previous_comments = get_previous_comments(file)
                    feedback = analyze_code(diff, previous_comments)
                    comments[file] = feedback
                else:
                    logging.info(f"No changes found in {file}")
        elif status == 'D':
            logging.info(f"File deleted: {file}. Skipping review.")

    final_comments = [f"Review for {file}:\n\n{feedback}" for file, feedback in comments.items()]
    
    with open('comments.json', 'w') as outfile:
        json.dump(final_comments, outfile)
    
    save_comments(comments)
    logging.info(f"Comments saved to comments.json and previous_comments.json")

if __name__ == "__main__":
    main()