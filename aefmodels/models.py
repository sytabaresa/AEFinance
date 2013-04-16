import webapp2
from google.appengine.ext import ndb


class AEFUser(ndb.Model):
    email = ndb.StringProperty(required=True)
    
    #TODO: define a user's profile
    
    
class Currency(ndb.Model):
    code = ndb.StringProperty(required=True)
    amount = ndb.FloatProperty(required=True)

class BankAccount(ndb.Model):
    balance = ndb.FloatProperty(default=1000)
    