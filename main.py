
import webapp2
import models
import time
import cgi

SECONDS = 0.2
MAIN_PAGE_FOOTER_TEMPLATE = """
    <form action="/sign" method="post">
      <div>Owner: <input type="text" name="owner"></div>
      <div>Business: <input type="text" name="business"></div>
      <div><input type="submit" value="Send it!"></div>
    </form>

    <form action="/search" method="post">
      <div>Search owner: <input type="text" name="searchOwner"></div>
      <div><input type="submit" value="Search!"></div>
    </form>
  </body>
</html>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        stores = models.Store.all()

        for store in stores:
            store_id = str(store.key().id_or_name())
            self.response.write('<a href="/detail/id=%s">Owner %s</a><br>' % (store_id, cgi.escape(store.owner)))
            self.response.write('Business %s<br><br>' % cgi.escape(store.business))

        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE)


class Sign(webapp2.RequestHandler):
    def post(self):
        owner = self.request.get('owner')
        business = self.request.get('business')

        store = models.Store()

        store.business = business
        store.owner = owner

        store.put()

        time.sleep(SECONDS)
        self.redirect('/', permanent=True)


class Detail(webapp2.RequestHandler):
    def get(self, id):
        store = models.Store().get_by_id(ids=int(id))

        if store:
            self.response.write('Detail for key id=%s: Owner->%s, business->%s'
                                % (str(store.key().id_or_name()), store.owner, store.business))
        else:
            self.response.write('Error!')

        print_goback_link(self)


class Search(webapp2.RequestHandler):
    def post(self):
        owner = self.request.get('searchOwner')

        if not owner:
            self.response.write('No search parameters!')
            print_goback_link(self)

        q = models.Store().all()
        results = q.filter('owner =', owner).run()

        self.response.write('<br>Results:')
        for result in results:
            self.response.write('<br> Id: %s, owner: %s, business: %s' %
                                (str(result.key().id_or_name()), result.owner, result.business))

        print_goback_link(self)


def print_goback_link(obj_self):
    obj_self.response.write('<br>')
    obj_self.response.write('<br><br><a href="/">Volver atras</a>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sign', Sign),
    ('/detail/id=(\d+)', Detail),
    ('/search', Search),
], debug=True)
