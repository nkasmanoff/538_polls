#/Users/noahkasmanoff/anaconda/bin/python3

"""
This file contains a web scraper that takes the daily polls accumulated
by fivethirtyeight.com, and sends that information to my phone.

These polls are located at url = https://projects.fivethirtyeight.com/polls/
"""

from twilio.rest import Client

from urllib.request import urlopen
from bs4 import BeautifulSoup
from json import load

url = "https://projects.fivethirtyeight.com/polls/"

def get_polls(url):
    """Returns a relatively dirty,
    but correct list of the dates and source of the most recent presidential approval ratings. 
    """
    
    client = urlopen(url)
    page_html = client.read()
    page_soup = BeautifulSoup(page_html,'html.parser')
    
    containers = page_soup.findAll('div',{'class': 'day-container'})

    
    
    todays_table = containers[0]

    date = str(todays_table.findAll('h2', {'class' : 'day hidden-date'})).split('"')[3]
   # print("today's date: " , date)
    todays_table = todays_table.findAll('table', {'class': 'polls-table'})[0].tbody
    table2 = todays_table.findAll("tr")[0]
   # print(len(todays_table.findAll("tr")))
    results = []
    for i in range(len(todays_table.findAll("tr"))):
        table2 = todays_table.findAll("tr")[i]
        result = table2.text
        if len(result) > 22:  #sufficent for now. 
        #print("")
       # print(result)
        
          results.append(result)
    return results


 

polls = get_polls(url)
path = '/Users/noahkasmanoff/dailyupdate/'
with open(path+'twilio.json') as f:
    twilio_credentials = load(f)
f.close()

account_sid = twilio_credentials['account_sid']
auth_token = twilio_credentials['auth_token']

client = Client(account_sid, auth_token)



for poll in polls: 
    message = client.messages.create(
                             	body=poll,
                              	from_=twilio_credentials['app_number'],
                              	to=twilio_credentials['my_number']
                          )

   # print(message.sid)



