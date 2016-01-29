import os

import config_secret as cs

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = cs.SECRET_KEY
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    APP_MAIL_SUBJECT_PREFIX = '[Flasky]'
    APP_MAIL_SENDER = cs.APP_MAIL_SENDER
    MAIL_USERNAME = cs.MAIL_USERNAME
    MAIL_PASSWORD = cs.MAIL_PASSWORD
    MAIL_SERVER = cs.MAIL_SERVER
    MAIL_PORT = cs.MAIL_PORT
    APP_ADMIN = cs.APP_ADMIN
    APP_POSTS_PER_PAGE = 20
    APP_FOLLOWERS_PER_PAGE = 20
    APP_FOLLOWING_PER_PAGE = 20
    APP_COMMENTS_PER_PAGE = 20
    BOOTSTRAP_SERVE_LOCAL = True
    APP_SLOW_DB_QUERY_TIME = 0.5

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = cs.MAIL_SERVER
    MAIL_PORT = cs.MAIL_PORT
    MAIL_USE_TLS = True
    MAIL_USERNAME = cs.MAIL_USERNAME
    MAIL_PASSWORD = cs.MAIL_PASSWORD
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # Email errors to administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.APP_MAIL_SENDER,
            toaddrs=[cls.APP_ADMIN],
            subject=cls.APP_MAIL_SUBJECT_PREFIX + 'Application Error',
            credentials=credentials,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stdere
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig,
}
