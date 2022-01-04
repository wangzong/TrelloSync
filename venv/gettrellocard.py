# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from pprint import pprint
import json
import csv
from trellokey import board_id,trello_key,trello_token

########################
# Get Trello cards
#
########################

trello_cards_url = "https://api.trello.com/1/boards/" + board_id + "/cards" + "?key=" + trello_key + "&token=" + trello_token
trello_lists_url = "https://api.trello.com/1/boards/" + board_id + "/lists" + "?key=" + trello_key + "&token=" + trello_token

response = requests.request(
   "GET",
   trello_cards_url
)
data = response.json()



with open('result.json','w', encoding='utf-8') as f:
   json.dump(data,f,indent=4, sort_keys=True)


response = requests.request(
   "GET",
   trello_lists_url
)

lists = response.json()
# pprint(lists)


with open('result.csv', mode='w',newline='', encoding='utf-8') as csv_f:
   writer = csv.writer(csv_f,delimiter = '王')
   for card in data:
      name = card['name']
      idlist = card['idList']
      listname = ''
      for list in lists:
         if list['id'] == idlist:
            listname = list['name']
      link = card['url']
      id = card['idShort']

      # lastupdate = card['dateLastActivity']

      # print(color)
      writer.writerow([name, listname, link, id])
      # writer.writerow([name,listname,link,id,lastupdate])

#######################
# Connect to G Sheet
#######################

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
#
# scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/sprea...,"https://www.googleapis.com/auth/drive...","https://www.googleapis.com/auth/drive"]
#


# pprint(response.json())