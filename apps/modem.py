import serial
import time

from app import app, db
from apps.sms.models import Message


class ModemGSM(object):
    """
    Class for manage GSM Modem.
    """
    instance = None
    port = None

    def __init__(self):
        self.port = serial.Serial(app.config["SERIAL_GSM"], 9600, timeout=5)

    # Singleton
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kargs)
        return cls.instance

    def send_sms(self, number, message, user, internal_id):
        """
        Send sms with command at.
            :param number: Number to send sms
            :param content: Description sms
            :param user: User sending sms
            :param internal_id: Identication of transaction (Campaign)
        """
        self.port.write(b'ATZ\r')
        time.sleep(1)

        self.port.write(b'AT+CMGF=1\r')
        time.sleep(1)

        number_gsm = str.encode(app.config["NUMBER_GSM"])
        self.port.write(b'AT+CSCA="' + number_gsm + b'"')
        time.sleep(1)

        self.port.write(b'AT+CMGS="' + str.encode(number) + b'"\r')
        time.sleep(1)

        self.port.write(str.encode(message) + b"\r")
        time.sleep(1)

        self.port.write(bytes([26]))

        # Add message in db
        message = Message(
            message=message, number=number,
            user=user, internal_id=internal_id
        )
        db.session.add(message)
        db.session.commit()

    def get_received_sms(self, internal_id):
        """
        Get received sms of a internal_id with command at.
            :param user: User logged
            :param internal_id: Identication of transaction (Campaign)
        """
        return Message.query.filter_by(internal_id=internal_id).all()

    def __del__(self):
        self.port.close()
