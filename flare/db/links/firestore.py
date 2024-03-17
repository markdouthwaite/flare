from firebase_admin import firestore, App as FirebaseApp
from flare.core.models.links import RichLink
from flare.core.errors import RichLinkRepositoryWriteError
from google.cloud.firestore_v1.base_query import FieldFilter


class FirestoreRepository:
    def __init__(self, app: FirebaseApp, collection_name: str):
        self.client = firestore.client(app)
        self.collection_name = collection_name

    @property
    def _collection(self):
        return self.client.collection(self.collection_name)


class FirestoreRichLinkRepository(FirestoreRepository):
    def get(self, rich_link_id: str) -> RichLink:
        doc_ref = self._collection.document(rich_link_id)
        return RichLink(**doc_ref.get().to_dict())

    def insert(self, rich_link: RichLink):
        if self.exists(rich_link.url):
            raise RichLinkRepositoryWriteError(
                f"url '{rich_link.url}' already exists in rich link repository"
            )

        doc_ref = self._collection.document(rich_link.id)
        payload = rich_link.dict()
        doc_ref.set(payload)

    def exists(self, rich_link_url: str) -> bool:
        existing = self._collection.where(
            filter=FieldFilter("url", "==", rich_link_url)
        ).stream()

        if any(existing):
            return True
        else:
            return False
