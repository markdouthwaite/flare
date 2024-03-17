from flare.api import init_app
from functools import partial
from firebase_admin import initialize_app
from flare.db.links.firestore import FirestoreRichLinkRepository
from flare.core.links import init_rich_link_extractor
from flare.core.extractors import html, github, arxiv
from flare.core.models.links import RichLinkConfig
from flare.core.models.filters import LinkFilterSet, ExtractedLinkFilterSet
from flare.core.validators.generic import is_topic, is_allowed, is_english_language, is_existing
from flare.core.validators.github import (
    is_active_repo,
    is_not_malware_repo,
    is_popular_repo,
)
from flare.core.keywords import machine_learning
from openai import OpenAI
import json

openai_client = OpenAI()


def completion(text: str, *, client: OpenAI, system_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content


summarise_prompt = """
"You are an expert copy editor for a science magazine. 
You are reviewing stories for inclusion in your online magazine. 
You need to write a short abstract for the following to act as the article summary on 
your website. The summary cannot exceed 50 words. Use a relaxed tone of voice, but not 
too informal. Do not use emojis."
"""

score_prompt = """
You are an expert editor for a machine learning magazine aimed at machine learning 
engineers and product people interested in artificial intelligence. You are able to give 
a interest score to any text passed to you. The text you receive may be articles, 
scientific paper abstracts or code repositories. 

Give your response in JSON format with the following schema with no other formatting:

{ "score": number (0-100) }
"""

firebase_app = initialize_app()

rich_link_repo = FirestoreRichLinkRepository(firebase_app, "rich_links")

summarizer = partial(completion, system_prompt=summarise_prompt, client=openai_client)

machine_learning_relevance = lambda _: (
    "machine-learning-relevance",
    json.loads(
        completion(_.text.value, client=openai_client, system_prompt=score_prompt,)
    )["score"],
)

rich_link_extractors = {
    "html": init_rich_link_extractor(
        link_extractor=html.extract,
        link_extractor_config={},
        rich_link_config=RichLinkConfig(
            summarizer=summarizer, attribute_scorers=[machine_learning_relevance],
        ),
        rich_link_repo=rich_link_repo,
        link_filter_set=LinkFilterSet(
            filters=[partial(is_allowed, block_list=["youtube.com"]), is_existing]
        ),
        extracted_link_filter_set=ExtractedLinkFilterSet(
            filters=[
                is_english_language,
                partial(is_topic, keyword_list=machine_learning.KEYWORDS),
            ]
        ),
    ),
    "github": init_rich_link_extractor(
        link_extractor=github.extract,
        link_extractor_config={},
        rich_link_config=RichLinkConfig(
            summarizer=summarizer, attribute_scorers=[machine_learning_relevance],
        ),
        rich_link_repo=rich_link_repo,
        link_filter_set=LinkFilterSet(
            filters=[is_existing]
        ),
        extracted_link_filter_set=ExtractedLinkFilterSet(
            filters=[
                is_not_malware_repo,
                is_active_repo,
                is_popular_repo,
                is_english_language,
                partial(is_topic, keyword_list=machine_learning.KEYWORDS),
            ]
        ),
    ),
    "arxiv": init_rich_link_extractor(
        link_extractor=arxiv.extract,
        link_extractor_config={},
        rich_link_config=RichLinkConfig(
            summarizer=summarizer, attribute_scorers=[machine_learning_relevance],
        ),
        rich_link_repo=rich_link_repo,
        link_filter_set=LinkFilterSet(
            filters=[is_existing]
        ),
        extracted_link_filter_set=ExtractedLinkFilterSet(
            filters=[
                is_english_language,
                partial(is_topic, keyword_list=machine_learning.KEYWORDS),
            ]
        ),
    ),
}

flask_app = init_app(rich_link_extractors, rich_link_repo)

if __name__ == "__main__":
    flask_app.run("0.0.0.0", port=8080)
