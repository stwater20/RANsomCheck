import threading

class FlaskThread(threading.Thread):
    def __init__(self, app, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: Flask = app  # type: ignore[attr-defined]

    def run(self) -> None:
        with self.app.app_context():
            super().run()