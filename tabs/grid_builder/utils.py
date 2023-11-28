from tabs.modal_builder.builder import ModalConfigBuilder


ACTIONS = ["edit", "delete", "clone"]
BULKACTIONS = ["update"]
TOOLBARACTIONS = ["hide", "filter", "daterange", "group-single", "export"]


class ColumnType:
    VARCHAR = 'VARCHAR'
    AUTOCOMPLETE = 'AUTOCOMPLETE'
    DATE = 'DATE'
    BOOLEAN = 'BOOLEAN'
    TIMESTAMP = 'TIMESTAMP'
    INTEGER = 'INTEGER'


class ToolTip:

    def __init__(self, user_field, date_field, tool_tip_text) -> None:
        self.userField = user_field
        self.dateField = date_field
        self.tooltipText = tool_tip_text


class Grid:
    def __init__(self, id, config,  type="datagrid"):
        self.id = id
        self.type = "datagrid"
        self.config = config


class SortingOrder:
    ASCENDING = "asc"
    DESCENDING = "desc"


class ColumnsCollection:
    def __init__(self):
        self.column_visibility_model = {}


class SortingModel:
    def __init__(self, field="last_modified", sort=SortingOrder.DESCENDING):
        self.field = field
        self.sort = sort


class Sorting:
    def __init__(self):
        self.sort_model = [SortingModel()]


class InitialState:
    def __init__(self):
        self.sorting = Sorting()
        self.columns = ColumnsCollection()


class Page:
    def __init__(self, size=50, number=1, total_records=0):
        self.size = size
        self.number = number
        self.total_records = total_records


class ConfigPayload:
    def __init__(self, search={}, sort={}, objects=[], view_name=None, fields=[], group_by=[]):
        self.objects = objects
        self.view_name = view_name
        self.fields = fields
        self.search = search
        self.sort = sort
        self.group_by = group_by
        self.page = Page()


class Column:

    def __init__(self, disableReorder=False, pinnable=False, resizable=True, sortable=True, filterable=True) -> None:
        self.disableReorder = disableReorder
        self.pinnable = pinnable
        self.resizable = resizable
        self.sortable = sortable
        self.filterable = filterable


class TextColumn(Column):

    def __init__(self, field, disableReorder=False, pinnable=False, resizable=True, sortable=True, filterable=True, headerName='', headerAlign="left", align="left", flex=4, editable=False, hideable=False, groupable=False) -> None:
        super().__init__(disableReorder, pinnable, resizable, sortable, filterable)
        self.field = field
        self.type = "string"
        self.headerName = headerName
        self.editable = editable
        self.hideable = hideable
        self.groupable = groupable
        self.headerAlign = headerAlign
        self.align = align
        self.flex = flex


class AutoCompleteColumn(Column):

    def __init__(self, field, disableReorder=False, pinnable=False, resizable=True, sortable=True, filterable=True, headerName='', headerAlign="left", align="left", flex=1, editable=False, hideable=False, groupable=True) -> None:
        super().__init__(disableReorder, pinnable, resizable, sortable, filterable)
        self.field = field
        self.type = "autocomplete"
        self.headerName = headerName
        self.headerName = headerName
        self.editable = editable
        self.hideable = hideable
        self.groupable = groupable
        self.headerAlign = headerAlign
        self.align = align
        self.flex = flex
        self.clearable = True

    def set_payload(self, objects, fields):
        self.payload = Payload(objects, fields)


class TimeColumn(Column):

    def __init__(self, field, disableReorder=False, pinnable=False, resizable=True, sortable=True, filterable=True, headerName='', headerAlign="center", align="center", flex=1, editable=False, hideable=True, groupable=False) -> None:
        super().__init__(disableReorder, pinnable, resizable, sortable, filterable)
        self.field = field
        self.type = "time"
        self.headerName = headerName
        self.headerName = headerName
        self.editable = editable
        self.hideable = hideable
        self.groupable = groupable
        self.headerAlign = headerAlign
        self.align = align
        self.flex = flex


