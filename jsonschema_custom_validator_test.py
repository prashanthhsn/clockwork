from numbers import Number
from jsonschema import validators, Draft7Validator
from jsonschema.exceptions import ValidationError

all_validators = dict(Draft7Validator.VALIDATORS)


def is_odd(validator, value, instance, schema):
    if not isinstance(instance, Number):
        yield ValidationError("%r is not a number" % instance)

    if not bool(instance & 1):
        yield ValidationError("%r is not an odd number" % instance)


all_validators["odd"] = is_odd

CustomValidator = validators.create(
    meta_schema=Draft7Validator.META_SCHEMA, validators=all_validators)

if __name__ == "__main__":

    schema = {
        'type': 'object',
        'properties': {
            'value': {
                'type': 'number',
                'odd': True
            },
        }
    }

    validator = CustomValidator(schema=schema)

    try:
        validator.validate({"value": 4})
    except ValidationError as error:
        print(error)