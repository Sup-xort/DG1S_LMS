from .base import *

ALLOWED_HOSTS = ['10.72.120.132', 'dg1s.pythonanywhere.com']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = True
MIDDLEWARE += ['django.middleware.clickjacking.XFrameOptionsMiddleware', ]
X_FRAME_OPTIONS = 'http://www.dg1s.o-r.kr/'
