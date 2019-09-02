from flask import Flask, request
import nltk
from nltk.corpus import stopwords
import re
import random
import string # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('punkt') 
nltk.download('wordnet')    # a semantically-oriented dictionary 

app = Flask(__name__)

# A Connection to Facebook Messenger
FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = 'chat2secret'# <paste your verify token here>
PAGE_ACCESS_TOKEN = 'EAAVHkmOSFkEBAJVCzrK7VpUrzAnXee9dVhJ3VNvBZCVIiOwQVTr59u73yJ2ZCSRBTkY9Ynwe8dWV2Or2l3VHlvpj7gknGRHLThZBHDtZCNQalLAOqMZCZBTQTZBMXjLJ0wmnGadK9oSkOiD2dtZAZCibdquLPYVag9e3wwgMTndDe0QZDZD'

# Read article
f=open("C://Users/Administrator/Desktop/trump.txt",'r',errors = 'ignore')
raw=f.read()                            # string
f.close()

# Preprocess text
raw = re.sub("[\[].*?[\]]", "", raw)    # Drop Citations
sent_tokens=nltk.sent_tokenize(raw)     # list of sentences 
stop_words = set(stopwords.words('english'))
lemmer = nltk.stem.WordNetLemmatizer()
def clean_text(raw):
    text = raw.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    text = nltk.word_tokenize(text)                  # list of Words
    text = [w for w in text if not w in stop_words]  # remove stop words
    text = [lemmer.lemmatize(token, 'v') for token in text]
    return text

# Handle Greetings
GREETING_INPUTS = ("hello", "hi", "greetings", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "Glad to talk to you"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Main Procedure
@app.route("/webhook",methods=['GET','POST'])
def listen():
    """This is the main function flask uses to listen at the `/webhook` endpoint"""
    if request.method == 'GET':             # A Webhook Check from Facebook for developers
#       print('request.method = ' + request.method + '-----------------')
        if  request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return "incorrect"

    if request.method == 'POST':            # A User query
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):          # Is there any content in the message?
                user_text = x['message']['text']
                user_id = x['sender']['id']
               # print('user_text: '+ x['sender']['id'] + '-----------------')
                respond(user_id, user_text)
        return "ok"

def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))

def respond(user_id, user_text):
    user_text=user_text.lower()
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get('https://graph.facebook.com/'+user_id, user_details_params).json() 

    if(user_text=='thanks' or user_text =='thank you' ):# Thanks
        send_message(user_id, "You are welcome.. "+user_details['first_name'])
        return
    if user_text == 'bye':
        send_message(user_id, "Bye Bye"+' '+user_details['first_name'])
        return
    if(greeting(user_text)!=None):                  # Greetings
        print(user_id, greeting(user_text))
        send_message(user_id, greeting(user_text)+' '+user_details['first_name'])
        return    
    else:                                           # Request
        sent_tokens.append(user_text)               # Add request to end of text sentences
        TfidfVec = TfidfVectorizer(analyzer=clean_text)   # Initialize Tokenizer
        tfidf = TfidfVec.fit_transform(sent_tokens) # Construct TFIDF table
        vals = cosine_similarity(tfidf[-1], tfidf)  # Between request and text sentences
        vals = vals[0]                              # Convert to vector        
        idx=vals.argsort()[-2]      # The most similar sentence
        if(not vals[:-1].any()):    # No similarity
            bot_response="I am sorry! I don't understand you"
        else:
            bot_response = sent_tokens[idx]
        send_message(user_id, bot_response)
        sent_tokens.remove(user_text)

import requests
def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {'message': {'text': text},
               'recipient': {'id': recipient_id},
               'notification_type': 'regular'    }
    auth =    {'access_token': PAGE_ACCESS_TOKEN}
    response = requests.post(FB_API_URL, params=auth, json=payload)
    return response.json()

if __name__ == '__main__':
    print('----------- starting main  --------------')
    app.run(debug=True)



