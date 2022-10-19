from switchbot import SwitchBot
from conn import switchbot


class Lock:
    lock_id = None
    device = None
    lock_state = None
    door_state = None

    def __init__(self, lock_id):
        self.lock_id = lock_id
        self.device = switchbot.device(id=lock_id)
        self.refresh()

    def refresh(self):
        new_status = self.device.status()
        self.lock_state = new_status["lock_state"]
        self.door_state = new_status["door_state"]

    def status(self):
        return {
                "lock_state": self.lock_state,
                "door_state": self.door_state
        }

    def lock(self):
        self.device.lock()
        self.refresh()

    def unlock(self):
        self.device.unlock()
        self.refresh()

    def update_status(self, lock_state):
        self.lock_state = lock_state.lower()
