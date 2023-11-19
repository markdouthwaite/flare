from src.commands.user import get_user
from src.commands.content import insert_content
from src.infrastructure.repositories.sqlite import (
    SQLiteUserRepository,
    SQLiteContentRepository,
)

user_repo = SQLiteUserRepository(database="sqlite:///flare.db")

user_id = create_user(
    user_repo,
    name="The Differential",
    slug="thedifferential",
    email="mark@douthwaite.io",
)
