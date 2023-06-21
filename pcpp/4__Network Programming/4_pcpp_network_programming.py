#  --------------- 3 - Network programming ----------
# pylint: skip-file


# ---------------- 1 - Basic concepts of network programming -----------

#  -- REST stands for Representational State (set of all properties) Transfer
#       - S : State of an object = set of all its properties, if one changes, it's called a transition
#       - T : Transfert : Transmitting states representations to and from the server.
#
#  -- BSD Sockets : 
#       - this was developed at UC Berkeley, became POSIX sockets
#       - a socket is a kind of end-point
#       - MS Windows reimplements BSD sockets in the form of the WinSock
#
# -- Socket : 
#       - domains : 'Unix' domain  for program running simultaneously on the same computer  
#       - internet domain - INET: program running on diff. machines and communicating via TCP/IP
#       - for INET : socket adress = Ip Adress (with IPv4 -> 32 bit long) +  port number : 16-bit long integer - 0..65536
#
#
# -- Protocol IP : 
#       - send a packet of data (a datagram) between two network nodes.
#       - unreliable : deas not guarantee the delivery, the integrity, or the order 
#       - upper layers compensate for these deficiencies 

# -- Protocol TCP / UDP
#       - UDP : does not use handshakes -> faster than TCP but less reliable
#       - UDP has a better performance : DNS, DHCP, etc.
#       - TCP is better for data safety : www REST mail 
#
# -- Connection-oriented vs. connectionless communication 
#       - Connection-oriented communications are usually built on top of TCP (ex : phone call)
#           - the caller is the client, it initiates the call
#           - the callee is the server
#       - Connectionless communications are usually built on top of UDP. (ex : walkie-talkies)
# 
# -- Fetching a document from a server 
#       - it's better way to use the URL (www...) than the IP address, behind which several servers can be hosted.add()


# ---------------- 2 - How to use socket in network programming -----------
import socket
server_addr = input("What server do you want to connect to? ")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.connect((server_addr, 80))
sock.send(b"GET / HTTP/1.1\rHost: " +          bytes(server_addr, "utf8") +          b"\rConnection: close\r\r")
reply = sock.recv(10000)
sock.close()
print(repr(reply))

#       - AF_INET       : symbol here to specify the Internet socket domain 
#       - SOCK_STREAM   : symbol here to specify a high-level socket able to act as a character device
#       - connect() method (and any other method whose results may be unsuccessful) raises an exception
#       - The send() method doesn't natively accept strings -> conversion in bytes
#       - sock.recv(10000) : receiving the first 10000 bytes from the response. IF more, it will be ignored
#       - It's a general practice to invoke recv() as long as it returns some data. 
#       - sock.shutdown(socket.SHUT_RDWR)
                # socket.SHUT_RD - we aren't going to read the server's messages anymore (we declare ourselves deaf)
                # socket.SHUT_WR - we won't say a word (actually, we'll be dumb)
                # socket.SHUT_RDWR - specifies the conjunction of the two previous options.

#   exceptions can raise :  socket.gaierror (connect use getaddrinfo()), ConnectionRefusedError, socket.timeout


# -- get() method 
    # GET / HTTP/1.1\r        -> GET + path + http version 
    # Host: www.site.com\r    -> host adress
    # Connection: close\r     -> close connexion
    # \r                      -> request terminator

# ---------------- 3 - Introduction to JSON -----------

# JSON : Javascript Object Notation 
# uses UTF-8 coded text 
# avoid using leading zeros
# for text, the only delimiter allowed is a quote "
# strings cannot be split over multiple lines
# boolean values : true false (preserve the case !)
# null 
# {} -> empty object 
{ "me": "Python",
	"pi": 3.141592653589,
	"parsec": 3.0857E16, 
	"electron": 1.6021766208E-19,
	"friend": "JSON",
	"off": true,
	"on": false,
	"set": null 
}


# ---------------- 4 - Using the JSON module in Python (5) -----------
import json 
# dumps() stands for dump String

# ------- serialization : from Python to JSON

# converts a float 
electron = 1.602176620898E10−19
print(json.dumps(electron)) # => 16021766189.98

# converts a string
comics = '"The Meaning of Life" by Monty Python\'s Flying Circus'
print(json.dumps(comics)) # => "\"The Meaning of Life\" by Monty Python's Flying Circus"

# converts nested lists
my_list = [1, 2.34, True, "False", None, ['a', 0]]
print(json.dumps(my_list)) # => [1, 2.34, True, "False", null, ["a", 0]]

# converts tuple nested in dict => the tuple is converted as an array
my_dict = {'me': "Python", 'pi': 3.141592653589, 'data': (1, 2, 4, 8), 'set': None}
print(json.dumps(my_dict)) # => {"me": "Python", "pi": 3.141592653589, "data": [1, 2, 4, 8], "friend": "JSON", "set": null}

# rules to remember
# Python        =>  JSON
# dict          =>  object 
# list, tuple   =>  array
# int, float    =>  number
# True, False   =>  true, false

# dumping an instance of a class is not allowed, but we can use the __dict__
class Who:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def encode_who(w):
    if isinstance(w, Who):
        return w.__dict__
    else:
        raise TypeError(w.__class__.__name__ + ' is not JSON serializable')

# raising a TypeError exception is obligatory
# dumping from Python to JSON is a serialization

