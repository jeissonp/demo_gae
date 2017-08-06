# -*- coding: utf-8 -*-
import webapp2
import sys
import os
from handlers import *

reload(sys)

sys.setdefaultencoding('utf8')

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/(\d+)', HomeHandler),
    ('/comment', CommentHandler),
    ], debug=True)
