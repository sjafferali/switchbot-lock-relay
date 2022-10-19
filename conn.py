import uuid
from cfg import TOKEN, SECRET

from switchbot import SwitchBot

switchbot = SwitchBot(token=TOKEN, secret=SECRET, nonce=str(uuid.uuid4()))
