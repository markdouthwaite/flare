import json
import random
from dataclasses import asdict
from datetime import datetime, timedelta

from faker import Faker
from faker.providers import DynamicProvider

from flare.common.identifier import generate_id
from flare.entities import Post, Tag

tech_use_cases_prefix_provider = DynamicProvider(
    provider_name="tech_use_case_prefix",
    elements=[
        "fast",
        "simple",
        "basic",
        "minimal",
        "advanced",
        "lite",
        "flask",
        "fastapi",
        "aws",
        "azure",
        "gcp",
    ],
)

tech_buzzwords_provider = DynamicProvider(
    provider_name="tech_buzzword",
    elements=[
        "tensorflow",
        "genai",
        "agent",
        "python",
        "pytorch",
        "llm",
        "k8s",
        "webassembly",
        "rust",
        "neural-network",
        "keras",
        "diffusion",
        "vector",
        "docker",
    ],
)

tech_use_cases_provider = DynamicProvider(
    provider_name="tech_use_case",
    elements=["chatbot", "service", "database", "pipeline", "app", "application"],
)

programming_language_provider = DynamicProvider(
    provider_name="programming_language",
    elements=["Python", "Rust", "C++", "Golang", "R", "C#", "bash", "Jupyter Notebook"],
)


computer_science_prefix = DynamicProvider(
    provider_name="cs_prefix",
    elements=[
        "Fast",
        "Simple",
        "Easy",
        "Supervised",
        "Unsupervised",
        "Deep",
        "Genetic",
        "Efficient",
        "Hybrid",
        "Complex",
        "Semi-supervised",
        "Self-supervised",
        "Evolutionary",
    ],
)


computer_science_term = DynamicProvider(
    provider_name="cs_term",
    elements=[
        "Time Series",
        "Algorithms",
        "Graph",
        "Traversal",
        "Tree",
        "Quadratic",
        "Regressive",
        "Automated",
        "Neural Network",
        "Transformer",
        "Data Structures",
        "Compiler Technology",
        "Architecture",
    ],
)

computer_science_suffix = DynamicProvider(
    provider_name="cs_suffix",
    elements=[
        "Classifier",
        "Classification",
        "for Large Language Models",
        "by Neuroevolution",
        "in Dynamical Systems",
        "for Humans",
        "for Human-like Behaviours",
        "using Python",
        "using Javascript",
        "with Time Windows",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ],
)


article_prefix = DynamicProvider(
    provider_name="article_prefix",
    elements=[
        "A Gentle Introduction to",
        "Brief Intro to",
        "Beginners Guide to",
        "Overview of",
        "Deep Dive Into",
        "Explainer:",
        "How To:",
    ],
)


article_suffix = DynamicProvider(
    provider_name="article_suffix",
    elements=[
        "for GCP",
        "for AWS",
        "for Kubernetes",
        "for Azure",
        "for Idiots",
        "",
        "",
        "",
        "for Beginners",
    ],
)


fake = Faker()
fake.add_provider(tech_buzzwords_provider)
fake.add_provider(tech_use_cases_provider)
fake.add_provider(tech_use_cases_prefix_provider)
fake.add_provider(programming_language_provider)
fake.add_provider(computer_science_prefix)
fake.add_provider(computer_science_term)
fake.add_provider(computer_science_suffix)
fake.add_provider(article_prefix)
fake.add_provider(article_suffix)


def github_repo_name():
    return (
        f"{fake.tech_use_case_prefix()}-{fake.tech_buzzword()}-{fake.tech_use_case()}"
    )


def github_repo_owner():
    return fake.company().lower().replace(" ", "-").replace(",", "")


def paper_name():
    return f"{fake.cs_prefix()} {fake.cs_term()} {fake.cs_suffix()}"


def article_name():
    return f"{fake.article_prefix()} {fake.cs_term()} {fake.article_suffix()}"


def boolean_state(pos_threshold: float = 0.1):
    if random.random() <= pos_threshold:
        return True
    else:
        return False


