import json
from services.project_service import ProjectService
from utils.http_responses import success, error

def lambda_handler(event, context):
    try:
        if "body" not in event:
            return error("Body vacío")

        body = json.loads(event["body"])

        created = ProjectService.create_project(body)
        return success({
            "message": "Proyecto creado correctamente",
            "project": created
        }, 201)

    except Exception as e:
        return error(str(e), 400)
