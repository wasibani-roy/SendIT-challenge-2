import os

class BaseConfig:
    DEBUG = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(BaseConfig):
    DEBUG = False
    Testing = True

class ProductionConfig(BaseConfig):
    DEBUG = False

app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
