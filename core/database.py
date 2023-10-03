#import the python packages
import databases
import sqlalchemy
from environs import Env
from databases import Database


# SQLAlchemy specific code, as with any other app
env = Env()
env.read_env()
db = env("DATABASE")
user = env("USER")
password = env("PASSWORD")
host = env("HOST")
dbname = env("DBNAME")
port = env("PORT")
schema = env("DBSCHEMA")

# Database connection
# database = db.Database(user, password, host, dbname, port)
DATABASE_URL = f"""postgresql+asyncpg://postgres:{password}@{host}:{port}/{dbname}"""
database = Database(DATABASE_URL)
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)


def get_database() -> Database:
    return database




