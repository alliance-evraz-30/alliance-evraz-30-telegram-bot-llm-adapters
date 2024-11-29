from async_pymongo import AsyncDatabase

from src.domain.project import Project, ProjectId


def project_to_document(project: Project) -> dict:
    result = project.model_dump(mode="json")
    result["_id"] = str(result.pop("id"))
    return result


def document_to_project(document: dict) -> Project:
    return Project(
        id=ProjectId(document["_id"]),
        title=document["title"],
        path=document["path"],
        structure=document["structure"],
        language=document["language"],
        context_id=document["context_id"],
    )


class ProjectRepo:
    def __init__(self, database: AsyncDatabase, collection_name: str = "project_collection"):
        self.collection = database[collection_name]

    async def add_one(self, item: Project):
        document = project_to_document(item)
        await self.collection.insert_one(document)

    async def get_one_by_id(self, item_id: ProjectId) -> Project:
        document = await self.collection.find_one({"_id": str(item_id)})
        if not document:
            raise LookupError(f"Project with id {item_id} not found")
        return document_to_project(document)
