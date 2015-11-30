# test_client.py
import datetime

from poster.encode import MultipartParam
from poster.streaminghttp import register_openers
import urllib2

def get_auth_token(username, password):
    auth_url = 'https://maxcvservices.dnb.com/rest/Authentication'
    req = urllib2.Request(auth_url)
    req.add_header('x-dnb-user', username)
    req.add_header('x-dnb-pwd', password)
    resp = urllib2.urlopen(req)
    auth_token = resp.info().getheader("Authorization")
    return auth_token

def get_next_batch_id():
    return str(1)

def get_batch_request():
    batch_request_file = open("batch_request/batch_request.xml")
    batch_request = batch_request_file.read()

    batch_request = batch_request.replace("{{filename}}", "Request.csv")
    batch_request = batch_request.replace("{{application_batch_id}}", get_next_batch_id())
    batch_request = batch_request.replace("{{message_timestamp}}", datetime.datetime.now().isoformat() + "Z")

username = 'P100000D368CF1EE8B74BB5B4322104F'
password = 'WatP1C#!'
url = "https://maxcvservices.dnb.com:8443/V2.0/Batches"
token = get_auth_token(username, password)

# Register the streaming http handlers with urllib2
register_openers()

# Start the multipart/form-data encoding of the file "DSC0001.jpg"
# "image1" is the name of the parameter, which is normally set
# via the "name" parameter of the HTML <input> tag.

request_param = MultipartParam.from_params({'request' : })

# headers contains the necessary Content-Type and Content-Length
# datagen is a generator object that yields the encoded parameters
datagen, headers = MultipartParam.from_file({"image1": open("DSC0001.jpg", "rb")})

# Create the Request object
request = urllib2.Request("http://localhost:5000/upload_image", datagen, headers)
# Actually do the request, and get the response
print urllib2.urlopen(request).read()