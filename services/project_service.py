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

        # Item principal SIN campos del GSI
        item = {
            "projectId": project_id,
            "name": payload["name"],
            "description": payload["description"],

            "imageUrl": payload.get("imageUrl"),
            "repoUrl": payload.get("repoUrl"),
            "demoUrl": payload.get("demoUrl"),

            "skills": payload.get("skills", []),

            "createdAt": timestamp,
            "updatedAt": timestamp
        }

        # Guardar item principal
        ProjectRepository.create_project(item)

        # Crear items para el GSI
        if "skills" in payload:
            for skill in payload["skills"]:
                if "skillId" not in skill:
                    continue
                
                gsi_item = {
                    "projectId": project_id,
                    "name": payload["name"],

                    # Claves del índice
                    "GSI1PK": skill["skillId"],  # Partition key del GSI
                    "GSI1SK": project_id,        # Sort key del GSI

                    # Timestamps
                    "createdAt": timestamp,
                    "updatedAt": timestamp
                }

                # Insertar item del GSI
                ProjectRepository.create_project(gsi_item)

        return item
