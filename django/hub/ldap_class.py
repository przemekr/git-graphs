import ldap
import base64
import requests
import json

class LDAP:
    def __init__(self, url, sec, bind, base, default):
       self.url = url
       self.sec = sec
       self.bind = bind
       self.base = base
       self.default = default
       self.connect()

    def connect(self):
       try:
           self.l = ldap.initialize(self.url)
           self.l.bind_s(self.bind, self.sec, ldap.AUTH_SIMPLE)
       except:
           pass

    def mailToThumb(self, name, email):
       for i in [0,1,2]:
          try:
             r= self.l.search_s(self.base, ldap.SCOPE_SUBTREE, '(mail=%s)'%(email),['thumbnailPhoto'])
             for dn,t in r:
                 if 'thumbnailPhoto' in t.keys():
                     return 'data:image/jpeg;base64,'+base64.b64encode(t['thumbnailPhoto'][0])
             break
          except:
             self.connect()
             pass

       print name
       r  = requests.get('https://api.github.com/search/users?q=%s' % name)
       if r.ok:
           i = json.loads(r.text or r.content)
           if i['total_count'] != 0:
               return i['items'][0]['avatar_url']

       # the default avatar
       return self.default
