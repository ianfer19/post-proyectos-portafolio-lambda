from config.dynamo import table

class ProjectRepository:

    @staticmethod
    def create_project(item: dict):
        table.put_item(Item=item)
        return item
