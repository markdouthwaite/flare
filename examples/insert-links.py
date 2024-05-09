import json

import requests

HTML_LINKS = [
    "https://arstechnica.com/information-technology/2024/02/report-sam-altman-seeking-trillions-for-ai-ch",
    "https://blog.eladgil.com/p/early-days-of-ai",
    "https://openai.com/research/building-an-early-warning-system-for-llm-aided-biological-threat-creatio",
    "https://simonwillison.net/2023/Dec/31/ai-in-2023/",
    "https://blog.research.google/2024/01/mobilediffusion-rapid-text-to-image.html",
    "https://zwischenzugs.com/2023/12/27/what-i-learned-using-private-llms-to-write-an-undergraduate-hist",
    "https://austinhenley.com/blog/copilotpainpoints.html",
    "https://jackcook.com/2024/02/23/mamba.html",
]

ARXIV_LINKS = [
    "https://arxiv.org/abs/2312.14769",
    "https://arxiv.org/abs/2401.15935",
    "https://arxiv.org/abs/2401.13802",
]


GITHUB_LINKS = [
    "https://github.com/google/space",
    "https://github.com/questdb/time-series-streaming-analytics-template",
]


for link in HTML_LINKS:
    response = requests.post(
        "http://localhost:8080/links/extract",
        headers={"content-type": "application/json"},
        data=json.dumps({"url": link}),
    )
    print(response.status_code, response.content)
