# -*- coding: utf-8 -*-
import webapp2
import sys
import os
from webapp2_extras import jinja2
from models import Comments
reload(sys)

sys.setdefaultencoding('utf8')
class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        _jinja2 = jinja2.get_jinja2(app=self.app)
        return _jinja2

    def render_template(self, filename, **kwargs):
        render = self.jinja2.render_template(filename, **kwargs)
        self.response.write(render)

class HomeHandler(BaseHandler):
    PER_PAGE = 10
    def get(self, page=0):
        page = int(page)
        offset = self.PER_PAGE * page

        list, next_cursor, more = Comments.query().order(-Comments.created).fetch_page(self.PER_PAGE, offset=offset)

        data = {
            'list': list,
            'page': page,
            'back': page > 0,
            'next': more and next_cursor,
        }

        self.render_template('index.html', **data)

class CommentHandler(BaseHandler):
    def get(self):
        self.render_template('comment.html')

    def post(self):
        comment = Comments()
        comment.text = self.request.get('text')
        comment.put()

        self.redirect('/comment')

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/(\d+)', HomeHandler),
    ('/comment', CommentHandler),
    ], debug=True)
