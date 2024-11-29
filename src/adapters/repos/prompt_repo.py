from typing import Optional, Iterable

from async_pymongo import AsyncDatabase
from pydantic import BaseModel

from src.domain.prompt import Prompt, PromptId
from src.enums import TargetLanguage


class PromptSby(BaseModel):
    ids: Optional[set[PromptId]] = None
    importance: Optional[tuple[int, int]] = None
    languages: Optional[set[TargetLanguage]] = None


def prompt_to_document(data: Prompt) -> dict:
    result = data.model_dump(mode="json")
    result["_id"] = result.pop("id")
    return result


def document_to_prompt(document: dict) -> Prompt:
    return Prompt(
        id=PromptId(document["_id"]),
        title=document["title"],
        value=document["value"],
        importance=document["importance"],
        language=document["language"],
    )


class PromptRepo:
    def __init__(self, database: AsyncDatabase):
        self._collection = database["prompt_collection"]

    @staticmethod
    def _filter_by_from_sby(sby: PromptSby) -> dict:
        and_conds = []
        if sby.ids is not None:
            and_conds.append({"_id": {"$in": [str(x) for x in sby.ids]}})
        if sby.importance:
            bottom, top = sby.importance
            and_conds.append({"importance": {"$gte": bottom}})
            and_conds.append({"importance": {"$lt": top}})
        if sby.languages is not None:
            and_conds.append({"language": {"$in": list(sby.languages)}})
        return {"$and": and_conds}

    async def add_many(self, items: Iterable[Prompt]):
        data = [prompt_to_document(x) for x in items]
        await self._collection.insert_many(data)

    async def add_one(self, item: Prompt):
        document = prompt_to_document(item)
        await self._collection.insert_one(document)

    async def get_all(self) -> list[Prompt]:
        documents = self._collection.find({})
        return [document_to_prompt(doc) async for doc in documents]

    async def get_selected(self, sby: PromptSby) -> list[Prompt]:
        filter_by = self._filter_by_from_sby(sby)
        cursor = self._collection.find(filter_by)
        return [document_to_prompt(doc) async for doc in cursor]

    async def remove_all(self):
        await self._collection.delete_many({})
