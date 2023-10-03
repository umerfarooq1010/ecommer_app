
# Importing Python packages
from environs import Env


# -----------------------------------------------------------------------------


# Env Object to read from env file
env = Env()
env.read_env()

# JWT Constants
ALGORITHM = env("ALGORITHM")
SECRET_KEY = env("SECRET_KEY")

# Access Token Expire Time
ACCESS_TOKEN_EXPIRE_MINUTES = env("ACCESS_TOKEN_EXPIRE_MINUTES")
ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)

# Cors
CORS_ORIGIN_ALL = env("CORS_ORIGIN_ALL")
CORS_ALLOW_METHODS = env("CORS_ALLOW_METHODS")
CORS_ALLOW_HEADERS = env("CORS_ALLOW_HEADERS")

