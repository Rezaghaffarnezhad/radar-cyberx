import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from config import config_by_name

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")

def create_app(config_name=None):
    if not config_name:
        config_name = os.getenv("FLASK_ENV", "development")
        
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, message_queue=app.config["REDIS_URL"])

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.chat_routes import chat_bp
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")

    # Register WebSocket Events
    import app.websocket.events

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
