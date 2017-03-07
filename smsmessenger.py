from twilio.rest import TwilioRestClient

ACCOUNT_SID = ''
AUTH_TOKEN = ''
TWILIO_NUMBER = ''

class SMSMessenger:
    
    def __init__(self):
        # Twilio account
        self._twilioCli = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    
    
        # cell phone numbers of player
        self._numbers = []
        self._numPrefix = "+1"

    def addNumber(self, number):
        self._numbers.append(self._numPrefix + number)
        
    def sendMessage(self, id, msg):
        self._twilioCli.messages.create(
            to = self._numbers[id],
            from_ = TWILIO_NUMBER,
            body = msg
        )

    def broadcastMessage(self, msg):
        for num in self._numbers:
            self._twilioCli.messages.create(
                to = num,
                from_ = TWILIO_NUMBER,
                body = msg
            )

if __name__ == '__main__':
    msgr = SMSMessenger()
    msgr.addNumber("7347413624")
    msgr.broadcastMessage("Hello World!")
