import webapp2
import logging
from models import Comments

from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.api import taskqueue

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        _jinja2 = jinja2.get_jinja2(app=self.app)
        return _jinja2

    def render_template(self, filename, **kwargs):
        user = users.get_current_user()
        kwargs.update({
            'email': user.email(),
            'logout': users.create_login_url('/')
        })

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


class RemoveHandler(webapp2.RequestHandler):
    def get(self):
        list = Comments.query().fetch(keys_only=True)
        total = 0
        for item in list:
            task = taskqueue.add(url='/remove', params={'id': item.id()})
            total += 1
        logging.info('Total {}'.format(total))

    def post(self):
        id = self.request.get('id')
        comment = Comments.get_by_id(int(id))
        if comment:
            comment.key.delete()
        else:
            logging.error('Not found {}'.format(id))
