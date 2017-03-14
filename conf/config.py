from .config_local import *

# Flask-SQLAlchemy will track modifications of objects and emit signals
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True
