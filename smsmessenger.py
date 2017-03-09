from twilio.rest import TwilioRestClient
import twilio.twiml
from flask import Flask, request
import Common.flask_helpers as flask_helpers
import configparser
import asyncio

class SMSMessenger:
    
    def __init__(self):
        # Config
        config = configparser.ConfigParser(allow_no_value=True)
        config.read('TwilioConfig.ini')
        
        # Twilio account
        account_sid = config.get('Auth','account_sid')
        auth_token = config.get('Auth','auth_token')
        self._twilioCli = TwilioRestClient(account_sid, auth_token)
        self._twilioNumber = config.get('Auth', 'twilio_number')
    
        # cell phone numbers of player
        self._numbers = []
        self._numPrefix = "+1"

        # Server variables
        self._app = Flask(__name__)

        # Event observers
        self._observers = []

    def run(self):
        self._app.add_url_rule("/", "textResponse", self.textResponse, methods=["GET", "POST"])
        flask_helpers.run_flask(self._app)

    def addObserver(self, func):
        self._observers.append(func)

    def notifyObservers(self, msg, sender):
        for ob in self._observers:
            ob(msg, sender)

    def textResponse(self):
        fromNumber = request.values.get("From", None)
        messageText = request.values.get("Body", None)
        print(fromNumber, " sends: ", messageText)

        self.notifyObservers(messageText, fromNumber)
        
        resp = twilio.twiml.Response()
        # return resoinse
        return str(resp)
        

    def addNumber(self, number):
        self._numbers.append(number)
        
    def sendMessage(self, id: int, msg):
        self._twilioCli.messages.create(
            to = self._numbers[id],
            from_ = self._twilioNumber,
            body = msg
        )

    def sendMessage(self, number, msg):
        self._twilioCli.messages.create(
            to = number,
            from_ = self._twilioNumber,
            body = msg
        )

    def broadcastMessage(self, msg):
        for num in self._numbers:
            self._twilioCli.messages.create(
                to = num,
                from_ = self._twilioNumber,
                body = msg
            )

if __name__ == '__main__':
    msgr = SMSMessenger()
    msgr.addNumber("+17347413624")
    msgr.run()
    print("End of main func")
