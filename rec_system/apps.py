from django.apps import AppConfig

class RecSystemConfig(AppConfig):
    """ Загрузка графа из БД """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rec_system'

    def ready(self):
        from .graph import load_graph_from_db
        import sys
        if 'migrate' not in sys.argv and 'makemigrations' not in sys.argv:
            load_graph_from_db()