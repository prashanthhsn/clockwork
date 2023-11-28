from tabs.grid_builder.builder import GridBuilder, Grid
from enum import Enum


class Tabs:

    def __init__(self, config, id="tabs", type="tab_layout") -> None:
        self.id: str = id
        self.type: str = type
        self.config: Config = config


class Config:

    def __init__(self) -> None:
        self.tabs = []


class Tab:

    def __init__(self) -> None:
        self.id: str
        self.label: str
        self.grids: Grid

    def set_id(self, id):
        self.id = id

    def set_label(self, label):
        self.label = label

    def set_grids(self, table, customize_item_label):
        grid_builder = GridBuilder(customize_item_label)
        self.grids = grid_builder.build(table=table)
