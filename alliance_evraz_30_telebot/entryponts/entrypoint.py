import json
from pathlib import Path

from adapters import llm
from constants import prompts
from services import services

def runLLM(project_path: Path, excludes: set[str]) -> str:
    adapter = llm.LLMAdapter()

    structure = services.convert_path_to_structure(project_path, excludes)
    structure = json.dumps(structure)

    chunks = services.split_text_in_chunks(structure)

    contents: list[str] = []
    for chunk in chunks:
        prompts_to_send = [
            prompts.about_architecture(),
            prompts.find_problems(),
            chunk,
            prompts.response_format(len(chunk) // 2),
        ]
        response = adapter.send_prompts(prompts_to_send)
        contents.append(response.get_content())

    if len(contents) > 1:
        prompts_to_send = [
            prompts.summarise(),
            *contents
        ]
        response = adapter.send_prompts(prompts_to_send)
        content = response.get_content()
    else:
        content = contents[0]

    response = adapter.send_prompts([
        prompts.translate(),
        content,
    ])
    content = response.get_content()
    return content

