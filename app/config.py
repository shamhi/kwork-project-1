from dotenv import dotenv_values


env = dotenv_values()


def getenv(key, rtype, default=None):
    value = env.get(key)
    if not value:
        return default

    return rtype(value)


class Config:
    TOKEN = getenv('TOKEN', str)
