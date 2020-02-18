import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/product_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or "redis://h:p8c976cdec6005aa7a877bc3923ee137b8bafd71d495bb8f28f313428f4f8ba0e@ec2-3-226-204-177.compute-1.amazonaws.com:18969"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xyzhaksdasdkb123'

