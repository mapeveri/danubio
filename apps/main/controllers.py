from flask import redirect
from flask.views import View


class IndexView(View):
    """
    Index main view
    """
    def dispatch_request(self):
        return redirect("/admin/login")
