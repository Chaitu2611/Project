class Config(object):
    DEBUG=False
    TESTING=False

    DATABASE="naukri"
    PASSWORD="2611"
    HOST="localhost"
    USER="postgres"
    PORT="5432"
    

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG=True

    DATABASE="naukri"
    PASSWORD="2611"
    HOST="localhost"
    USER="postgres"
    PORT="5432"


class TestingConfig(Config):
    TESTING=True

    DATABASE="naukri"
    PASSWORD="2611"
    HOST="localhost"
    USER="postgres"
    PORT="5432"
