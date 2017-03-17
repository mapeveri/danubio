from flask import request
from flask_restful import Resource

from app import api
from apps.modem import ModemGSM
from apps.sms import models


class SendSms(Resource):
    """
    Send sms API with ModemGSM class
    """
    def post(self):
        # Parameters sms
        number = request.form['number']
        message = request.form['message']

        # Check parameters
        if number and message:
            try:
                # Instance GSM Class
                instanceGsm = ModemGSM()
                # Send SMS
                instanceGsm.send_sms(number, message)
            except Exception:
                return {
                    'result': 'error',
                    'description': 'Error endpoint send_sms'
                }

            return {'result': 'ok', description: 'Success'}
        else:
            return {
                'result': 'error',
                'description': 'The number and message parameters are needed'
            }


api.add_resource(SendSms, '/api/send_sms')
