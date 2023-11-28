from database_include_exclude import FIELDS_TO_EXCLUDE

class ColumnType:
    VARCHAR = 'VARCHAR'
    AUTOCOMPLETE = 'AUTOCOMPLETE'
    DATE = 'DATE'
    BOOLEAN = 'BOOLEAN'
    TIMESTAMP = 'TIMESTAMP'
    INTEGER = 'INTEGER'


class Item():

    def __init__(self, id) -> None:
        self.id: str = id
        self.label: str = None
        self.fullWidth = True


class TextItem(Item):

    def __init__(self, id, label) -> None:
        super().__init__(id)
        self.type = 'string'
        self.multiline = True
        self.label = label

    def set_max_length(self, max_length):
        self.max_length = max_length


class NumberItem(Item):

    def __init__(self, id, label) -> None:
        super().__init__(id)
        self.type = 'number'
        self.label = label

    def set_max_value(self, max_value):
        self.max_value = max_value


class DateItem(Item):

    def __init__(self, id, label) -> None:
        super().__init__(id)
        self.type = 'datetime'
        self.label = label


class AutocompleteItem(Item):

    def __init__(self, id, label) -> None:
        super().__init__(id)
        self.type = 'autocomplete'
        self.clearable = True
        self.readOnly = True
        self.options = "api"
        self.label = label

    def set_prefixId(self, prefixId=None):
        self.prefixId = prefixId

    def set_groupKey(self, groupKey=None):
        self.groupKey = groupKey

    def set_payload(self, objects, fields):
        self.payload = Payload(objects, fields)


class BooleanItem(Item):

    def __init__(self, id, label) -> None:
        super().__init__(id)
        self.type = 'boolean'
        self.label = label


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


class Required:
    def __init__(self) -> None:
        pass


class ErrorMessage:

    def __init__(self) -> None:
        self.required = Required()


class Validation:

    def __init__(self, properties={}, required=[]) -> None:
        self.additional_properties = True
        self.properties = properties
        self.required = required
        self.errorMessage = ErrorMessage()
        self.type = "object"


class KeyMap:

    def __init__(self) -> None:
        pass


class ModalConfig:

    def __init__(self,recordId,idKey,object,keyMap,items,valdiation,hideHeader=True) -> None:
        self.recordID = recordId
        self.idKey = idKey
        self.object = object
        self.hideHeader = hideHeader
        self.keyMap = keyMap
        self.items = items
        self.validation = valdiation
