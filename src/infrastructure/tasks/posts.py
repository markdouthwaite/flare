from celery import current_app, shared_task
from src.commands.posts import extract_and_load_post as _extract_and_load_post


@shared_task(ignore_result=True)
def extract_and_load_post(post_id: str, url: str, source_name: str):
    print(current_app.conf)
    _extract_and_load_post(
        post_id,
        url,
        source=current_app.conf.SOURCES[source_name],
        repo=current_app.conf.POSTS_REPO,
    )
