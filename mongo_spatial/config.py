class BaseConfig(object):
    ADMINS = []
    DEBUG = True
    TESTING = False
    VERBOSE = False
    PROPAGATE_EXCEPTIONS = True

    SENTRY_DSN = ""
    SENTRY_RELEASE = "v0.1-rc1"

    SQLALCHEMY_DATABASE_URI = ''


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://basic_auth:eJTy5mn7shrHmU9c@localhost/basic_auth'


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ''


class StagingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ''


class ProductionConfig(BaseConfig):
    pass


config = {
    "development": "mongo_spatial.config.DevelopmentConfig",
    "testing": "mongo_spatial.config.TestingConfig",
    "staging": "mongo_spatial.config.StagingConfig",
    "production": "mongo_spatial.config.ProductionConfig"
}
