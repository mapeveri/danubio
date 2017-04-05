import datetime
from app import db


class Message(db.Model):
    """
    Model Message
    """
    __tablename__ = 'Messages'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    created = db.Column(
        db.DateTime, nullable=False,
        default=datetime.datetime.utcnow
    )
    internal_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('User', foreign_keys=user_id)

    def __repr__(self):
        return '<Message %r>' % (self.message)
