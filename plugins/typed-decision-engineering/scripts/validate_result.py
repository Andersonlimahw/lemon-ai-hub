#!/usr/bin/env python3
"""Validate semantic invariants JSON Schema cannot express across spec/results."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def validate(spec: dict, result: dict, tolerance: float = 1e-6) -> None:
    questions = spec.get("questions", {})
    answers = result.get("answers", {})
    if set(questions) != set(answers):
        raise ValueError("answer IDs must exactly match question IDs")
    for question_id, question in questions.items():
        answer = answers[question_id]
        if answer.get("type") != question.get("type"):
            raise ValueError(f"{question_id}: answer type mismatch")
        if answer["type"] == "noul":
            value = answer.get("noul")
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{question_id}: noul must be finite in [0,1]")
            continue
        probabilities = answer.get("probabilities", {})
        expected = list(question["criteria"] if answer["type"] == "choice" else range(len(question["criteria"])))
        actual = list(probabilities)
        if answer["type"] == "choice" and set(actual) != set(expected):
            raise ValueError(f"{question_id}: probability keys must match Choice criteria")
        values = list(probabilities.values())
        if not values or any(isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1 for value in values):
            raise ValueError(f"{question_id}: invalid probabilities")
        if abs(sum(values) - 1) > tolerance:
            raise ValueError(f"{question_id}: probabilities must sum to 1")
        if answer["type"] == "choice" and answer.get("choice") not in probabilities:
            raise ValueError(f"{question_id}: selected choice missing from probabilities")
        if answer["type"] == "score" and not 0 <= answer.get("score", -1) <= len(expected) - 1:
            raise ValueError(f"{question_id}: score outside level range")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    validate(json.loads(args.spec.read_text(encoding="utf-8")), json.loads(args.result.read_text(encoding="utf-8")))


if __name__ == "__main__":
    main()
