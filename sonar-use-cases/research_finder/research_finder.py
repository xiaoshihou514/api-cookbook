#!/usr/bin/env python3
"""
Research Finder CLI - A tool to research topics or questions using Perplexity's Sonar API.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional, Any

import requests # Added requests import
from requests.exceptions import RequestException

class ResearchAssistant:
    """A class to interact with Perplexity Sonar API for research."""

    API_URL = "https://api.perplexity.ai/chat/completions"
    DEFAULT_MODEL = "sonar-pro"
    PROMPT_FILE = "system_prompt.md" # Default prompt filename

    def __init__(self, api_key: Optional[str] = None, prompt_file: Optional[str] = None):
        """
        Initialize the ResearchAssistant with API key and system prompt.
        """
        self.api_key = api_key or self._get_api_key()
        if not self.api_key:
            raise ValueError(
                "API key not found. Please provide via argument, environment variable (PPLX_API_KEY), or key file."
            )

        script_dir = Path(__file__).parent
        prompt_path = Path(prompt_file) if prompt_file else script_dir / self.PROMPT_FILE
        if not prompt_path.is_absolute() and prompt_file:
             prompt_path = Path.cwd() / prompt_file
        elif not prompt_path.is_absolute():
             prompt_path = script_dir / self.PROMPT_FILE

        self.system_prompt = self._load_system_prompt(prompt_path)
        print(f"System prompt loaded from: {prompt_path}", file=sys.stderr) # Debug print

    def _get_api_key(self) -> str:
        """
        Try to get API key from environment or from a file.
        """
        api_key = os.environ.get("PPLX_API_KEY", "")
        if api_key:
            return api_key

        search_dirs = [Path.cwd(), Path(__file__).parent]
        key_filenames = ["pplx_api_key", ".pplx_api_key", "PPLX_API_KEY", ".PPLX_API_KEY"]

        for directory in search_dirs:
            for key_file in key_filenames:
                key_path = directory / key_file
                if key_path.exists():
                    try:
                        return key_path.read_text().strip()
                    except Exception:
                        pass
        return ""

    def _load_system_prompt(self, prompt_path: Path) -> str:
        """
        Load the system prompt from a file.
        """
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Warning: Prompt file not found at {prompt_path}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Could not load system prompt from {prompt_path}: {e}", file=sys.stderr)

        print("Using fallback default system prompt.", file=sys.stderr)
        return (
            "You are an AI research assistant. Your task is to research the user's query, "
            "provide a concise summary, and list the sources used."
        )

    def research_topic(self, query: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
        """Placeholder for research function."""
        print(f"Researching (placeholder): '{query}' using model '{model}'...")
        # TODO: Implement actual API call here
        return {"summary": "Placeholder summary", "sources": ["placeholder source"], "raw_response": ""}


def display_results(results: Dict[str, Any]):
    """Placeholder for displaying results."""
    print("\n--- Results ---")
    print(f"Summary: {results.get('summary')}")
    print(f"Sources: {results.get('sources')}")
    print("---------------")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Research Finder CLI")
    parser.add_argument("query", type=str, help="The research question or topic.")
    parser.add_argument("-m", "--model", type=str, default=ResearchAssistant.DEFAULT_MODEL, help=f"Perplexity model (default: {ResearchAssistant.DEFAULT_MODEL})")
    parser.add_argument("-k", "--api-key", type=str, help="Perplexity API key (overrides env var/file)")
    parser.add_argument("-p", "--prompt-file", type=str, help=f"Path to system prompt (default: {ResearchAssistant.PROMPT_FILE})")
    # TODO: Add JSON output arg later

    args = parser.parse_args()

    try:
        print(f"Initializing research assistant for query: \"{args.query}\"", file=sys.stderr)
        assistant = ResearchAssistant(api_key=args.api_key, prompt_file=args.prompt_file)

        print("Researching in progress...", file=sys.stderr)
        results = assistant.research_topic(args.query, model=args.model)
        display_results(results)

    except ValueError as e: # Catch API key error
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred in main: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
