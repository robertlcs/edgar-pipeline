import urllib2

def get_auth_token(username, password):
    auth_url = 'https://maxcvservices.dnb.com/rest/Authentication'
    req = urllib2.Request(auth_url)
    req.add_header('x-dnb-user', username)
    req.add_header('x-dnb-pwd', password)
    resp = urllib2.urlopen(req)
    auth_token = resp.info().getheader("Authorization")
    return auth_token

username = 'P100000D368CF1EE8B74BB5B4322104F'
password = 'WatP1C#!'
url = "https://maxcvservices.dnb.com:8443/V2.0/Batches"
token = get_auth_token(username, password)
print token