class BooleanColumn(Column):

    def __init__(self, field, disableReorder=False, pinnable=False, resizable=True, sortable=True, filterable=True, headerName='', headerAlign="center", align="center", flex=1, editable=False, hideable=True, groupable=False) -> None:
        super().__init__(disableReorder, pinnable, resizable, sortable, filterable)
        self.field = field
        self.type = "boolean"
        self.headerName = headerName
        self.headerName = headerName
        self.editable = editable
        self.hideable = hideable
        self.groupable = groupable
        self.headerAlign = headerAlign
        self.align = align
        self.flex = flex


class DateColumn(Column):

    def __init__(self, field, disableReorder=False, pinnable=False, resizable=True, sortable=True, filterable=True, headerName='', headerAlign="left", align="left", flex=1, editable=True, hideable=True, groupable=False) -> None:
        super().__init__(disableReorder, pinnable, resizable, sortable, filterable)
        self.field = field
        self.type = "date"
        self.headerName = headerName
        self.headerName = headerName
        self.editable = editable
        self.hideable = hideable
        self.groupable = groupable
        self.headerAlign = headerAlign
        self.align = align
        self.flex = flex


class ChangedByUser(Column):

    def __init__(self, field, user_field, date_field, disableReorder=False, pinnable=False, resizable=True, sortable=False, filterable=False, tool_tip_text="dataGrid.updatedCellTooltip", headerName='', headerAlign="left", align="left", flex=1, editable=True, hideable=True, groupable=False) -> None:
        super().__init__(disableReorder, pinnable, resizable, sortable, filterable)
        self.field = field
        self.tooltip = ToolTip(user_field=user_field,
                               date_field=date_field, tool_tip_text=tool_tip_text)
        self.editable = editable
        self.align = align
        self.type = "changedByUser"
        self.headerAlign = headerAlign
        self.flex = flex
        self.hideable = hideable
        self.groupable = groupable
        self.headerName = headerName
        self.valueField = date_field


class CreatedByUser(Column):

    def __init__(self, field, user_field, date_field, disableReorder=False, pinnable=False, resizable=True, sortable=False, filterable=False, tool_tip_text="dataGrid.updatedCellTooltip", headerName='', headerAlign="left", align="left", flex=1, editable=True, hideable=True, groupable=False) -> None:
        super().__init__(disableReorder, pinnable, resizable, sortable, filterable)
        self.field = field
        self.tooltip = ToolTip(user_field=user_field,
                               date_field=date_field, tool_tip_text=tool_tip_text)
        self.editable = editable
        self.align = align
        self.type = "createdByUser"
        self.headerAlign = headerAlign
        self.flex = flex
        self.hideable = hideable
        self.groupable = groupable
        self.headerName = headerName
        self.valueField = date_field


class Payload:

    def __init__(self, objects, fields, size=50, number=1, total_records=0, search={}, sort={}) -> None:
        self.objects = [str(objects)]
        self.fields = [str(fields)]
        self.page = {
            "size": size,
            "number": number,
            "total_records": total_records
        }
        self.search = search
        self.sort = sort


# class DataGrid:
#     def __init__(self, id, config,  type="datagrid"):
#         self.id = id
#         self.type = "datagrid"
#         self.config = config


# class Config(DataGrid):
#     def __init__(self, table_name, rowId, title='', recordId='', dateRangeEndId='', dateRangeStartId=''):
#         super().__init__(table_name)
#         self.config['recordId'] = recordId
#         self.config['rowId'] = rowId
#         self.config['title'] = title
#         self.config['dateRangeStartId'] = dateRangeStartId
#         self.config['dateRangeEndId'] = dateRangeEndId
#         self.config['columns'] = []
#         self.config['actions'] = ACTIONS
#         self.config['bulkActions'] = BULKACTIONS
#         self.config['toolbarActions'] = TOOLBARACTIONS

#     def build_initial_state(self):
#         self.config["initialState"] = InitialState()

#     def build_payload(self, table_name, objects, fields):
#         config_payload = ConfigPayload(objects=objects)
#         for field in fields:
#             field = f"{table_name}.{field.name}"
#             config_payload.fields.append(field)
#         self.config["payload"] = config_payload

#     def build_modal_config(self, table, customize_item_label=None):
#         builder = ModalConfigBuilder(customize_item_label)
#         modal_config = builder.build(table=table)
#         self.config["modalConfig"] = modal_config
