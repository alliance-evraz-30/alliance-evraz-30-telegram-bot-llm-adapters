from pathlib import Path

from llm_service.entrypoint import run


def main():
    project_path = Path("D:/hakatons/files/RESTfulAPI-master 2/")
    excludes = {
        ".idea",
        ".venv",
        ".git",
        ".gitignore",
        ".env",
        "__pycache__",
    }
    result = run(project_path, excludes)
    print(result)


if __name__ == "__main__":
    main()
