from async_pymongo import AsyncDatabase

from src.domain.context import Context, ContextId


def context_to_document(context: Context) -> dict:
    result = context.model_dump(mode="json")
    result["_id"] = str(result.pop("id"))
    return result


def document_to_context(document) -> Context:
    return Context(
        id=document["_id"],
        content=document["content"],
    )


class ContextRepo:
    def __init__(self, database: AsyncDatabase):
        self._collection = database["context_collection"]

    async def add_one(self, item: Context):
        doc = context_to_document(item)
        await self._collection.insert_one(doc)

    async def get_one_by_id(self, item_id: ContextId) -> Context:
        doc = await self._collection.find_one({"_id": str(item_id)})
        if not doc:
            raise LookupError(item_id)
        return document_to_context(doc)

    async def update_one(self, item: Context):
        doc = context_to_document(item)
        await self._collection.update_one({"_id": doc["_id"]}, {"$set": doc})
