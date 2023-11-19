import json
import gzip
import os

import sqlalchemy.exc

from src.common import backends
from src.common.normalize import normalize_legacy_record
from src.commands.content import insert_content
from src.commands.user import get_user

ADMIN_ID = "23717269e6144d8e995c7541a39b648c"
EMBED_MODEL = os.environ["FLARE_EMBED_MODEL"]
BACKEND = "default"


user_repo, content_repo, _ = backends.initialize(BACKEND)

buffer = gzip.open("data/development/exports_resource-snapshot.jsonl.gz", mode="rb")

with buffer as file:
    data = file.read().decode("utf-8")
    rows = data.split("\n")
    rows = [json.loads(_.strip()) for _ in rows if len(_) > 0][586:]

user = get_user(user_repo, ADMIN_ID)

count = 0
for i, row in enumerate(rows):
    if row["provider"] == "github":
        count += 1
    # normalized_record = normalize_legacy_record(row)
    # if normalized_record is not None and normalized_record.metadata[
    #     "locale"
    # ].startswith("en"):
    #     print(i + 1, normalized_record.url)
    #     try:
    #         insert_content(
    #             user, content_repo, normalized_record, embedding_model=EMBED_MODEL
    #         )
    #     except sqlalchemy.exc.IntegrityError:
    #         pass
print(count)