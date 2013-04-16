import webapp2
import jinja2
import os
from aefmodels.models import AEFUser
from aefmodels.models import BankAccount
from aefmodels.models import Currency
from google.appengine.api import users
from google.appengine.ext import ndb

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

class ViewBankAccount(webapp2.RequestHandler):
   
    def get(self):
        user = users.get_current_user()
        user = AEFUser.get_by_id(user.user_id(), parent=None)
        bank = BankAccount.query(ancestor=user.key).fetch()
        currencies = Currency.query(ancestor=bank[0].key).fetch()
        
        template_values = {
            'links': [('/profile', 'My Profile'), ('/account', 'View Bank Acount'), ('/rates', 'See Current Exchange Rates'), ('/trade', 'Trade Currency')],
            'title': 'Your Bank Balance',
            'balance': currencies
        }
        
        template = template_env.get_template('/static/html/bank.html')
        self.response.out.write(template.render(template_values))


class MakeTrade(webapp2.RequestHandler):
   
    def get(self):
        #TODO: get a list of the user's currencies
        user = users.get_current_user()
        user = AEFUser.get_by_id(user.user_id(), parent=None)
        bank = BankAccount.query(ancestor=user.key).fetch()
        currencies = Currency.query(ancestor=bank[0].key)
        template_values = {
            'links': [('/profile', 'My Profile'), ('/account', 'View Bank Acount'), ('/rates', 'See Current Exchange Rates'), ('/trade', 'Trade Currency')],
            'title': 'Trade Currency',
            'currencies': currencies
        }
        
        template = template_env.get_template('/static/html/trade.html')
        self.response.out.write(template.render(template_values))


class ViewRates(webapp2.RequestHandler):
    
    def get(self):
        
        template_values = {
            'links': [('/profile', 'My Profile'), ('/account', 'View Bank Acount'), ('/rates', 'See Current Exchange Rates'), ('/trade', 'Trade Currency')],
            'title': 'Current Exchange Rates'           
        }
        
        template = template_env.get_template('/static/html/rates.html')
        self.response.out.write(template.render(template_values))
        
        
class Transaction(webapp2.RequestHandler):
    
    def get(self):
       
        try:
            
            old_c = self.request.get('old_c')
            new_c = self.request.get('new_c')
            rate = float(self.request.get('rate'))
            amount = float(self.request.get('amount'))
            
            user = AEFUser.get_by_id(users.get_current_user().user_id(), parent=None)
            bank = BankAccount.query(ancestor=user.key).get()
            old_currency = Currency.query(Currency.code == old_c, ancestor=bank.key).get()
            new_currency = Currency.query(Currency.code == new_c, ancestor=bank.key).get()
                       
            if new_currency is None:
                new_currency = Currency(parent=bank.key, code=new_c, amount=0)
            
            old_currency.amount = float(old_currency.amount - amount)
            new_currency.amount = float(new_currency.amount + (amount * rate))
            
            ndb.put_multi([old_currency, new_currency])
            self.response.out.write('Rates.aef_handler({"transaction_status": "success"});')
            
        except Exception, e:
            
            self.response.out.write('Rates.aef_handler("transaction_status": "fail", "reason": "' + e.message + '");')
            
           
        