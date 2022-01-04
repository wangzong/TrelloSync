import requests
import json
import csv
from pprint import pprint
from notion_secret import TASK_DATABASE_ID, NOTION_DB_URL, NOTION_PG_URL, TOKEN
from notionsync import NotionSync

'''
This script is to create task_id and task_name mapping file tasks.json.
The file will be used by worklog.py to convert the task_id to task_name
'''

nsync = NotionSync()
db_json = nsync.query_databases()
data = db_json['results']
tasks = {}

task_number = len(data)
print("%d tasks to be processed." % task_number)

processed_number = 0

for task in data:
    id = task['id']
    last_updated_time = task['last_edited_time']
    print(id, last_updated_time)
    task_json = nsync.get_page_task(id)

    results = task_json['results']
    if len(results) > 0:
        title = results[0]['title']['plain_text']
        # pprint(task_json)
        # title = task_json['results'][0]['title']['plain_text']
        tasks[id]={'title':title,'last_updated_time':last_updated_time}
    processed_number = processed_number + 1
    print("%d of %d tasks done." % (processed_number, task_number))
pprint(tasks)

with open("tasks_v2.json","w") as f:
     json.dump(tasks,f)
