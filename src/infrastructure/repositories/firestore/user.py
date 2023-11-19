from src.entities.user import User

from firebase_admin import firestore


class FireStoreUserRepository:
    def __init__(self, app=None):
        self.db = firestore.client(app)

    def create(self, user: User):
        user_ref = self.db.collection("users").document(user.id)
        user_ref.set(user.dict())
