"""
Services related to weaviate vector database
"""

import os
import weaviate
from utilities.file_utilities import load_json_from_file


class WeaviateService:
    """
    Weaviate service
    """

    def __init__(self):
        self.client = None
        self._init_schema()

    def _init_client(self):
        """
        init_client
        :return:
        """
        host = os.environ.get("WEAVIATE_HOST")
        port = os.environ.get("WEAVIATE_PORT")
        self.client = weaviate.Client(
            f"http://{host}:{port}",
            additional_headers={
                "X-OpenAI-Api-Key": os.environ.get("OPENAI_API_KEY"),
            },
        )

    def _init_schema(self):
        """
        _init_schema
        :return:
        """
        self._init_client()
        self.schema_class = os.environ.get("WEAVIATE_SCHEMA_CLASS")
        existing_schema = self.client.schema.get()
        if not any(
            cls["class"] == self.schema_class for cls in existing_schema["classes"]
        ):
            self.client.schema.create(load_json_from_file("schema.json"))

    def insert_data(self, content_id, title, body):
        """

        :param content_id:
        :param title:
        :param body:
        :return:
        """
        exists = self.client.data_object.exists(
            content_id, class_name=self.schema_class
        )
        data_object = {
            "body": body,
            "title": title,
        }
        if not exists:
            self.client.data_object.create(
                data_object=data_object,
                class_name=self.schema_class,
                uuid=content_id,
            )
            print("Object created.")
        else:
            self.client.data_object.update(
                uuid=content_id, class_name=self.schema_class, data_object=data_object
            )
            print("Object updated.")

    def search(self, query_text, max_distance=0.5, match_limit=3):
        """

        :param query_text:
        :param max_distance:
        :param match_limit:
        :return:
        """
        return (
            self.client.query.get(self.schema_class, ["title", "body"])
            .with_near_text({"concepts": [query_text], "distance": max_distance})
            .with_limit(match_limit)
            .with_additional(["distance"])
            .do()
        )

    def delete(self, content_id):
        """ "
        :param content_id:
        :return:
        """
        self.client.data_object.delete(uuid=content_id, class_name=self.schema_class)

    def item_exists(self, content_id):
        """
        :param content_id:
        :return boolean:
        """
        return self.client.data_object.exists(content_id, class_name=self.schema_class)
