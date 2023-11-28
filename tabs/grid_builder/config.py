from tabs.grid_builder.utils import *
from database_include_exclude import FIELDS_TO_EXCLUDE


class Config:
    def __init__(self, recordId, rowId, title, dateRangeStartId, dateRangeEndId, payload, initialState, modalConfig, columns=[], actions=ACTIONS,  bulkActions=BULKACTIONS, toolbarActions=TOOLBARACTIONS, checkboxSelection=False) -> None:
        self.recordId = recordId
        self.rowId = rowId
        self.title = title
        self.actions = actions
        self.dateRangeStartId = dateRangeStartId
        self.dateRangeEndId = dateRangeEndId
        self.bulkActions = bulkActions
        self.toolbarActions = toolbarActions
        self.payload = payload
        self.initialState = initialState
        self.checkboxSelection = checkboxSelection
        self.columns = columns
        self.modalConfig = modalConfig


class ConfigBuilder:

    def __init__(self) -> None:
        self.record_id = None
        self.row_id = None
        self.title = None
        self.date_range_start_id = None
        self.date_range_end_id = None
        self.payload = None
        self.initial_state = None
        self.columns = []
        self.modal_config = None

        self.type_to_method = {
            ColumnType.VARCHAR: self.build_text_column_config,
            ColumnType.AUTOCOMPLETE: self.build_autocomplete_column_config,
            ColumnType.DATE: self.build_date_column_config,
            ColumnType.BOOLEAN: self.build_boolean_column_config,
            ColumnType.TIMESTAMP: self.build_time_column_config
        }

    def check_field_type(self, column):
        column_type = str(column.type).split(
            '(')[0] if '(' in str(column.type) else str(column.type)
        return column_type if not column.foreign_keys else ColumnType.AUTOCOMPLETE

    def build_text_column_config(self, field, _):
        return TextColumn(field)

    def build_boolean_column_config(self, field, _):
        return BooleanColumn(field)

    def build_autocomplete_column_config(self, field, column):
        autocomplete_column = AutoCompleteColumn(field)
        for fkey in column.foreign_keys:
            autocomplete_column.set_payload(objects=fkey._table_key(),
                                            fields=fkey.target_fullname)
        return autocomplete_column

    def build_date_column_config(self, field, _):
        return DateColumn(field)

    def build_time_column_config(self, field, _):
        return TimeColumn(field)

    def build_changed_by_user_config(self, table):
        field = f"{table.name}.{table.columns.get('modified_by_id').name}"
        date_field = f"{table.name}.{table.columns.get('modified_date').name}"
        changed_by_user_column = ChangedByUser(
            field=field, user_field=field, date_field=date_field)
        return changed_by_user_column

    def build_created_by_user_config(self, table):
        field = f"{table.name}.{table.columns.get('created_by_id').name}"
        date_field = f"{table.name}.{table.columns.get('created_date').name}"
        created_by_user_column = CreatedByUser(
            field=field, user_field=field, date_field=date_field)
        return created_by_user_column

    def build(self, table):
        return self.set_record_id().\
            set_row_id().\
            set_title().\
            set_date_range_start_id().\
            set_date_range_end_id().\
            set_payload(table_name=table.name, objects=[
                table.name], fields=table.columns._all_columns).\
            set_initial_state().\
            set_columns(table=table).\
            set_modal_config(table=table).\
            build_config()

    def build_config(self):
        return Config(
            recordId=self.record_id,
            rowId=self.row_id,
            title=self.title,
            dateRangeStartId=self.date_range_start_id,
            dateRangeEndId=self.date_range_end_id,
            payload=self.payload,
            initialState=self.initial_state,
            columns=self.columns,
            modalConfig=self.modal_config
        )

    def set_record_id(self, record_id: str = None):
        self.record_id = record_id
        return self

    def set_row_id(self, row_id: str = None):
        self.row_id = row_id
        return self

    def set_title(self, title: str = None):
        self.title = title
        return self

    def set_date_range_start_id(self, date_range_start_id: str = None):
        self.date_range_start_id = date_range_start_id
        return self

    def set_date_range_end_id(self, date_range_end_id: str = None):
        self.date_range_end_id = date_range_end_id
        return self

    def set_payload(self, table_name, objects, fields):
        config_payload = ConfigPayload(objects=objects)
        for field in fields:
            field = f"{table_name}.{field.name}"
            config_payload.fields.append(field)
        self.payload = config_payload
        return self

    def set_initial_state(self):
        self.initial_state = InitialState()
        return self

    def set_columns(self, table):
        columns = table.columns._all_columns
        for column in columns:
            if column.name in FIELDS_TO_EXCLUDE:
                continue
            else:
                column_type = self.check_field_type(column)
                if column_type in self.type_to_method:
                    method = self.type_to_method[column_type]
                    field = f"{column.table.name}.{column.name}"
                    self.columns.append(method(field, column))

        self.columns.extend([self.build_changed_by_user_config(
            table=table), self.build_created_by_user_config(table=table)])
        return self

    def set_modal_config(self, table, customize_item_label=None):
        builder = ModalConfigBuilder(customize_item_label)
        modal_config = builder.build(table=table)
        self.modal_config = modal_config
        return self
