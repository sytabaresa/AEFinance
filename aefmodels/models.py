import webapp2
from google.appengine.ext import ndb


class AEFUser(ndb.Model):
    email = ndb.StringProperty(required=True)
    
    #TODO: define a user's profile
    
    
class CurrencyTrade(ndb.Model):
    oldCurrency = ndb.StringProperty(required=True)
    newCurrency = ndb.StringProperty(required=True)
    amount = ndb.IntegerProperty(required=True)
    

class BankAccount(ndb.Model):
    balance = ndb.IntegerProperty(default=1000)