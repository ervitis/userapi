import webapp2
from calendar_ex.calendar_service import CalendarService


calendar_service = CalendarService()
decorator = calendar_service.create_decorator()


class MainPage(webapp2.RequestHandler):

    @decorator.oauth_aware
    def get(self):
        url = decorator.authorize_url()

        if decorator.has_credentials():
            self.response.write('<a href="/continue">Continua</a>')
        else:
            self.response.write('<a href="%s">Login</a>' % url)


class ContinueHandler(webapp2.RequestHandler):

    @decorator.oauth_required
    def get(self):
        calendar_service.create_service()

        calendars = calendar_service.get_calendars()

        for calendar in calendars:
            self.response.write('%s<br>' % calendar['summary'])


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/continue', ContinueHandler),
    (decorator.callback_path, decorator.callback_handler()),
], debug=True)
