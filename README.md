# Mafia Game Host
Using voice and SMS, Cozmo can be the spectator of Mafia game to guide the killing and lynch day and night.

## Implementation Details [IMPORTANT]

**PART I:**
Use `flask` to handle incoming web requests. The server is exposed to the internet via an `ngrok` tunnel.

How to set it up:

1. Cozmo_response is the method that is designated by flask to handle the incoming requests. No changes required in the code for this.

2. Download ngrok from the official website: https://ngrok.com/

3. Flask sets up the server on port 5000. To have ngrok set up the tunnel, enter the following command: `ngrok http 5000`
4. The console will now provide details of the tunell URLs and will display incoming requests. Keep this window alive:
![Ngrok Console](/ReadmeImage/ngrok_console.png?raw=true "Ngrok Console")
5. The details of the tunnel URLs with a more verbose debug will be available at the following url: http://127.0.0.1:4040/
6. Copy one of the URLs (in this example: http://330b43d6.ngrok.io/) to be used for the next step
![Ngrok](/ReadmeImage/ngrok.png?raw=true "Ngrok")

**PART II:**	
A `twilio` account is used to set up a phone number for Cozmo to send messages via SMS/MMS.

How to set it up:

1. Sign up for a Twilio account: https://www.twilio.com/

2. You will receive your Account SID and Authorization Token that will be used for all interactions with the API.
![Twilio](/ReadmeImage/twilio.png?raw=true "Twilio")

3. Go to the Phone numbers section and choose a number to be associated with the account. You are allowed one free number with a trial account.
4. Once you have a number assigned to the account, select it by going to Phone Numbers -> Manage Numbers -> Active Numbers. Under messaging, change �A message comes in� to Webhook and the URL to the ngrok URL as copied in step 7 of PART I.
![Twilio Config](/ReadmeImage/twilio_config.png?raw=true "Twilio Config")

5. Detailed information about Twilio package for Python can be found at: https://www.twilio.com/docs/quickstart/python

## Instructions [IMPORTANT]

The modules required in addition to the `Cozmo` module are:

* Flask
* Twilio
* Common


Common is a package included in the Git repo: https://github.com/Wizards-of-Coz/Common

The other modules can be installed via pip if not already present:
`pip install Flask`
`pip install twilio`

1. Fill up TwilioConfig.ini with your account sid, auth token and twilio phone number obtained from part I to the corresponding fields.
2. Start the script partygamehost.py
3. Each player send `Join, <name>` to twilio number. The names should be unique.
4. Follow Cozmo's voice guide and private message.
5. The supported text message send to twilio for different roles and stages are
`Vote, <name>`, `Kill, <name>`, `Canel, <role>`, `Detect, <name>`, `Protect, <name>`, case sensitive.
