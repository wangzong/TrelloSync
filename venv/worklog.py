import requests
import json
import csv
from pprint import pprint
from notion_secret import TASK_DATABASE_ID, NOTION_DB_URL, NOTION_PG_URL, TOKEN
from notionsync import NotionSync
from dateutil import parser
from datetime import datetime, timedelta, timezone
import argparse

# get current time in BJ timezone
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
bj_now = utc_now.astimezone(timezone(timedelta(hours=8)))


# Set date argument
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-d","--date", type=str,
                    help="generate log for a specific date, date format is YYYY-MM-DD")
arg = arg_parser.parse_args()

if arg.date:
    date_str = arg.date
    time_str = '12:00:00+08:00'
    dt_str = date_str + " " + time_str
    dt=datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S%z')
else:
    # if no argument, take current BJ time as dt to process
    dt=bj_now


# Get Notion tasks DB
nsync = NotionSync()
db_json = nsync.query_databases()
data = db_json['results']

# Get the tasks list from tasks_v2.json
with open('tasks_v2.json', mode='r', encoding='utf-8') as tasks_f:
    tasks_json = json.load(tasks_f)


print("Writing worklog.csv...")

with open('worklog.csv', mode='a',newline='', encoding='utf-8') as csv_f:
    writer = csv.writer(csv_f)
    writer.writerow([datetime.strftime(dt, '%Y-%m-%d')])
    # print(datetime.strftime(dt, '%Y-%m-%d'))
    # writer.writerow([datetime.strftime(bj_now.date(),'%Y-%m-%d')])
    for task in data:
        title = ""
        # print(task)
        id = task['id']
        # print(id)
        # print(tasks_json.keys)

        if id in tasks_json.keys():
            title = tasks_json[id]['title']
        else:
            page_json = nsync.get_page_task(id)
            # pprint(page_json)
            results = page_json['results']
            if len(results) > 0:
                title = results[0]['title']['plain_text']
        created_time = parser.parse(task['created_time'])
        utc_last_edited_time = parser.parse(task['last_edited_time'])
        bj_last_edited_time = utc_last_edited_time.astimezone(timezone(timedelta(hours=8)))

        if bj_last_edited_time.date() == dt.date() and title != "":
            # print(title,bj_last_edited_time)
            writer.writerow([title,bj_last_edited_time])
    writer.writerow([])

print("Done.")

