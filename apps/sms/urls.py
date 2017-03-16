from app import app
from apps.sms import controllers


app.add_url_rule(
    '/', view_func=controllers.IndexView.as_view('index')
)
