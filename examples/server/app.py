import settings

from flare.api import initialize_app as initialize_flare_app

flask_app, celery_app = initialize_flare_app(settings)

if __name__ == "__main__":
    flask_app.run("0.0.0.0", port=8080)
