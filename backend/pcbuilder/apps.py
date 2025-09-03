from django.apps import AppConfig

class PCBuilderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pcbuilder'
    label = 'builder' # apps name used to be 'builder'
