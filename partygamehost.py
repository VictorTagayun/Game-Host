import cozmo
import asyncio
import threading
from smsmessenger import SMSMessenger

NUM_MAFIA = 2
NUM_INNOCENT = 4
NUM_PLAYER = 6

NIGHT_ANNOUNCEMENTS = {
    "Night Start": "Close your eyes",
    "Barman": "Cancel doctor, detective, or not",
    "Doctor": "",
    "Detective": ""
}

class PartyGameHost:
    def __init__(self):
        # thread lock
        self._lock = threading.Lock()
        
        self._msgr = SMSMessenger()
        self._msgReceived = False
        self._msg = None
        self._lastSender = None

        # hierarchical state machine
        self._currState = "Prepare"

        # state handlers
        self._stateMsgProcessor = {
            "Prepare": processMsgPrepare,
            "Night": None,
            "Day": None
        }

        # state main loop
        self._stateMainLoop = {
            "Prepare": None,
            "Night": None,
            "Day": None
        }

        # player data
        self._playerNumbers = []

    def receiveMessage(self, msg, sender=None):
        if msg:
            with self._lock:
                self._msgReceived = True
                self._msg = msg
                self._lastSender = sender

    async def processMessage(self):
        with self._lock:
            if self._msgReceived:
                self._msgReceived = False
                await self._robot.say_text(self._msg).wait_for_completed()

    async def announce(self, msg):
        await self._robot.say_text(msg).wait_for_completed()

    async def processMsgPrepare(self):
        with self._lock:
            if self._msgReceived:
                self._msgReceived = False
                if self._msg == "Join" and not self._lastSender in self._playerNumbers:
                    self._playerNumbers.append(self._lastSender)
        print(len(self._playerNumbers))
    
    async def assignRoles(self):
        pass

    async def run(self, coz_conn:cozmo.conn.CozmoConnection):
        self._robot = await coz_conn.wait_for_robot()

        # Add observer
        self._msgr.addObserver(self.receiveMessage)
        
        # Start SMS server
        t1 = threading.Thread(target=self._msgr.run, args=[])
        t1.start()

        # self._robot = 
        print("Cozmo running")

        while True:
            await self._stateMsgProcessor[self._currState]()
            await asyncio.sleep(0.1)

    
if __name__ == "__main__":
    host = PartyGameHost()
    cozmo.setup_basic_logging()
    cozmo.connect(host.run)

