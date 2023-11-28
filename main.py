from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from tabs.tab_builder.builder import TabsBuilder
from schema.builder import SchemaBuilder
from speed_dial_builder.builder import SpeedDialBuilder
from tabs.grid_builder.builder import GridBuilder

import json


def customize_tab_label(table):
    return 'test.'+table.name


def customize_modal_config_item_label(column):
    return 'test.'+column.table.name+'.'+column.name


if __name__ == "__main__":
    engine = create_engine('postgresql://betra:betra@localhost/clockwork')
    metadata = MetaData()
    metadata.reflect(engine)
    Base = automap_base(metadata=metadata)
    Session = sessionmaker(bind=engine)
    session = Session()
    table = metadata.tables.get('time_entry')
    #####################################
    # builder = TabsBuilder()
    # tab_object = builder.build(table=table)
    # tab_config = json.dumps(tab_object, default=lambda item: item.__dict__)
    # print('built!', tab_config)
    #####################################
    builder = SchemaBuilder()
    # schema_obj = builder.build(table=table)
    schema = json.dumps(builder.build(table=table), default=lambda item: item.__dict__)
    print('built!', schema)
    #####################################
    # builder = SpeedDialBuilder()
    # speed_dial_object = builder.build(table=table)
    # speed_dial_config = json.dumps(speed_dial_object, default=lambda item: item.__dict__)
    # print('built!', speed_dial_config)
    #####################################
    # builder = GridBuilder()
    # grid_object = builder.build(table=table)
    # grid_config = json.dumps(grid_object, default=lambda item: item.__dict__)
    # print('built!', grid_object)
