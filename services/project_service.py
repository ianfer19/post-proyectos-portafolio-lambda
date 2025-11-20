import uuid
import time
from repositories.project_repository import ProjectRepository

class ProjectService:

    @staticmethod
    def create_project(payload: dict):

        # Validaciones mínimas
        if "name" not in payload:
            raise Exception("El campo 'name' es obligatorio.")
        if "description" not in payload:
            raise Exception("El campo 'description' es obligatorio.")

        project_id = payload.get("projectId", str(uuid.uuid4()))
        timestamp = str(int(time.time()))

        skills = payload.get("skills", [])
        skills_ids = [s["skillId"] for s in skills if "skillId" in s]

        item = {
            "projectId": project_id,
            "name": payload["name"],
            "description": payload["description"],

            "imageUrl": payload.get("imageUrl"),
            "repoUrl": payload.get("repoUrl"),
            "demoUrl": payload.get("demoUrl"),

            "skills": skills,
            "skillsIds": skills_ids,

            "createdAt": timestamp,
            "updatedAt": timestamp
        }

        ProjectRepository.create_project(item)

        return item
