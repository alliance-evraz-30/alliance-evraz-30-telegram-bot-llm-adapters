from fastapi import APIRouter, Depends, UploadFile, File

from src.bootstrap import Bootstrap, get_container
from src.domain.context import Context, ContextId
from src.domain.prompt import Prompt
from src.services.context_service import combine_context_with_prompts

context_router = APIRouter(
    prefix="/context",
    tags=["Context"],
)


@context_router.post("/")
async def create_context(
        context: Context,
        container: Bootstrap = Depends(get_container),
):
    await container.context_service().create_one(context)
    return context


@context_router.post("/{context_id}/clear")
async def clear_context(
        context_id: ContextId,
        container: Bootstrap = Depends(get_container),
):
    pass


@context_router.post("/{context_id}/project")
async def upload_zip(
        context_id: ContextId,
        file: UploadFile = File(...),
        container: Bootstrap = Depends(get_container),
):
    pass


@context_router.post("/{context_id}/prompt")
async def send_prompts(
        context_id: ContextId,
        data: list[Prompt],
        container: Bootstrap = Depends(get_container),
):
    crud_service = container.context_service()
    llm_service = container.context_llm_service()

    # Получаем контекст, комбинируем с промтами, сохраняем
    context = await crud_service.get_one_by_id(context_id)
    context = await llm_service.combine_context_with_prompts(context, data)
    await crud_service.update_one(context)

    # Получаем ответ модели, комбинируем контекст с рекомендациями, сохраняем
    recommendations = await llm_service.send_context(context)
    context = await llm_service.combine_context_with_recommendations(context, recommendations)
    await crud_service.update_one(context)

    return recommendations

