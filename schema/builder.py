from schema.utils import *


class SchemaBuilder:

    def __init__(self) -> None:
        self.schema = Schema()
        self.type_to_method = {
            TypeEnum.STRING: self.build_text_property,
            TypeEnum.NUMBER: self.build_number_property,
            TypeEnum.BOOLEAN: self.build_boolean_property
        }
        self.column_type = {
            Integer: TypeEnum.NUMBER,
            Numeric: TypeEnum.NUMBER,
            String: TypeEnum.STRING,
            DateTime: TypeEnum.DATETIME,
            Boolean: TypeEnum.BOOLEAN
        }

    def build(self, table):
        for column in table.columns._all_columns:
            column_type = get_column_type(column)
            method = self.type_to_method[column_type]
            self.schema.properties[column.name] = method(column, column_type)
        return self.schema

    def build_text_property(self, column, column_type):
        property = TextProperty(column_type.value)
        if hasattr(column.type, 'length'):
            property.set_maxLength(column.type.length)
        return property

    def build_number_property(self, column, column_type):
        property = NumericProperty(column_type.value)
        # property.set_precision(column.type.precision if hasattr(
        #     column.type, 'precision') else None)
        # property.set_scale(column.type.scale if hasattr(
        #     column.type, 'scale') else None)
        if hasattr(column.server_default, 'minvalue'):
            property.set_minimum(column.server_default.minvalue)
        if hasattr(column.server_default, 'maxvalue'):
            property.set_maximum(column.server_default.maxvalue)
        return property

    def build_boolean_property(self, column, column_type):
        property = BooleanProperty(column_type.value)
        return property
