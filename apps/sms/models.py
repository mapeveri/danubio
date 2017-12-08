import datetime
from app import db


class Message(db.Model):
    """
    Model Message.

    - **parameters**:
        :param id: Identification Message.
        :param message: Content sms message.
        :param number: Number sms.
        :param created: Created sms.
        :param internal_id: Id campaign.
        :param user_id: User that created the sms.
        :param user: User relation.
        :param received: If is a message received
    """
    __tablename__ = 'Messages'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    number = db.Column(db.String(50), nullable=False)
    created = db.Column(
        db.DateTime, nullable=False,
        default=datetime.datetime.utcnow
    )
    internal_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('User', foreign_keys=user_id)
    received = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Message %r>' % (self.message)
