import cozmo
import asyncio
import threading
import random
from smsmessenger import SMSMessenger
from enum import Enum

NUM_MAFIA = 2
NUM_INNOCENT = 4
NUM_PLAYER = 6

ANNOUNCEMENTS = {
    "Role Start": "Start to assign roles",
    "Night Start": "Close your eyes",
    "Barman": "Cancel doctor, detective, or not",
    "Doctor": "",
    "Detective": ""
}

PRIVATE_MESSAGES = {
    "Role Detail" : "%s, your role is: %s"
}

class Role(Enum):
    CITIZEN = 0,
    DOCTOR = 1,
    DETECTIVE = 2,
    MAFIOSO = 3,
    BARMAN = 4 

ROLE_NAME = {
    Role.CITIZEN: "citizen",
    Role.MAFIOSO: "mafioso",
    Role.DOCTOR: "doctor",
    Role.DETECTIVE: "detective",
    Role.BARMAN: "barman"
}

MAFIA_POOL = [Role.MAFIOSO, Role.MAFIOSO, Role.BARMAN]
INNOCENT_POOL = [Role.CITIZEN, Role.CITIZEN, Role.CITIZEN, Role.CITIZEN, Role.DOCTOR, Role.DETECTIVE]

class Player:
    name = None
    number = None
    role = None
    
    def __init__(self, name, number):
        self.name = name
        self.number = number


class PartyGameHost:
    def __init__(self):
        # thread lock
        self._lock = threading.Lock()
        
        self._msgr = SMSMessenger()
        self._msgReceived = False
        self._msgBuffer = []
        self._senderBuffer = []

        # hierarchical state machine
        self._currState = "Prepare"

        # state handlers
        self._stateMsgProcessor = {
            "Prepare": self.processMsgPrepare,
            "Night": None,
            "Day": None
        }

        # state main loop
        self._stateMainLoop = {
            "Prepare": self.mainLoopPrepare,
            "Night": None,
            "Day": None
        }


    def initializeGame(self):
        # player data
        self._playerNumbers = []
        self._players = {}
        self._roleRecords = {}

    def receiveMessage(self, msg, sender=None):
        if msg:
            with self._lock:
                self._msgReceived = True
                self._msgBuffer.append(msg)
                self._senderBuffer.append(sender)

    async def announce(self, msg):
        await self._robot.say_text(msg).wait_for_completed()

    async def processMsgPrepare(self):
        msg = None
        sender = None
        with self._lock:
            if self._msgReceived:
                msg = self._msgBuffer.pop(0)
                sender = self._senderBuffer.pop(0)
                if not self._msgBuffer:
                    self._msgReceived = False
                    
        (command,_,name) = msg.partition(",")
        if command == "Join" and name not in self._players:
            self._players[name] = Player(name, sender)
            print(len(self._players), " players joined")

    async def mainLoopPrepare(self):
        # enough players to start game
        if len(self._players) == NUM_PLAYER:
            await self.assignRoles()
            
            # change state to start game
            self._currState = "Night"
    
    async def assignRoles(self):
        # announce
        await self.announce(ANNOUNCEMENTS["Role Start"])
        
        # randomly pick assignments
        mafiaNames = random.sample(self._players.keys(), NUM_MAFIA)
        innocentNames = list(filter(lambda n: n not in mafiaNames, self._players.keys()))
        mafiaRoles = random.sample(MAFIA_POOL, NUM_MAFIA)
        innocentRoles = random.sample(INNOCENT_POOL, NUM_INNOCENT)

        # record and inform assignments
        for i in range(0, NUM_MAFIA):
            name = mafiaNames[i]
            role = mafiaRoles[i]
            player = self._players[name]
            player.role = role
            self._roleRecords[role] = name
            msg = PRIVATE_MESSAGES["Role Detail"] % (name, ROLE_NAME[role])
            self._msgr.sendMessage(player.number, msg)

        for i in range(0, NUM_INNOCENT):
            name = innocentNames[i]
            role = innocentRoles[i]
            player = self._players[name]
            player.role = role
            self._roleRecords[role] = name
            msg = PRIVATE_MESSAGES["Role Detail"] % (name, ROLE_NAME[role])
            self._msgr.sendMessage(player.number, msg)
        

    async def run(self, coz_conn:cozmo.conn.CozmoConnection):
        self._robot = await coz_conn.wait_for_robot()
        print("Cozmo running")

        # Add observer
        self._msgr.addObserver(self.receiveMessage)
        
        # Start SMS server
        t1 = threading.Thread(target=self._msgr.run, args=[], daemon=True)
        print("Server thread is daemon ", t1.isDaemon())
        t1.start()

        self.initializeGame()
        while True:
            await self._stateMsgProcessor[self._currState]()
            await self._stateMainLoop[self._currState]()
            await asyncio.sleep(0.1)

    
if __name__ == "__main__":
    host = PartyGameHost()
    cozmo.setup_basic_logging()
    cozmo.connect(host.run)

