from flask import request
from flask_login import current_user, login_required
from flask_restful import Resource

from app import api
from apps.modem import ModemGSM


class SendSms(Resource):
    """
    Send sms API with ModemGSM class
    """
    @login_required
    def post(self):
        # Parameters sms
        number = request.form['number']
        message = request.form['message']
        internal_id = request.form['internal_id']

        # Check parameters
        if number and message and internal_id:
            try:
                # Instance GSM Class
                instanceGsm = ModemGSM()
                # Send SMS
                instanceGsm.send_sms(
                    number, message, current_user, internal_id
                )
            except Exception:
                return {
                    'result': 'error',
                    'description': 'Error endpoint send_sms'
                }

            return {'result': 'ok', 'description': 'Success'}
        else:
            return {
                'result': 'error',
                'description': 'The number and message parameters are needed'
            }


api.add_resource(SendSms, '/api/send_sms')
