from flare.core.models.links import RichLink

from supabase import create_client


class SupabaseRichLinkRepository:
    def __init__(self, url: str, key: str):
        self._client = create_client(url, key)

    def get(self, rich_link_id: str) -> RichLink:
        response = self._client.table('links').select("*").eq("id", rich_link_id).execute()
        print(response)
        return RichLink(**response["data"][0])

    def insert(self, rich_link: RichLink):
        self._client.table("links")
        self._client.table("links").insert(
            rich_link.dict()
        ).execute()
