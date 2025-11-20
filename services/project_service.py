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

        # Generar ID único si no viene del frontend
        project_id = payload.get("projectId", str(uuid.uuid4()))

        timestamp = str(int(time.time()))

        # Construir el item final
        item = {
            "projectId": project_id,
            "name": payload["name"],
            "description": payload["description"],

            # Opcionales
            "imageUrl": payload.get("imageUrl"),
            "repoUrl": payload.get("repoUrl"),
            "demoUrl": payload.get("demoUrl"),

            # Skills embebidos
            "skills": payload.get("skills", []),

            # Indices para filtrar
            # Vamos a generar un materialized index para cada skill usado
            "GSI1PK": None,   # Esto se ignora en un INSERT múltiple
            "GSI1SK": project_id,

            # Timestamps
            "createdAt": timestamp,
            "updatedAt": timestamp
        }

        # IMPORTANTE:
        # Por cada skill debe insertarse un item con sus campos GSI1
        skill_items = []

        if "skills" in payload:
            for skill in payload["skills"]:
                if "skillId" not in skill:
                    continue

                skill_items.append({
                    **item,
                    "GSI1PK": skill["skillId"]
                })

        # Insert principal (proyecto)
        ProjectRepository.create_project(item)

        # Insert de cada skill para el GSI
        for s in skill_items:
            ProjectRepository.create_project(s)

        return item
