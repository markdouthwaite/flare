from src.infrastructure import backends

from src.commands import edition, candidate

BACKEND = backends.initialize()
AGENT = BACKEND.agents.get("d63de94cf7d3436a86bd2e085926fbda")

candidate.reset_candidate_status(BACKEND, AGENT)

edition.update_current(BACKEND, AGENT, k=5)

current_edition = edition.get_current(BACKEND)

print(current_edition)
