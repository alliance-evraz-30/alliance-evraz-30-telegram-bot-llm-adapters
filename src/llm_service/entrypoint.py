import json
from pathlib import Path

from . import prompts, services, llm


def run(project_path: Path, excludes: set[str]) -> str:
    structure = services.convert_path_to_structure(project_path, excludes)

    prompts_to_send = [
        prompts.ARCHITECTURE_CONTEXT_PROMPT,
        json.dumps(structure),
        *prompts.PROMPTS,
    ]

    adapter = llm.LLMAdapter()
    response = adapter.send_prompts(prompts_to_send)
    content = response.get_content()

    response = adapter.send_prompts(["Translate this text in russian: " + content])
    response.print()

    return response.get_content()
