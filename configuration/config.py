from configuration.request_formatter import RequestFormatter
from flask import Flask
from flask.logging import default_handler

def configure(app: Flask):
    app.config.update(
        TESTING=True,
        SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'  # this should be extracted to a secret
    )
    
    formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
    default_handler.setFormatter(formatter)
    
