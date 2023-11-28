from tabs.tab_builder.utils import *

TAB_ID = "tabs"
TAB_TYPE = "tab_layout"


class TabsBuilder:

    def __init__(self, customize_tab_label=None, customize_item_label=None) -> None:
        self.customize_tab_label = customize_tab_label
        self.customize_item_label = customize_item_label
        self.config = None

    def build(self, table):
        return self.set_config(table=table).build_tabs()

    def set_config(self, table):
        self.config = Config()
        self.set_tab(table=table)
        return self

    def set_tab(self, table):
        tab = Tab()
        tab.set_id(id=table.name)

        if not self.customize_tab_label:
            tab.set_label(label=None)
        else:
            label = self.customize_tab_label(table=table)
            tab.set_label(label=label)

        tab.set_grids(
            table=table, customize_item_label=self.customize_item_label)
        self.config.tabs.append(tab)

    def build_tabs(self):
        return Tabs(config=self.config)
