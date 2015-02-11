"""
Django settings for jukebox2web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, '../Media/')
MEDIA_URL = '/media/'

MUSIC_TYPES = [
'audio/vorbis-config', 'audio/vorbis', 'audio/vnd.vmx.cvsd', 'audio/vnd.sealedmedia.softseal-mpeg', 'audio/vnd.rip',
'audio/vnd.rhetorex.32kadpcm', 'audio/vnd.qcelp', 'audio/vnd.octel.sbc', 'audio/vnd.nuera.ecelp9600',
'audio/vnd.nuera.ecelp7470', 'audio/vnd.nuera.ecelp4800', 'audio/vnd.nortel.vbk', 'audio/vnd.nokia.mobile-xmf',
'audio/vnd.ms-playready.media.pya', 'audio/vnd.lucent.voice', 'audio/vnd.hns.audio', 'audio/vnd.everad.plj',
'audio/vnd.dvb.file', 'audio/vnd.dts.hd', 'audio/vnd.dts', 'audio/vnd.dra', 'audio/vnd.dolby.pulse.1',
'audio/vnd.dolby.pl2z', 'audio/vnd.dolby.pl2x', 'audio/vnd.dolby.pl2', 'audio/vnd.dolby.mps', 'audio/vnd.dolby.mlp',
'audio/vnd.dolby.heaac.2', 'audio/vnd.dolby.heaac.1', 'audio/vnd.dlna.adts', 'audio/vnd.digital-winds',
'audio/vnd.dece.audio', 'audio/vnd.cns.inf1', 'audio/vnd.cns.anp1', 'audio/vnd.cmles.radio-events',
'audio/vnd.cisco.nse', 'audio/vnd.CELP', 'audio/vnd.audiokoz', 'audio/vnd.4SB', 'audio/vnd.3gpp.iufp', 'audio/VMR-WB',
'audio/VDVI', 'audio/ulpfec', 'audio/UEMCLIP', 'audio/tone', 'audio/telephone-event', 'audio/t38', 'audio/t140c',
'audio/speex', 'audio/sp-midi', 'audio/SMV-QCP', 'audio/SMV0', 'audio/SMV', 'audio/rtx', 'audio/rtp-midi',
'audio/rtploopback', 'audio/rtp-enc-aescm128', 'audio/RED', 'audio/raptorfec', '', 'audio/prs.sid', 'audio/PCMU-WB',
'audio/PCMU', 'audio/PCMA-WB', 'audio/PCMA', '', 'audio/ogg', 'audio/mpeg4-generic', 'audio/mpeg', 'audio/mpa-robust',
'audio/MP4A-LATM', 'audio/mp4', 'audio/MPA', 'audio/mobile-xmf', 'audio/LPC', 'audio/L24', 'audio/L20', 'audio/L16',
'audio/L8', 'audio/ip-mr_v2.5', 'audio/iLBC', 'audio/GSM-HR-08', 'audio/GSM-EFR', 'audio/GSM', 'audio/G729E',
'audio/G729D', '', 'audio/G729', 'audio/G728', 'audio/G726-40', 'audio/G726-32', 'audio/G726-24', 'audio/G726-16',
'audio/G723', 'audio/G722', 'audio/G721', '', 'audio/G719', 'audio/fwdred', 'audio/example', 'audio/EVRCWB1',
'audio/EVRCWB0', 'audio/EVRCWB', 'audio/EVRCNW1', 'audio/EVRCNW0', 'audio/EVRCNW', 'audio/EVRCB1', 'audio/EVRCB0',
'audio/EVRCB', 'audio/EVRC1', 'audio/EVRC0', 'audio/EVRC-QCP', 'audio/EVRC', 'audio/encaprtp', 'audio/eac3',
'audio/DVI4', 'audio/DV', 'audio/dsr-es202212', 'audio/dsr-es202211', 'audio/dsr-es202050', 'audio/dsr-es201108',
'audio/dls', 'audio/DAT12', 'audio/CN', 'audio/clearmode', 'audio/BV32', 'audio/BV16', 'audio/basic', 'audio/ATRAC3',
'audio/ATRAC-X', 'audio/ATRAC-ADVANCED-LOSSLESS', 'audio/asc', 'audio/aptx', 'audio/amr-wb+', 'audio/AMR-WB',
'audio/AMR', 'audio/ac3', 'audio/3gpp2', 'audio/3gpp', 'audio/32kadpcm', 'audio/1d-interleaved-parityfec']

MAX_UPLOAD_SIZE = 20971520
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_URL = '/static/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's9aw1$(pelyz6q#o(vi99*cv1&%q-6pmbloul3kzh46z&dpo(9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library_manager'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'jukebox2web.urls'

WSGI_APPLICATION = 'jukebox2web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                     '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'production_file':{
            'level' : 'INFO',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : os.path.join(BASE_DIR, './main.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount' : 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_false'],
        },
        'debug_file':{
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : os.path.join(BASE_DIR, './debug.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount' : 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        },
        'null': {
            "class": 'django.utils.log.NullHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['null', ],
        },
        'py.warnings': {
            'handlers': ['null', ],
        },
        '': {
            'handlers': ['console', 'production_file', 'debug_file'],
            'level': "DEBUG",
        },
    }
}


