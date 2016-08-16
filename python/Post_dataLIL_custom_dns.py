# JMQLCCPF92NIWSKS channel 176 test dns channel

import urllib2,urllib,httplib,socket,ssl,Elec,time

def MyResolver(host):
  if host == 'data.learninginventions.org':
    return '10.10.12.69'
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

error_count = 0
id = 1

dict = {'1': 'BABEHECVXXMQD95W', '2': 'Q9966C36KTI5NMCT', '3': '40CX4E19V7J3G0P5', '4': 'DVTAFANUMZ8RG6JL', '5': '7QM7M546G7RG4WMP'
, '6': 'B7G3AI0D0DZ2J1XH', '7': '7K1XG6R4I8AEHDZA', '8': '8L6IPBYKI33M4TVT', '9': 'TUD0PCTS2JWZ92AI', '10': 'GPLEXQM3CKE2V2R4'
, '11': '7W407GFVBOSS9PTU', '12': 'W8DUW0J1N5H83Z8Q', '13': '174HYQ00PGCJ0FFZ', '14': 'K4TFNXZDFEDL2F32', '15': 'QNVMRAUGUQH453RL'
, '16': '3OGCDDJGWO1602FX', '17': 'DBQ98EN3Y2FQ2CX5', '18': 'C8VTVEWPGFD5LJEH', '19': 'TC54VIPY9S3N1LR5', '20': 'SL8EGDEUX20VGJ4I'
, '21': 'C14A9ZPDBIPMBT8V', '22': 'VUHFMR0DCZR46M5F', '23': '8MGWNR90I7CJ1I5G', '24': '1Q32UTUYD7O8UUUI', '25': 'BCNZYIHY0VAA9BMB'
, '26': 'MY8C6EIW7MCE5FXK', '27': 'QELETH245N7FB941', '28': 'IVULR1U8AVE3S8U4', '29': 'FKOPUJCQWSXEAI4V', '30': '4XX5R341ED3HS1IB'
, '31': 'HCCGRJLA0H5624Z8', '32': 'EBX5H5AZ69927XCR', '33': 'GJ9XJAZ8NS8VWVHU', '34': '0JZT0I6DL8D2SO77'}

header = {'data': 'text/html'}

while True:
    if id > 34 :
        id = 1

    try:
        data = {'key': dict[str(id)], 'field1': Elec.readenergy(id),'field3': Elec.readcurr(id)}
        body = urllib.urlencode(data)
        h = urllib2.Request("http://data.learninginventions.org/update?", body, headers=header)
        resp = urllib2.urlopen(h)
        print "Channel write : " + resp.read()

    except IOError:
        error_count = error_count + 1
        print "Count Error : " + str(error_count)
        print "Cannot connect modbus channel : " + str(id)
        error = {'key': '9EVBN3MJPB2TQ28S', 'field1': error_count, 'field2': id}
        data_error = urllib.urlencode(error)
        a = urllib2.Request("http://data.learninginventions.org/update?", data_error, headers=header)
        resp = urllib2.urlopen(a)

        print "Trying to resent the data ..."
        time.sleep(1)
        data_reentry = {'key': dict[str(id)], 'field1': Elec.readenergy(id),'field3': Elec.readcurr(id)}
        data_atm = urllib.urlencode(data_reentry)
        h = urllib2.Request("http://data.learninginventions.org/update?", data_atm, headers=header)
        resp = urllib2.urlopen(h)
        print "Channel write : " + resp.read()

    print "Channel : " + str(id)
    id = id + 1
