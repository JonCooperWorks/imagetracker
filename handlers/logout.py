from google.appengine.api import users

from handlers.base import BaseHandler


class LogoutHandler(BaseHandler):

  def get(self):
    if users.get_current_user():
      return self.redirect(users.create_logout_url(self.uri_for('home')))

    return self.redirect_to('home')
