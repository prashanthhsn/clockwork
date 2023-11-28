from tabs.grid_builder.utils import *
from tabs.grid_builder.config import *
from database_include_exclude import FIELDS_TO_EXCLUDE


class GridBuilder:
    def __init__(self, customize_item_label=None):
        self.customize_item_label = customize_item_label
        # datagrid properties
        self.id = None
        self.config = None

    def build(self, table):
        return self.set_id(id=table.name).set_config(table=table).build_grid_config()

    def build_grid_config(self):
        return Grid(id=self.id, config=self.config)

    def set_id(self, id):
        self.id = id
        return self

    def set_config(self, table):
        builder = ConfigBuilder()
        config = builder.build(table=table)
        self.config = config
        return self
