Plugins:
pylint-django
django-ckeditor

-- Pylint relative dirs imports está bugeado
    A continuación los comandos de pylint
     para evitar que pylint declare error:
     
    - # pylint: disable=import-error