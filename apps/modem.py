import time
import serial

from app import app, db
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
        self.port.write(b'ATZ\r')
        time.sleep(0.5)
        # response = self.port.read(64)

        self.port.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        # response = self.port.read(64)

        number_gsm = str.encode(app.config["NUMBER_GSM"])
        self.port.write(b'AT+CSCA="' + number_gsm + b'"')
        time.sleep(0.5)
        # response = self.port.read(64)

        self.port.write(b'AT+CMGS="' + str.encode(number) + b'"\r')
        time.sleep(0.5)
        # response = port.read(64)

        self.port.write(str.encode(message) + b"\r")
        time.sleep(0.5)
        # response = self.port.read(64)

        self.port.write(bytes([26]))

        # Add message in db
        message = Message(
            message=message, number=number, user=user
        )
        db.session.add(message)
        db.session.commit()

    def __del__(self):
        self.port.close()
