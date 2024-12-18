from .base import *

ALLOWED_HOSTS = ['10.72.120.132', '']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = False
MIDDLEWARE += ['django.middleware.clickjacking.XFrameOptionsMiddleware', ]
X_FRAME_OPTIONS = 'http://www.dg1s.o-r.kr/'
