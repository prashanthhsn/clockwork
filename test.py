from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from schema_builder.schema_builder import SchemaBuilder
import json

if __name__ == "__main__":
    engine = create_engine('postgresql://betra:betra@localhost/clockwork')
    metadata = MetaData()
    metadata.reflect(engine)
    Base = automap_base(metadata=metadata)
    Session = sessionmaker(bind=engine)
    session = Session()
    table = metadata.tables.get('time_entry')
    builder = SchemaBuilder()
    schema_obj = builder.build(table=table)
    schema = json.dumps(schema_obj, default=lambda item: item.__dict__)
    print('built!', schema)