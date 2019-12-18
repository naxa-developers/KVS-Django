
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'kvs_db',
        'USER': 'postgres',
        "PASSWORD": '',
        'HOST': '172.19.0.2',
        'PORT': '5432'
    }
}
