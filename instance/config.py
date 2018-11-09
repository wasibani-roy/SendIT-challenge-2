class BaseConfig(object):
    """Commmon configurations that are common across all environments"""
    Debug = True


class TestingConfig(BaseConfig):
    Testing = True


class DevelopmentConfig(BaseConfig):
    """
    Development configuartions

    """
    Debug = True
    Testing = True


class ProductionConfig(BaseConfig):
    """
    Production configuarations

    """
    Debug = False

    Testing = False


app_config = {
    "development": DevelopmentConfig,
    "Testing": TestingConfig,
    "production": ProductionConfig
}
