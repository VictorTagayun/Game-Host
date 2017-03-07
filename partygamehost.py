import cozmo
import asyncio
import threading
from smsmessenger import SMSMessenger

class PartyGameHost:
    def __init__(self):
        self._msgr = SMSMessenger()
        self._msgReceived = False
        self._msg = None

    def receiveMessage(self, msg):
        if msg:
            self._msgReceived = True
            self._msg = msg

    async def processMessage(self):
        self._msgReceived = False
        await self._robot.say_text(self._msg).wait_for_completed()

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
            if (self._msgReceived):
                await self.processMessage()
            await asyncio.sleep(0.1)

    
if __name__ == "__main__":
    host = PartyGameHost()
    cozmo.setup_basic_logging()
    cozmo.connect(host.run)

