import requests
from notion_secret import TASK_DATABASE_ID, NOTION_DB_URL, NOTION_PG_URL, TOKEN

class NotionSync:
    def __init__(self):
        pass

    def query_databases(self, integration_token=TOKEN):
        database_url = NOTION_DB_URL + TASK_DATABASE_ID + "/query"

        # headers = {"Authorization": "Bearer " + token, "Notion-Version": "2021-05-13"}
        response = requests.post(database_url, headers={"Authorization": "Bearer " + f"{integration_token}", "Notion-Version":"2021-05-13"})
        # print(database_url)
        # print(response.status_code)
        if response.status_code != 200:
            raise ApiError(f'Response Status: {response.status_code}')
        else:
            return response.json()

    def get_page_task(self, page_id, integration_token=TOKEN):
        # The API url to get a page title is
        # GET https://api.notion.com/v1/pages/page_id/properties/title
        page_url = NOTION_PG_URL + page_id + "/properties/title"
        # print(page_url)
        response = requests.get(page_url, headers={"Authorization": "Bearer " + f"{integration_token}", "Notion-Version":"2021-05-13"})
        # print(response.status_code)
        if response.status_code != 200:
            raise ApiError(f'Response Status: {response.status_code}')
        else:
            return response.json()
