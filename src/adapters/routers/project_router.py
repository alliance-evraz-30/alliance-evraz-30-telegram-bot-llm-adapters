from fastapi import APIRouter, UploadFile, File, Depends

from src.bootstrap import Bootstrap, get_container
from src.domain.project import ProjectId, Project

project_router = APIRouter(
    prefix="/project",
)


@project_router.post("/")
async def create_project(
        file: UploadFile = File(...),
        container: Bootstrap = Depends(get_container),
) -> ProjectId:
    project = await container.project_service().create_project_from_upload_file(file)
    await container.prompt_service().send_project(project)
    return project.id


@project_router.get("/{project_id}")
async def get_one_by_id(
        project_id: ProjectId,
        container: Bootstrap = Depends(get_container),
) -> Project:
    return await container.project_repo().get_one_by_id(project_id)

# @project_router.get("/{project_id}")
# def get_selected_recommendations(
#         project_id: ProjectId,
# ) -> list[Recommendation]:
#     pass
#
#
# @project_router.get("/{project_id}")
# def get_all_recommendations(
#         project_id: ProjectId,
# ) -> list[Recommendation]:
#     pass
#
#
# @project_router.get("/{project_id}/core")
# def get_core_recommendation(
#         project_id: ProjectId,
# ) -> Recommendation:
#     pass
#
#
# @project_router.get("/{project_id}/free")
# def get_free_recommendation(
#         project_id: ProjectId,
# ) -> Recommendation:
#     pass
