import uuid
from cfg import TOKEN, SECRET

from datetime import timedelta, datetime
from switchbot import SwitchBot

CACHE_TIME=300


class Lock:
    lock_id = None
    device = None
    lock_state = None
    door_state = None
    last_updated = None

    def __init__(self, lock_id):
        self.lock_id = lock_id
        self.refresh()

    def refresh(self):
        self._authenticate()
        new_status = self.device.status()
        self.lock_state = new_status["lock_state"]
        self.door_state = new_status["door_state"]
        self.last_updated = datetime.now()

    def status(self):
        if self.last_updated < datetime.now() - timedelta(seconds=CACHE_TIME):
            self.refresh()
        return {
                "lock_state": self.lock_state,
                "door_state": self.door_state
        }

    def _authenticate(self):
        switchbot = SwitchBot(token=TOKEN, secret=SECRET, nonce=str(uuid.uuid4()))
        self.device = switchbot.device(id=self.lock_id)

    def lock(self):
        self._authenticate()
        self.device.lock()
        self.refresh()

    def unlock(self):
        self._authenticate()
        self.device.unlock()
        self.refresh()

    def update_status(self, lock_state):
        self.lock_state = lock_state.lower()
