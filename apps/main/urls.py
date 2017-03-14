from app import app
from apps.main import controllers


app.add_url_rule(
    '/', view_func=controllers.IndexView.as_view('index')
)
