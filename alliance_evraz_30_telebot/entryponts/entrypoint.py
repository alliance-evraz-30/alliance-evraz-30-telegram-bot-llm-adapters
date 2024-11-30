import json
from pathlib import Path

from adapters.llm import LLMAdapter
from constants.prompts import get_prompts, get_summarise_prompts
from services.services import convert_path_to_structure, split_text_in_chunks


def runLLM(project_path: Path, excludes: set[str]) -> str:
    adapter = LLMAdapter()

    structure = convert_path_to_structure(project_path, excludes)
    structure = json.dumps(structure)

    chunks = split_text_in_chunks(structure)

    contents: list[str] = []
    for chunk in chunks:
        prompts_to_send = get_prompts()
        prompts_to_send.append(chunk)
        response = adapter.send_prompts(prompts_to_send)
        contents.append(response.get_content())

    if len(contents) > 1:
        prompts_to_send = get_summarise_prompts()
        prompts_to_send.extend(contents)
        response = adapter.send_prompts(prompts_to_send)
        content = response.get_content()
    else:
        content = contents[0]

    response = adapter.send_prompts(["Translate this text in russian: " + content])

    return response.get_content()
