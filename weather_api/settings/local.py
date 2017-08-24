try:
	from .base import *
except ImportError:
	pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't(m3r5n&r9mywcxy2^tq8s@nh2)2)0n#%o%w+xg4x*g#ydexvh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}