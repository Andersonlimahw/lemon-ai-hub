import json
import importlib.util
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MODULE_SPEC = importlib.util.spec_from_file_location("validate_result", ROOT / "scripts/validate_result.py")
VALIDATOR = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(VALIDATOR)


class SchemaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = Draft202012Validator(json.loads((ROOT / "references/decision-spec.schema.json").read_text()))
        cls.result = Draft202012Validator(json.loads((ROOT / "references/decision-result.schema.json").read_text()))

    def test_all_question_types_validate(self):
        payload = {"schema_version":"1", "state":{"text":"hello"}, "questions": {
            "route":{"type":"choice","instructions":"route", "criteria":{"a":"A","b":"B"}},
            "quality":{"type":"score","instructions":"score", "criteria":["bad","good"]},
            "safe":{"type":"noul","instructions":"is safe", "criteria":{"true":"safe","false":"unsafe"}},
        }}
        self.spec.validate(payload)

    def test_unknown_question_property_rejected(self):
        payload = {"schema_version":"1", "state":"x", "questions":{"q":{"type":"noul","instructions":"x","extra":1}}}
        self.assertTrue(list(self.spec.iter_errors(payload)))

    def test_result_bounds(self):
        valid = {"schema_version":"1", "answers":{"q":{"type":"noul","noul":0.7}}}
        self.result.validate(valid)
        invalid = {"schema_version":"1", "answers":{"q":{"type":"noul","noul":1.2}}}
        self.assertTrue(list(self.result.iter_errors(invalid)))

    def test_semantic_result_validation(self):
        spec = {"questions":{"route":{"type":"choice","criteria":{"safe":"S","unsafe":"U"}}}}
        valid = {"answers":{"route":{"type":"choice","choice":"safe","probabilities":{"safe":0.8,"unsafe":0.2}}}}
        VALIDATOR.validate(spec, valid)
        invalid = {"answers":{"route":{"type":"choice","choice":"admin","probabilities":{"safe":0.2,"unsafe":0.2}}}}
        with self.assertRaises(ValueError):
            VALIDATOR.validate(spec, invalid)


if __name__ == "__main__":
    unittest.main()
