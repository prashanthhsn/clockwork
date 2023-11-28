from tabs.modal_builder.utils import *
from database_include_exclude import FIELDS_TO_EXCLUDE


class ModalConfigBuilder:

    def __init__(self, customize_item_label=None) -> None:
        self.customize_label = customize_item_label
        self.type_to_method = {
            ColumnType.INTEGER: self.generate_number_modal_config,
            ColumnType.VARCHAR: self.generate_text_modal_config,
            ColumnType.AUTOCOMPLETE: self.generate_autocomplete_modal_config,
            ColumnType.DATE: self.generate_date_modal_config,
            ColumnType.BOOLEAN: self.generate_boolean_modal_config
            # Add more data types as needed
        }

        # properties of modal config
        self.record_id = None
        self.id_key = None
        self.object = None
        self.key_map = None
        self.items = []
        self.validation = None

    def build(self, table):
        return self.set_record_id().\
            set_id_key().\
            set_object(table.name).\
            set_key_map().\
            set_validation().\
            set_items(table.columns._all_columns).\
            build_modal_config()

    def build_modal_config(self):
        return ModalConfig(
            recordId=self.record_id,
            idKey=self.id_key,
            object=self.object,
            keyMap=self.key_map,
            items=self.items,
            valdiation=self.validation)

    def get_label(self, column):
        if not self.customize_label:
            return f"{column.table.name}.{column.name}"
        else:
            return self.customize_label(column)

    @staticmethod
    def check_field_type(column):
        if not str(column.type).isalpha():
            column_type, max_value = str(column.type).split('(')
            max_value = max_value.rsplit(')')[0]
            return (column_type, max_value) if not bool(column.foreign_keys) else ('AUTOCOMPLETE', None)
        else:
            return (str(column.type).split('(')[0], None) if not bool(column.foreign_keys) else ('AUTOCOMPLETE', None)

    def generate_autocomplete_modal_config(self, column, _):
        label = self.get_label(column)
        field = AutocompleteItem(id=column.name, label=label)
        field.set_prefixId()
        field.set_groupKey()
        for fkey in column.foreign_keys:
            field.set_payload(objects=fkey._table_key(),
                              fields=fkey.target_fullname)
        return field

    def generate_number_modal_config(self, column, max_value=None):
        label = self.get_label(column)
        field = NumberItem(id=column.name, label=label)
        field.set_max_value(max_value=max_value)
        return field

    def generate_text_modal_config(self, column, max_length=None):
        label = self.get_label(column)
        field = TextItem(id=column.name, label=label)
        field.set_max_length(max_length=max_length)
        return field

    def generate_date_modal_config(self, column, _):
        label = self.get_label(column)
        field = DateItem(id=column.name, label=label)
        return field

    def generate_boolean_modal_config(self, column, _):
        label = self.get_label(column)
        field = BooleanItem(id=column.name, label=label)
        return field

    def set_record_id(self, record_id: str = None):
        self.record_id = record_id
        return self

    def set_id_key(self, id_key: str = None):
        self.id_key = id_key
        return self

    def set_object(self, object: str):
        self.object = object
        return self

    def set_key_map(self):
        self.key_map = KeyMap()
        return self

    def set_validation(self):
        self.validation = Validation()
        return self

    def set_items(self, columns):
        for column in columns:
            if column.name in FIELDS_TO_EXCLUDE:
                continue
            else:
                column_type, max_value = self.check_field_type(
                    column)
                if column_type not in self.type_to_method:
                    continue
                else:
                    method = self.type_to_method[column_type]
                    field = method(column, max_value)
                    self.items.append(field)
        return self
