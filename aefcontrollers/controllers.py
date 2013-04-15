import webapp2
import jinja2
import os
from aefmodels.models import AEFUser
from aefmodels.models import BankAccount
from google.appengine.api import users

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

class ViewBankAccount(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user = AEFUser.get_by_id(user.user_id(), parent=None)
        bank = BankAccount.query(ancestor=user.key).fetch()
        
        template_values = {
            'links': [('/profile', 'My Profile'), ('/account', 'View Bank Acount'), ('/rates', 'See Current Exchange Rates'), ('/trade', 'Trade Currency')],
            'title': 'Your Bank Balance',
            'balance': bank[0].balance
        }
        
        template = template_env.get_template('/static/html/bank.html')
        self.response.out.write(template.render(template_values))


class MakeTrade(webapp2.RequestHandler):
    def get(self):
        pass


class ViewRates(webapp2.RequestHandler):
    def get(self):
        pass