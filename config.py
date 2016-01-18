import os

import config_secret as cs

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = cs.SECRET_KEY
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    APP_MAIL_SUBJECT_PREFIX = '[Flasky]'
    APP_MAIL_SENDER = cs.APP_MAIL_SENDER
    APP_ADMIN = cs.APP_ADMIN
    APP_POSTS_PER_PAGE = 20
    APP_FOLLOWERS_PER_PAGE = 20
    APP_FOLLOWING_PER_PAGE = 20
    APP_COMMENTS_PER_PAGE = 20
    BOOTSTRAP_SERVE_LOCAL = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = cs.MAIL_SERVER
    MAIL_PORT = cs.MAIL_PORT
    MAIL_USE_TLS = True
    MAIL_USERNAME = cs.MAIL_USERNAME
    MAIL_PASSWORD = cs.MAIL_PASSWORD
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite'))
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(basedir, 'data.sqlite'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
