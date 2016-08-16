import urllib2,urllib,httplib,socket,ssl,Elec,time

# init variables
error_count = 0
id = 1
dict = {'key':'value'} # api write key from your channel on datalogging

# Post data function
def senddata(data):
    body = urllib.urlencode(data)
    h = urllib2.Request("https://data.learninginventions.org/update?", body)
    try:
        resp = urllib2.urlopen(h)
        return resp.read()
    except:
        pass

# Custom dns methods by using socket / httplib
def MyResolver(host):
  if host == 'data.learninginventions.org':
    return 'ip address' # input ip address for custom dns
  else:
    return host

class MyHTTPConnection(httplib.HTTPConnection):
  def connect(self):
    self.sock = socket.create_connection((MyResolver(self.host),self.port),self.timeout)

class MyHTTPSConnection(httplib.HTTPSConnection):
  def connect(self):
    sock = socket.create_connection((MyResolver(self.host), self.port), self.timeout)
    self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file)

class MyHTTPHandler(urllib2.HTTPHandler):
  def http_open(self,req):
    return self.do_open(MyHTTPConnection,req)

class MyHTTPSHandler(urllib2.HTTPSHandler):
  def https_open(self,req):
    return self.do_open(MyHTTPSConnection,req)

opener = urllib2.build_opener(MyHTTPHandler,MyHTTPSHandler)
urllib2.install_opener(opener)

# main program
while True:
    if id > 34 :
        id = 1
    try:
        data = {'key': dict[str(id)], 'field1': Elec.readenergy(id),'field3': Elec.readcurr(id)}
    except IOError:
        error_count += 1
        print "Count Error : %s" % error_count
        print "Cannot connect modbus channel : %s" % id
        error = {'key': 'value', 'field1': error_count, 'field2': id} # channel for error records
        print senddata(error)
        time.sleep(1)
        try:
            data = {'key': dict[str(id)], 'field1': Elec.readenergy(id),'field3': Elec.readcurr(id)}
        except IOError:
            id += 1
            continue
    print senddata(data)
    print "Channel : %s" % id
    id += 1
