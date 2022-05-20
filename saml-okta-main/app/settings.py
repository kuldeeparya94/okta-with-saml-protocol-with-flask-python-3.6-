# -*- coding: utf-8 -*-
"""Application configuration settings for different environment"""
import os


class SecretKey(object):
    SECRET_KEY = os.environ.get('APP_SECRET', 'i-fell-not-good')


class AppDirectory(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class Config(SecretKey, AppDirectory):
    ENV = 'dev'
    DEBUG = True


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True

