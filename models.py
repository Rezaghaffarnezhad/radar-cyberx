from datetime import datetime
from app.main import db
from geoalchemy2 import Geometry

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=False, index=True)
    username = db.Column(db.String(64), unique=True, nullable=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    online_status = db.Column(db.Boolean, default=False)

    # Relationships
    location = db.relationship('Location', backref='user', uselist=False, cascade='all, delete-orphan')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')

    def to_dict(self):
        loc = self.location
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar": self.avatar,
            "bio": self.bio,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "online_status": self.online_status,
            "location": {
                "latitude": loc.latitude if loc else None,
                "longitude": loc.longitude if loc else None,
                "visibility_radius": loc.visibility_radius if loc else 5000
            } if loc else None
        }

class Location(db.Model):
    __tablename__ = 'locations'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, default=0.0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    visibility_radius = db.Column(db.Integer, default=5000) # در متر
    
    # PostGIS geometry column for high-performance spatial queries (SRID 4326 for WGS 84)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(32), default='text') # text, image, file, voice
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(32), default='sent') # sent, delivered, read

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "message": self.message,
            "type": self.type,
            "created_at": self.created_at.isoformat(),
            "status": self.status
        }

class Friend(db.Model):
    __tablename__ = 'friends'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Block(db.Model):
    __tablename__ = 'blocks'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    blocked_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reported_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
