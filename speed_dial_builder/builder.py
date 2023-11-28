from speed_dial_builder.utils import *


class SpeedDialBuilder:

    def __init__(self) -> None:
        self.speed_dial = SpeedDial()

    def build(self, table):
        self.set_id()
        self.build_config(table)
        return self.speed_dial

    def set_id(self, id="speed_dial_id"):
        self.speed_dial.id = id

    def build_config(self, table, label=None):
        self.speed_dial.config = Config(label=label, table=table)
