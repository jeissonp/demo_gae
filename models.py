# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

class Comments(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.TextProperty()