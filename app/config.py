class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///{name}.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI.format(name="app")


class DevConfig(Config):
    """
    Statement for enabling the development environment
    """
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI.format(name="dev")


class TestConfig(Config):
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI.format(
        name="test"
    )


config = {
    "base": Config,
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig
}
