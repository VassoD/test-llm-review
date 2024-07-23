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

def get_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.warning(f"File not found: {file_path}")
        return None

def are_files_identical(file1, file2):
    content1 = get_file_content(file1)
    content2 = get_file_content(file2)
    return content1 == content2 and content1 is not None

def main():
    comments = {}
    changed_files = get_changed_files()
    
    # Group identical files
    file_groups = {}
    for file_path in changed_files:
        if file_path.endswith((".js")):
            found_group = False
            for group, paths in file_groups.items():
                if any(are_files_identical(file_path, existing_path) for existing_path in paths):
                    paths.append(file_path)
                    found_group = True
                    break
            if not found_group:
                file_groups[file_path] = [file_path]

    for group, file_paths in file_groups.items():
        logging.info(f"Analyzing changes in file group: {file_paths}")
        diff = get_file_diff(group)
        if diff:
            feedback = analyze_code(diff)
            comments[group] = (file_paths, feedback)
        else:
            logging.info(f"No changes found in {group}")

    final_comments = []
    for group, (file_paths, feedback) in comments.items():
        if len(file_paths) == 1:
            final_comments.append(f"Review for {file_paths[0]}:\n\n{feedback}")
        else:
            paths_str = ", ".join(file_paths)
            final_comments.append(f"Review for files: {paths_str}\n\n{feedback}")

    with open('comments.json', 'w') as outfile:
        json.dump(final_comments, outfile)
    logging.info(f"Comments saved to comments.json: {final_comments}")

if __name__ == "__main__":
    main()