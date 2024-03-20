import json
import sys

import jsonschema

from . import content_origin


STRINGS = {
    "anyOf": [
        {"type": "string"},
        {"type": "array", "items": {"type": "string"}},
    ]
}


def get_schema():
    return {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "packages": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
            },
            "contentOrigin": {
                "type": "object",
                "properties": {
                    source_type: {"type": "array", "items": collector.schema}
                    for source_type, collector in content_origin.load().items()
                },
            },
        },
        "required": ["packages", "contentOrigin"],
        "additionalProperties": False,
    }


def validate(config):
    try:
        jsonschema.validate(config, get_schema())
    except jsonschema.ValidationError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


def print_schema():
    print(json.dumps(get_schema(), indent=2))