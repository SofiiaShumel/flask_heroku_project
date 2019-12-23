from root.entities import *
from root.database import *


db = Database()

Base.metadata.create_all(db.sqlaclchemy_engine)


