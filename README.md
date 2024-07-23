# Testing Automated PR reviews

This project includes a JavaScript file and an automated code review system using Claude AI.

## Structure

- `src/script.js`: Main JavaScript file
- `.github/workflows/claude-code-review.yml`: GitHub Actions workflow for automated code review
- `review_script.py`: Python script for interfacing with Claude AI

## Setup

1. Ensure you have a GitHub account and have created a repository.
2. Clone this repository to your local machine.
3. Install the required Python packages: `pip install anthropic requests`
4. Set up your Anthropic API key as a secret in your GitHub repository settings. Name it `ANTHROPIC_API_KEY`.

## Usage

The code review system will automatically run on every pull request. Claude AI will analyze the code changes and provide feedback as comments on the pull request.
