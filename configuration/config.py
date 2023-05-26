def configure(app):
    app.config.update(
        TESTING=True,
        SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'  # this should be extracted
    )
