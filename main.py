import webapp2
import jinja2
import os
from google.appengine.api import users

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
        #select * from yahoo.finance.xchange where pair in ("EURUSD","GBPUSD")
        
class SignIn(webapp2.RequestHandler):
    def get(self):
        
        self.redirect('/profile')
        
class Profile(webapp2.RequestHandler):
    def get(self):
        
        template_values = {
            'title': 'My Profile'
        }
        
        template = template_env.get_template('/static/html/profile.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(template_values))
        
    
application = webapp2.WSGIApplication([('/', MainPage), ('/signin', SignIn), ('/profile', Profile)], debug=True)