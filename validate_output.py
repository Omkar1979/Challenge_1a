import json
import os
from jsonschema import validate, ValidationError

SCHEMA_PATH = "sample_dataset/schema/output_schema.json"
OUTPUT_DIR = "output"

with open(SCHEMA_PATH, "r") as schema_file:
    schema = json.load(schema_file)

valid = True
for file in os.listdir(OUTPUT_DIR):
    if file.endswith(".json"):
        path = os.path.join(OUTPUT_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        try:
            validate(instance=data, schema=schema)
            print(f" {file} is VALID")
        except ValidationError as e:
            print(f" {file} is INVALID:")
            print(f"   ⤷ {e.message}")
            valid = False

if valid:
    print("\n All output files passed schema validation!")
else:
    print("\n⚠️ Some files failed. Fix them before submission.")
