import json
from datetime import date

from context.config import DATA_DIR

TRUTH = DATA_DIR / "truth" / "questions.jsonl"
CATEGORIES = {"anchor", "multi_source", "temporal", "conflict", "alias", "false_premise", "lookup"}


def items() -> list[dict]:
    return [json.loads(line) for line in TRUTH.read_text().splitlines()]


def test_ids_are_unique_and_sequential():
    ids = [q["id"] for q in items()]
    assert ids == [f"Q{i:02d}" for i in range(1, len(ids) + 1)]


def test_fields_and_categories():
    for q in items():
        assert q["category"] in CATEGORIES, q["id"]
        assert q["question"].strip() and q["expected_answer"].strip(), q["id"]
        date.fromisoformat(q["as_of"])
        assert q["expected_facts"], q["id"]


def test_every_expected_source_exists():
    missing = [(q["id"], s) for q in items() for s in q["expected_sources"] if not (DATA_DIR / s).is_file()]
    assert not missing


def test_false_premise_questions_cover_unknowns():
    false_premise = [q for q in items() if q["category"] == "false_premise"]
    assert len(false_premise) >= 3
    assert any(not q["expected_sources"] for q in false_premise)
