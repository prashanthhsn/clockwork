from numbers import Number
from jsonschema import validators, Draft202012Validator
from jsonschema.exceptions import ValidationError
from enum import Enum

import json


class Duration(Enum):

    FIFTEEN_MINS = 900000

    THIRTY_MINS = 1800000

    FORTY_FIVE_MINS = 2700000

    ONE_HOUR = 3600000

    ONE_HOUR_FIFTEEN_MINS = 4500000

    ONE_HOUR_THIRTY_MINS = 5400000

    ONE_HOUR_FORTY_FIVE_MINS = 6300000

    TWO_HOURS = 7200000

    TWO_HOUR_FIFTEEN_MINS = 8100000

    TWO_HOUR_THIRTY_MINS = 9000000

    TWO_HOUR_FORTY_FIVE_MINS = 9900000

    THREE_HOURS = 10800000

    THREE_HOUR_FIFTEEN_MINS = 11700000

    THREE_HOUR_THIRTY_MINS = 12600000

    THREE_HOUR_FORTY_FIVE_MINS = 13500000

    FOUR_HOURS = 13500000

    FOUR_HOUR_FIFTEEN_MINS = 15300000

    FOUR_HOUR_THIRTY_MINS = 16200000

    FOUR_HOUR_FORTY_FIVE_MINS = 17100000

    FIVE_HOURS = 18000000

    FIVE_HOUR_FIFTEEN_MINS = 18900000

    FIVE_HOUR_THIRTY_MINS = 19800000

    FIVE_HOUR_FORTY_FIVE_MINS = 20700000

    SIX_HOURS = 21600000

    SIX_HOUR_FIFTEEN_MINS = 22500000

    SIX_HOUR_THIRTY_MINS = 23400000

    SIX_HOUR_FORTY_FIVE_MINS = 24300000

    SEVEN_HOURS = 25200000

    SEVEN_HOUR_FIFTEEN_MINS = 26100000

    SEVEN_HOUR_THIRTY_MINS = 27000000

    SEVEN_HOUR_FORTY_FIVE_MINS = 27900000

    EIGHT_HOURS = 28800000


def validate_time_entry(validator, value, instance, schema):
    if not isinstance(instance, dict):
        yield ValidationError("%r is not an object" % instance)

    start_time = instance.get('start_time', None)
    end_time = instance.get('end_time', None)

    if not isinstance(start_time, Number):
        yield ValidationError("'start_time' must be a number")

    if not isinstance(end_time, Number):
        yield ValidationError("'end_time' must be a number")

    duration = end_time - start_time

    if duration <= 28800000 and not ((duration//60000)%15==0):
        yield ValidationError("Billing Duration is not valid")

all_validators = dict(Draft202012Validator.VALIDATORS)
all_validators["validate_time_entry"] = validate_time_entry

CustomValidator = validators.create(
    meta_schema=Draft202012Validator.META_SCHEMA, validators=all_validators)


if __name__ == "__main__":

    input_json = {
    "start_time": 1694497508857,
    "end_time": 1694526308857,
    "description": "Custom Validator Test",
    "board_id": "068f7e9c-e9a5-4207-99d9-de345d538422",
    "billable": True,
    "labels": [
        "ab51f4c9-0b48-4de9-82cc-871a87f8c8ac"
    ]
}

    schema_file = open('time_entry_schema.json')
    schema = json.load(schema_file)

    validator = CustomValidator(schema=schema)

    try:
        validator.validate(input_json)
    except ValidationError as error:
        print(error)
