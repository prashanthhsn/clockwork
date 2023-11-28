SPEED_DIAL_TYPE = "speed_dial"


class ItemType:
    VARCHAR = 'VARCHAR'
    AUTOCOMPLETE = 'AUTOCOMPLETE'
    # DATE = 'DATE'
    # BOOLEAN = 'BOOLEAN'
    # TIMESTAMP = 'TIMESTAMP'


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


class Payload():

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


class Item:

    def __init__(self, id) -> None:
        self.id = id
        self.fullWidth = True


class TextItem(Item):

    def __init__(self, id, label=None) -> None:
        super().__init__(id)
        self.type = "string"
        self.label = label


class AutocompleteItem(Item):

    def __init__(self, id, label=None) -> None:
        super().__init__(id)
        self.prefixId = None
        self.type = "autocomplete"
        self.clearable = True
        self.label = label
        self.readOnly = True
        self.options = "api"
        self.groupKey = None

    def set_payload(self, objects, fields):
        self.payload = Payload(objects=objects, fields=fields)

    def set_prefixId(self, prefixId):
        self.prefixId = prefixId

    def set_groupKey(self, groupKey):
        self.groupKey = groupKey


class Items:

    def __init__(self, customize_label=None) -> None:
        self.customize_label = customize_label
        self.type_to_method = {
            ItemType.VARCHAR: self.build_text_item_config,
            ItemType.AUTOCOMPLETE: self.build_autocomplete_item_config,
        }
        self.items = []

    def check_item_type(self, item):
        item_type = str(item.type).split(
            '(')[0] if '(' in str(item.type) else str(item.type)
        return item_type if not item.foreign_keys else ItemType.AUTOCOMPLETE

    def build(self, items):
        for item in items:
            item_type = self.check_item_type(item)
            if item_type in self.type_to_method:
                method = self.type_to_method[item_type]
                self.items.append(method(item))
        return self.items

    def get_label(self, item):
        if not self.customize_label:
            return f"{item.table.name}.{item.name}"
        else:
            return self.customize_label(item)

    def build_text_item_config(self, item):
        label = self.get_label(item=item)
        item_obj = AutocompleteItem(id=item.name, label=label)
        for fkey in item.foreign_keys:
            item_obj.set_payload(objects=fkey._table_key(),
                                 fields=fkey.target_fullname)
        return item_obj

    def build_autocomplete_item_config(self, item):
        label = self.get_label(item=item)
        item_obj = TextItem(id=item.name, label=label)
        return item_obj


class Config:

    def __init__(self, label, table) -> None:
        self.label = label
        self.actions = [Actions(table=table, id=table.name, object=table.name)]


class Actions:

    def __init__(self, id, object, table, recordId=None, view=None, type="form", icon=None, label=None) -> None:
        self.id = id
        self.view = view
        self.type = type
        self.icon = icon
        self.label = label
        self.record_id = recordId
        self.items = self.build_items_config(table=table)
        self.object = object
        self.validation = Validation()

    def build_items_config(self, table):
        items = Items()
        items = items.build(items=table.columns._all_columns)
        return items


class SpeedDial:

    id: str
    type: str
    config: Config

    def __init__(self) -> None:
        self.type = SPEED_DIAL_TYPE
