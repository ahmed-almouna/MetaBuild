from django.apps import AppConfig

class PCBuilderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pcbuilder'
    label = 'builder' # the app's name used to be 'builder' this helps with db migrations
