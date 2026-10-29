"""
LLM Response Evaluator
=======================
A tool for scoring LLM outputs against quality rubrics.

Author: Samuel Eno Sunday
License: MIT
"""

import json
import sys
from pathlib import Path


def load_responses(filepath):
    """Load LLM responses from a JSON file."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found -> {filepath}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("Error: JSON must contain a list of response objects.")
        sys.exit(1)

    return data


def calculate_average(scores):
    """Return the average of a list of numbers (rounded to 2 decimals)."""
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 2)


def evaluate_response(item):
    """Evaluate a single response. Returns a dict with scores and average."""
    factuality = item.get("factuality_score", 0)
    relevance = item.get("relevance_score", 0)
    safety = item.get("safety_score", 0)

    avg = calculate_average([factuality, relevance, safety])

    return {
        "id": item.get("id", "N/A"),
        "factuality": factuality,
        "relevance": relevance,
        "safety": safety,
        "average": avg,
    }


def generate_report(evaluations):
    """Print a clean evaluation report to the console."""
    print("=" * 50)
    print("LLM RESPONSE EVALUATION REPORT")
    print("=" * 50)
    print(f"Total responses evaluated: {len(evaluations)}\n")

    overall_scores = []

    for ev in evaluations:
        print(
            f"ID {ev['id']} | "
            f"Factuality: {ev['factuality']} | "
            f"Relevance: {ev['relevance']} | "
            f"Safety: {ev['safety']} | "
            f"Avg: {ev['average']}"
        )
        overall_scores.append(ev["average"])

    overall_average = calculate_average(overall_scores)

    print("=" * 50)
    print(f"Overall average score: {overall_average}")
    print("=" * 50)


def main():
    filepath = "sample_data.json"

    # Allow passing a filename via command line: python evaluator.py myfile.json
    if len(sys.argv) > 1:
        filepath = sys.argv[1]

    print(f"Loading responses from: {filepath}\n")
    responses = load_responses(filepath)

    evaluations = [evaluate_response(item) for item in responses]
    generate_report(evaluations)


if __name__ == "__main__":
    main()
