'''
Tiffany Fabianac Modified code from:
Reading GMAIL using Python
    - https://github.com/abhishekchhibber/Gmail-Api-through-Python
	- Abhishek Chhibber
'''

'''
This script does the following:
- Go to Gmal inbox
- Find and read all the Google Alert messages
- Extract details (Date, Snippet) and export them to a .csv file / DB
'''

'''
Before running this script, the user should get the authentication by following 
the link: https://developers.google.com/gmail/api/quickstart/python
Also, client_secret.json should be saved in the same directory as this file
'''

# Importing required libraries
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import csv
import json
import io

# Creating a storage.JSON file with authentication details
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'  # we are using modify and not readonly, as we will be marking the messages Read
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

user_id = 'me'
label_id_one = 'INBOX'

# Getting all the unread messages from Inbox
# labelIds can be changed accordingly
alert_msgs = GMAIL.users().messages().list(userId='me', labelIds=[label_id_one], q='from:googlealerts-noreply@google.com').execute()

# We get a dictonary. Now reading values for the key 'messages'
mssg_list = alert_msgs['messages']

final_list = []

for mssg in mssg_list:
    temp_dict = {}
    m_id = mssg['id']  # get id of individual message
    message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()  # fetch the message using API
    payld = message['payload']  # get payload of the message
    headr = payld['headers']  # get header of the payload

    for two in headr:  # getting the date
        if two['name'] == 'Date':
            msg_date = two['value']
            date_parse = (parser.parse(msg_date))
            m_date = (date_parse.date())
            temp_dict['Date'] = str(m_date)
        else:
            pass

    temp_dict['Snippet'] = message['snippet']



    final_list=json.dumps(temp_dict)  # This will create a dictonary item in the final list
    re.sub(r'\u22c5', '', final_list)
    print final_list

# exporting the values as .csv
#final_list = json.loads(final_list)
with open("API_out.csv", "a") as f:
    header=["Date", "Snippet"]
    writer = csv.DictWriter(f, fieldnames=header, delimiter=',')
    for x in final_list:
        writer.writerow(x)




