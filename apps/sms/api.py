import json

from flask import request
from flask_login import current_user, login_required
from flask_restful import Resource

from app import api
from apps.modem import ModemGSM
from apps.sms.models import Message


class SendSms(Resource):
    """
    Class for send sms.
    """

    @login_required
    def post(self):
        """
        Send sms API with ModemGSM class.
        """
        # Parameters sms
        number = request.form['number']
        message = request.form['message']
        internal_id = request.form['internal_id']

        # Check parameters
        if number and message and internal_id:
            try:
                # Instance GSM Class
                gsm = ModemGSM()
                # Send SMS
                gsm.send_sms(
                    number, message, current_user, internal_id
                )
            except Exception:
                return {
                    'result': 'error',
                    'description': 'Error endpoint send_sms'
                }

            return {'result': 'ok', 'description': 'Success'}
        else:
            description = 'The internal_id, number and message ' \
                            'parameters are needed'

            return {
                'result': 'error',
                'description': description
            }


class GetReceivedSms(Resource):
    """
    Class for get sms.
    """

    @login_required
    def post(self):
        """
        Get received sms API with ModemGSM class.
        """
        # Parameters sms
        internal_id = request.form['internal_id']

        # Check parameters
        if internal_id:
            try:
                # Get received
                data = Message.query.filter_by(
                    internal_id=internal_id, received=True
                ).all()

                # Convert to json data
                records = []
                for record in data:
                    records.append({
                        "number": record.number, "user_id": record.user_id,
                        "created": record.created.strftime('%m/%d/%Y'),
                        "message": record.message
                    })
                data = json.dumps(records)
            except Exception:
                return {
                    'result': 'error',
                    'description': 'Error endpoint get_received_sms'
                }

            return {'result': 'ok', 'description': 'Success', 'data': data}
        else:
            return {
                'result': 'error',
                'description': 'The internal_id parameter is required'
            }


api.add_resource(SendSms, '/api/send_sms')
api.add_resource(GetReceivedSms, '/api/get_received_sms')
