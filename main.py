
import webapp2
import models
import cgi


MAIN_PAGE_FOOTER_TEMPLATE = """
    <form action="/sign" method="post">
      <div>Owner: <input type="text" name="owner"></div>
      <div>Business: <input type="text" name="business"></div>
      <div><input type="submit" value="Send it!"></div>
    </form>
  </body>
</html>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        key = models.ConstructKey(name='stores')
        stores = models.Store.query(ancestor=key.create_key()).order(models.Store.owner).fetch()

        for store in stores:
            store_id = str(store.key.id())
            self.response.write('<a href="/detail/id=%s">Owner %s</a><br>' % (store_id, cgi.escape(store.owner)))
            self.response.write('Business %s<br><br>' % cgi.escape(store.business))

        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE)


class Sign(webapp2.RequestHandler):
    def post(self):
        owner = self.request.get('owner')
        business = self.request.get('business')

        key = models.ConstructKey(name='stores')

        store = models.Store(parent=key.create_key())

        store.business = business
        store.owner = owner

        store.put()

        self.redirect('/')


class Detail(webapp2.RequestHandler):
    def get(self, id):
        key = models.ConstructKey(name='stores')

        store = models.Store.get_by_id(id=int(id), parent=key.create_key())

        if store:
            self.response.write('Detail for key id=%s: Owner->%s, business->%s'
                                % (store.key.id(), store.owner, store.business))
        else:
            self.response.write('Error!')

        self.response.write()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sign', Sign),
    ('/detail/id=(\d+)', Detail),
], debug=True)
