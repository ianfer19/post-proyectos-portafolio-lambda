from config.dynamo import table
import uuid
import time
from boto3.dynamodb.conditions import Key

class ProjectRepository:

    @staticmethod
    def create_project(data: dict):
        table.put_item(Item=data)
        return data
