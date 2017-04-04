import time
import serial

from app import app
from apps.sms.models import Message


class ModemGSM(object):
    """
    Class for manage GSM Modem
    """
    instance = None
    port = None

    def __init__(self):
        self.port = serial.Serial(app.config["SERIAL_GSM"])

    # Singleton
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kargs)
        return cls.instance

    def send_sms(self, number, message, user):
        time.sleep(1)
        self.port.write('ATZ\r')
        response = self.port.read(64)

        self.port.write('AT+CMGF=1\r')
        response = self.port.read(64)

        self.port.write('AT+CSCA="' + app.config["NUMBER_GSM"] + '"')
        response = self.port.read(64)
        self.port.write('AT+CMGS="' + number.encode() + '"\r')
        response = port.read(64)

        self.port.write(message.encode() + "\r")
        response = self.port.read(64)

        self.port.write(chr(26))

        # Add message in db
        message = Message(
            message=message, number=number, user=user
        )
        db.session.add(message)
        db.session.commit()

    def __del__(self):
        self.port.close()
