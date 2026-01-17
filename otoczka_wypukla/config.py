class Config:
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