# the second approach is to overload the defaut() method of the class json.JSONEncoder
# and to pass it into dumps() using the keyword argument named cls 
class MyEncoder(json.JSONEncoder):
    def default(self, w):
        if isinstance(w, Who):
            return w.__dict__
        else:
            return super().default(self, z)

some_man = Who('John Doe', 42)
print(json.dumps(some_man, cls=MyEncoder))


# ------- deserialization : from JSON to Python with json.loads() => deserialization
import json
jstr = '"\\"The Meaning of Life\\" by Monty Python\'s Flying Circus"'
comics = json.loads(jstr)
print(type(comics))     # <class 'str'>
print(comics)           # "The Meaning of Life" by Monty Python's Flying Circus


# deserialize an instance -> calling json.loads with parameter
def decode_who(w):
    return Who(w['name'], w['age'])

old_man = Who("Jane Doe", 23)
json_str = json.dumps(old_man, default=encode_who)
new_man = json.loads(json_str, object_hook=decode_who)
print(type(new_man),new_man.__dict__) #  <class '__main__.Who'> {'name': 'Jane Doe', 'age': 23}


# more complicated method, by redefining the superclass constructor
class MyDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.decode_who)

    def decode_who(self, d):
        print(self)
        print(type(d))

        return Who(**d)


some_man = Who('Jane Doe', 23)
json_str = json.dumps(some_man, cls=MyEncoder)
new_man = json.loads(json_str, cls=MyDecoder)

print(type(new_man))
print(new_man.__dict__)


# ---------------- 5 - Introduction to XML (8) -----------
<?xml version = "1.0" encoding = "utf-8"?>
<!-- comment -->
<!DOCTYPE cars_for_sale SYSTEM "cars.dtd">
# two versions currently in use: 1.0 and 1.1
# dtd : doc type definition SYSTEM (privately) or PUBLIC ()
# dtd : uses SGML
# URI : "cars.dtd"

# 2 forms for empty element
<empty/>
<empty></empty>

# tag can have one or multiple attribute
<price currency="GBP">32000</price>

# parsing an xml file, and iterating on elements and then on properties
cars_for_sale = xml.etree.ElementTree.parse('.\\cars.xml').getroot()
for car in cars_for_sale.findall('car'): 
    for prop in car:
        print(prop.tag, prop.attrib, prop.text)

# removing an element : 
cars_for_sale.remove(car)        

#  adding an element : 
new_car = xml.etree.ElementTree.Element('car')
xml.etree.ElementTree.SubElement(new_car, 'id').text = '4'
xml.etree.ElementTree.SubElement(new_car, 'brand').text = 'Maserati'
xml.etree.ElementTree.SubElement(new_car, 'model').text = 'Mexico'
xml.etree.ElementTree.SubElement(new_car, 'production_year').text = '1970'
xml.etree.ElementTree.SubElement(new_car, 'price', {'currency': 'EUR'}).text = '61800'
cars_for_sale.append(new_car)

# writing to file
tree.write('newcars.xml', method='')


# ---------------- 5 - HTTP made simple : the request module  (10) -----------

# to prepare a testing platform
npm install -g json-server
json-server --watch cars.json

# using request is easier !
import requests
reply = requests.get('http://localhost:3000') # port 80 can be omitted
print(reply.status_code)

# all HTTP code 
print(requests.codes.__dict__)

# we can use name code instead value
if reply.status_code == requests.codes.ok: 
    pass

# in headers, Content-Type indicates the the type of the response
print(reply.headers) 
reply.headers['Content-Type'] 
print(reply.text)   # main content
# ... 'Content-Type': 'text/html; charset=UTF-8', ....

# others http methods : 
# - POST : to send new data to a server
# - PUT : to update data on a server
# - DELETE, HEAD, CONNECT, OPTIONS, TRACE


# protecting request uses
try:
    reply = requests.get('http://localhost:3000', timeout=1) # in seconds
except requests.exceptions.Timeout:
    print('Sorry, Mr. Impatient, you didn\'t get your data')
else:
    print('Here is your data, my Master!')

# ---------------- 6 - CRUD how to build a simple REST client -----------

# CRUD : Create (post) Read (get) Update (post) Delete (delete) 

# in content type is JSON : 
reply.json()

# we can only on element, et perform test with  requests.codes.not_found:
reply = requests.get('http://localhost:3000/cars/2')

# and sorting the response, asc or desc
reply = requests.get('http://localhost:3000/cars?_sort=production_year')
reply = requests.get('http://localhost:3000/cars?_sort=production_year&_order=desc')

#  HTTP 1.1 
#  sends its response and keeps the connection alive, waiting for the client's next request;
#  closes silently  he connection if the client is inactive for some time
reply.headers['Connection']) # Connection=keep-alive

# the client can ask the server to close the connection 
headers = {'Connection': 'Close'}
reply = requests.get('http://localhost:3000/cars/', headers=headers)

# adding a car with resquest.post(... data=)
h_close = {'Connection': 'Close'}
h_content = {'Content-Type': 'application/json'}
new_car = {'id': 7, .............  'convertible': False}
reply = requests.post('http://localhost:3000/cars', headers=h_content, data=json.dumps(new_car))
print("reply=" + str(reply.status_code))
reply = requests.get('http://localhost:3000/cars/', headers=h_close)

# and last, PUT method 
car = {'id': 6, .... 'convertible': True}
reply = requests.put('http://localhost:3000/cars/6', headers=h_content, data=json.dumps(car))

#  ==================================================== FIN ===============================






