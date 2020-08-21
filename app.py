import random
from flask import Flask, request
from pymessenger.bot import Bot

import requests
from bs4 import BeautifulSoup

URL = 'https://tygia.vn/gia-vang'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())
sauce = list(soup.find('tbody').find_all('tr'))

metadata = dict({
    gold.find('th').contents[0].strip('\n\r '): {
    "buy":gold.find('span', class_='text-green font-weight-bold').contents[0],
    "sell":gold.find('span', class_='text-red font-weight-bold').contents[0]
    } for gold in sauce[8:23]
})

metadata["Hồ Chí Minh"] = {
    "buy":sauce[0].find('span', class_='text-green font-weight-bold').contents[0], 
    "sell":sauce[0].find('span', class_='text-red font-weight-bold').contents[0]
}

def update_sjc():
    URL = 'https://tygia.vn/gia-vang'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    sauce = list(soup.find('tbody').find_all('tr'))
    metadata = dict({
        gold.find('th').contents[0].strip('\n\r '): {
            "buy":gold.find('span', class_='text-green font-weight-bold').contents[0],
            "sell":gold.find('span', class_='text-red font-weight-bold').contents[0]
        } for gold in sauce[8:23]
    })
    metadata["Hồ Chí Minh"] = {
        "buy":sauce[0].find('span', class_='text-green font-weight-bold').contents[0], 
        "sell":sauce[0].find('span', class_='text-red font-weight-bold').contents[0]
    }
    return "data updated"

def ask_sjc(city):
    city = city.strip(" ")
    if city in metadata:
        return "giá sjc mua của " + city + " là " + metadata[city]["buy"] + "VND, bán là " + metadata[city]["sell"] + 'VND'
    else:
        return city + " không có hoặc hãy kiểm tra dấu và viết hoa"

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEdtRujExABAEHzSs5k3nc5Ld1JS0PLOKZC9VLuP8dzOmLC4zHdJE3NMqfoWIxQSrLlErUVZANzHpm2Px0mdS6ADMuoVmwYZBdQM8pZBKbMEhQ261tXeWjpk4HjBXfkyuUkQQgGKYdmNzWPvQnfKsoqToH79Mdh9eTF25fZAG7LJnqsvoTKG'
VERIFY_TOKEN = 'ditmecosoc'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    mess = message['message']['text']
                    if mess == "update sjc":
                      update_sjc()
                    else:
                      send_message(recipient_id, ask_sjc(mess))
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    # response_sent_nontext = get_message()
                    send_message(recipient_id, str(message['message']))
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["Sua cc", "Bu cu", "dit me co soc", "du cang it thoi"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()


