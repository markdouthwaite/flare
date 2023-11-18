"""
POST /feed
GET  /feed/{feed-id}/content  # get the feed!
PUT  /feed/{feed-id}/content/{content-id}  # update (e.g. publish/make non-public)
POST /feed/{feed-id}/content  # add content to the feed (inc. summarize, score)
GET  /feed/{feed-id}/tags     # get tags for the feed
GET  /feed/{feed-id}/tags/{tag-id}  # get tag info
POST /feed/{feed-id}/tags     # list tags
"""

raw_content = [
    {
        "url": "https://ghost.org/docs/content-api",
        "title": "",
        "body": "",
        "featured": False,
        "visibility": "public",
        "read_time": 1,
        "og_image": None,
        "og_title": None,
        "og_description": None,
        "tags": [
            {
                "id": "f1a4fd1bbcee40f980414b479e22850a"
            }
        ]
    }
]


content = [
    {
        "id": "2e2eae5546194c308fbd75b216473103",
        "url": "https://ghost.org/docs/content-api",
        "title": "",
        "body": "",
        "summary": "",
        "featured": False,
        "visibility": "public",
        "created_at": "2023-11-04T15:43:07",
        "updated_at": "2023-11-04T15:43:07",
        "published_at": "2023-11-04T15:43:07",
        "read_time": 1,
        "score": 7,
        "og_image": None,
        "og_title": None,
        "og_description": None,
        "tags": [
            {
                "id": "f1a4fd1bbcee40f980414b479e22850a",
                "name": "GitHub",
                "visibility": "public"
            }
        ]
    }
]


tags = [
    {
        "id": "f1a4fd1bbcee40f980414b479e22850a",
        "name": "GitHub",
        "visibility": "public",
        "tagger": "taggers.GitHub"
    }
]


feeds = [
    {
        "id": "machine-learning",
        "scorer": {
            "callable": "scorers.MachineLearning",
            "parameters": {}
        },  # scores content at load-time for relevance
        "ranker": {
            "callable": "rankers.MachineLearning",
            "parameters": {}
        },  # maintains feed
        "summarizer": {
            "callable": "summarizers.OpenAI"
        },
        "workers": [

        ],  # background workers that can check for updates to source content,
            # publish content etc.
        "created_at": "2023-11-04T15:43:07"
    }
]