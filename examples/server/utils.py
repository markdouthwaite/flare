import json
from typing import Tuple

from openai import OpenAI

from flare.core.models.links import ExtractedLink

openai_client = OpenAI()


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


def summarize(text: str) -> str:
    return completion(text, client=openai_client, system_prompt=summarise_prompt)


def score(attribute: str, link: ExtractedLink, system_prompt: str) -> Tuple[str, float]:
    response = completion(
        link.text.value, client=openai_client, system_prompt=system_prompt
    )
    score = json.loads(response)["score"]
    return attribute, score


def machine_learning_relevance(link: ExtractedLink) -> Tuple[str, float]:
    return score("machine_learning_relevance", link, score_prompt)
