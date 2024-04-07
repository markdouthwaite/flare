from typing import Optional

from firebase_admin import App as FirebaseApp
from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter, Query

from flare.core.errors import RichLinkRepositoryReadError, RichLinkRepositoryWriteError
from flare.core.models.links import RichLink, RichLinkSet
from flare.core.models.queries import QueryFilterSet, QueryOrderBy


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

    def list(
        self,
        filter_set: Optional[QueryFilterSet] = None,
        order_by: Optional[QueryOrderBy] = None,
        limit: Optional[int] = None,
    ) -> RichLinkSet:
        query = self._collection

        if filter_set is not None:
            for f in filter_set.filters:
                query = query.where(filter=FieldFilter(f.field, f.operator, f.value))

        if order_by is not None:
            if order_by.direction == "desc":
                direction = Query.DESCENDING
            elif order_by.direction == "asc":
                direction = Query.ASCENDING
            else:
                raise RichLinkRepositoryReadError(
                    f"invalid order_by direction '{order_by.direction}"
                )

            query = query.order_by(order_by.field, direction=direction)

        if limit is not None:
            query = query.limit(limit)

        results = query.stream()

        return RichLinkSet(links=[RichLink(**doc.to_dict()) for doc in results])

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
