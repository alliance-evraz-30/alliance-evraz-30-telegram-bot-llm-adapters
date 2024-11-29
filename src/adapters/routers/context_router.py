from fastapi import APIRouter, Depends, UploadFile, File

from src.bootstrap import Bootstrap, get_container
from src.domain.context import Context, ContextId
from src.domain.prompt import Prompt

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
    service = container.context_service()
    await service.clear_one(context_id)
    return "Ok"


@context_router.post("/{context_id}/project")
async def upload_zip(
        context_id: ContextId,
        file: UploadFile = File(...),
        container: Bootstrap = Depends(get_container),
):
    project = await container.project_service().create_project_from_upload_file(file, context_id)

    # Отправляем проект в LLM, получаем контекст, сохраняем в базу
    context = await container.prompt_service().send_project(project)
    await container.context_service().update_one(context)

    return "Ok"


@context_router.post("/{context_id}/prompt")
async def send_prompts(
        context_id: ContextId,
        prompts: list[Prompt],
        container: Bootstrap = Depends(get_container),
):
    crud_service = container.context_service()
    llm_service = container.context_llm_service()

    # Получаем контекст
    try:
        context = await crud_service.get_one_by_id(context_id)
    except LookupError:
        context = Context(id=context_id, content="")
        await crud_service.create_one(context)

    # Получаем ответ модели, комбинируем контекст с рекомендациями, сохраняем
    recommendations = await llm_service.send_prompts_with_context(prompts, context)
    context = await llm_service.combine_context_with_recommendations(context, recommendations)
    await crud_service.update_one(context)

    return recommendations
