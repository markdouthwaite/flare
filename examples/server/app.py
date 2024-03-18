from flare.api import initialize_app as initialize_flare_app

import settings

flask_app = initialize_flare_app(settings.rich_link_extractors, settings.rich_link_repo)

if __name__ == "__main__":
    flask_app.run("0.0.0.0", port=8080)
