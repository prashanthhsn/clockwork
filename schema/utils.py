from enum import Enum
from sqlalchemy import Integer, String, DateTime, Boolean, Numeric


class TypeEnum(Enum):
    BOOLEAN = "boolean"
    STRING = "string"
    DATETIME = "datetime"
    NUMBER = "number"


class Schema:

    def __init__(self) -> None:
        self.type = "object"
        self.properties = {}
        self.validate_time_entry = True


class Property:

    type: TypeEnum

    def __init__(self, type: TypeEnum) -> None:
        self.type = type


class TextProperty(Property):

    def __init__(self, type: TypeEnum) -> None:
        super().__init__(type)

    def set_maxLength(self, maximum):
        self.maxlength = maximum

    def set_default(self, default):
        self.default = default


class NumericProperty(Property):

    def __init__(self, type: TypeEnum) -> None:
        super().__init__(type)

    def set_precision(self, precision):
        self.precision = precision

    def set_scale(self, scale):
        self.scale = scale

    def set_default(self, default):
        self.default = default

    def set_minimum(self, min):
        self.min = min

    def set_maximum(self, max):
        self.max = max


class BooleanProperty(Property):

    def __init__(self, type: TypeEnum) -> None:
        super().__init__(type)

    def set_default(self, default):
        self.default = default


def get_column_type(column):
    if isinstance(column.type, Integer):
        return TypeEnum.NUMBER
    elif isinstance(column.type, Numeric):
        return TypeEnum.NUMBER
    elif isinstance(column.type, String):
        return TypeEnum.STRING
    elif isinstance(column.type, DateTime):
        return TypeEnum.DATETIME
    elif isinstance(column.type, Boolean):
        return TypeEnum.BOOLEAN
    else:
        return TypeEnum.STRING
