import webapp2
import jinja2
import os
from aefmodels.models import AEFUser
from aefmodels.models import BankAccount
from google.appengine.api import users
from aefcontrollers.controllers import *

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

class MainPage(webapp2.RequestHandler):
    def get(self):
        
        template_values = {
            'title': 'aefinance',
            'url': users.create_login_url('/signin'),
            'link_text': 'Sign in using your google account'
        }
        template = template_env.get_template('/static/html/index.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(template_values))
        #http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22http%3A%2F%2Fwww.missoulaavalanche.org%2Fcurrent-advisory%2F%22%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22content%22%5D%2Fdiv%5B1%5D'&format=json
        #select * from yahoo.finance.exchange where pair in ("EURUSD","GBPUSD")
        #http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20(%22EURUSD%22%2C%22GBPUSD%22)&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=cbfunc
        
class SignIn(webapp2.RequestHandler):
    def get(self):
        
        user = users.get_current_user()
        if(user):
            aefuser = AEFUser.get_by_id(user.user_id(), parent=None)
            if(aefuser):
                pass
            else:
                user = AEFUser(id=user.user_id(), email=user.email())
                user_key = user.put()
                bank_account = BankAccount(parent=user_key)
                bank_account.put()
                
        self.redirect('/profile')
        
class Profile(webapp2.RequestHandler):
    def get(self):
        
        template_values = {
            'title': 'My Profile',
            'links': [('/profile', 'My Profile'), ('/account', 'View Bank Acount'), ('/rates', 'See Current Exchange Rates'), ('/trade', 'Trade Currency')]
        }
        
        template = template_env.get_template('/static/html/profile.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(template_values))
   
application = webapp2.WSGIApplication([('/', MainPage), ('/signin', SignIn), ('/profile', Profile), ('/rates', ViewRates), ('/trade', MakeTrade), ('/account', ViewBankAccount)], debug=True)