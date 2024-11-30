import json
from pathlib import Path

from llm_service import services, llm
from llm_service import prompts


def run(project_path: Path, excludes: set[str]) -> str:
    adapter = llm.LLMAdapter()

    structure = services.convert_path_to_structure(project_path, excludes)
    structure = json.dumps(structure)

    chunks = services.split_text_in_chunks(structure)

    contents: list[str] = []
    for chunk in chunks:
        prompts_to_send = prompts.get_prompts()
        prompts_to_send.append(chunk)
        response = adapter.send_prompts(prompts_to_send)
        contents.append(response.get_content())

    if len(contents) > 1:
        prompts_to_send = prompts.get_summarise_prompts()
        prompts_to_send.extend(contents)
        response = adapter.send_prompts(prompts_to_send)
        content = response.get_content()
    else:
        content = contents[0]

    response = adapter.send_prompts(["Translate this text in russian: " + content])
    response.print()

    return response.get_content()