def create_random_arxiv_post():
    author = fake.name()
    return Post(
        id=generate_id(),
        url=f"https://arxiv.org/abs/{generate_id()}",
        kind="paper",
        title=paper_name().strip(),
        description=fake.sentence(nb_words=10),
        text=fake.paragraph(nb_sentences=10),
        image_url="https://source.unsplash.com/random/?cosmos",
        locale="en",
        excerpt=fake.paragraph(nb_sentences=2),
        featured=boolean_state(pos_threshold=0.1),
        status="unpublished",
        readability=random.randint(1, 50),
        read_time=random.randint(2, 15),
        rating=round(random.random() * 10, 1),
        metadata={
            "citation_date": datetime.now() - timedelta(days=random.randint(0, 365)),
            "author": author,
            "authors": [
                author,
                *list({fake.name() for _ in range(random.randint(0, 5))}),
            ],
            "subjects": list({fake.cs_term for _ in range(random.randint(0, 5))}),
            "journal_ref": None,
            "comments": None,
        },
        created_at=datetime.now(),
        created_by="system",
        updated_at=None,
        updated_by=None,
        tags=[Tag(name="paper")],
    )


def create_random_github_post():
    owner = github_repo_owner()
    repo_name = github_repo_name()
    repo = f"{owner}/{repo_name}"
    repo_url = f"https://github.com/{repo}"
    td = random.randint(0, 365)
    created_at = datetime.now() - timedelta(days=td)
    return Post(
        id=generate_id(),
        url=repo_url,
        kind="code",
        title=repo.strip(),
        description=fake.sentence(nb_words=10),
        text=fake.paragraph(nb_sentences=10),
        image_url="https://source.unsplash.com/random/?cosmos",
        locale="en",
        excerpt=fake.paragraph(nb_sentences=2),
        featured=boolean_state(pos_threshold=0.1),
        status="unpublished",
        readability=random.randint(1, 50),
        read_time=random.randint(2, 15),
        rating=round(random.random() * 10, 1),
        metadata={
            "language": fake.programming_language(),
            "is_fork": boolean_state(pos_threshold=0.02),
            "is_archived": boolean_state(pos_threshold=0.001),
            "created_at": created_at,
            "updated_at": created_at,
            "topics": list({fake.tech_buzzword() for _ in range(5)}),
            "stars": random.randint(0, 50),
            "forks": random.randint(0, 50),
            "issues": random.randint(0, 50),
        },
        created_at=datetime.now(),
        created_by="system",
        updated_at=None,
        updated_by=None,
        tags=[Tag(name="code")],
    )


def create_random_article_post():
    return Post(
        id=generate_id(),
        url=fake.domain_name() + "/" + fake.tech_buzzword().lower(),
        kind="article",
        title=article_name().strip(),
        description=fake.sentence(nb_words=10),
        text=fake.paragraph(nb_sentences=10),
        image_url="https://source.unsplash.com/random/?cosmos",
        locale="en",
        excerpt=fake.paragraph(nb_sentences=2),
        featured=boolean_state(pos_threshold=0.1),
        status="unpublished",
        readability=random.randint(1, 50),
        read_time=random.randint(2, 15),
        rating=round(random.random() * 10, 1),
        metadata={},
        created_at=datetime.now(),
        created_by="system",
        updated_at=None,
        updated_by=None,
        tags=[Tag(name="article")],
    )


def main(
    path: str = "data/posts.jsonl",
    n_github_posts=100,
    n_arxiv_papers=100,
    n_articles=100,
):
    with open(path, "w+") as posts:
        for _ in range(n_github_posts):
            data = json.dumps(asdict(create_random_github_post()), default=str) + "\n"
            posts.write(data)
        for _ in range(n_arxiv_papers):
            data = json.dumps(asdict(create_random_arxiv_post()), default=str) + "\n"
            posts.write(data)
        for _ in range(n_articles):
            data = json.dumps(asdict(create_random_article_post()), default=str) + "\n"
            posts.write(data)


if __name__ == "__main__":
    main()
