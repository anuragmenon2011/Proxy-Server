import socket
import sys
import thread
import re
import hashlib
import datetime
from time import sleep


global host
host='localhost'
global size
size=4096
global backlog
backlog=50
cache_dict={}
timeout_dict={}


def Main():
    pr,tt=checkArgs()
    port=int(pr)
    tout=int(tt)
    #print(port,tout)
    #print(port)
    serv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serv.bind((host,port))
    serv.listen(backlog)
    while(True):
        sock,address=serv.accept()
        #print(sock,address)
        #data=sock.recv(size)
        thread.start_new_thread(proxy_call, (sock,address,tout))
        
        
    sock.close()
        
def proxy_call(so,address, tout):
    #print("Inside proxy call method")
    
    data=so.recv(size)
    #print("Socket and Address in method")
    #print(sock,address)
    if(data):
        #print(data)
        method_check=data.split('\n')[0]
        url=method_check.split(' ')[1]
        #print("This is url......"+url)
        hash=hashlib.sha256()
        hash.update(url)
        url_hash=hash.hexdigest()
        #print(url_hash)
        fl=False
        #time_fl=False
        if(url_hash in cache_dict):
            
            time_now=datetime.datetime.now()
            cache_time=timeout_dict[url_hash]
            elap=time_now-cache_time
            #print(elap)
            if(elap>datetime.timedelta(minutes=tout)):
                print("Timeout exceeded. Deleting cache values")
                del cache_dict[url_hash]
                del timeout_dict[url_hash]
            else:
                print("Inside cache result else.............")
                cached_res=cache_dict[url_hash]
                so.send(cached_res)
                fl=True
        #print(method_check)
        if(not fl): 
            req=re.match(r'GET.*',method_check)
            if hasattr(req,'group'):
                print("Inside GET method check")
                host_port=re.findall(r'Host:(.*)',data)
                #print("This is host and port from regex")
                #print(host_port)
                host_port_str=host_port[0].strip()
                #print("Port resolution")
                #print(host_port_str)
                port_pos=host_port_str.find(":")
                #print(port_pos)
                if(port_pos==-1):
                    pt=80
                    ht=host_port_str
                else:
                    ht,pt1=host_port_str.split(':')
                    pt=int(pt1)
                list_req=req.group(0).split(' ')
                vers=list_req[2].strip()
                #req_path=list_req[1].strip()
                #print(vers)
                #print(req_path)
                if(vers=='HTTP/1.0'):
                    #print("In HTTP version 1.0 check")
                    #dd=re.match(r"^[a-zA-Z0-9_:\-/.]*$",req_path)
                    
                    #print(dd)
                    #if(re.match(r"^[a-zA-Z0-9_\-:/.]*$",req_path)):
                    #print("Special characters check in URL")
                    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    #print(data)
                    #print(ht,pt)
                    data_new=data.replace("http://"+ht,'',1)
                    #print(data_new)
                    try:
                        s.connect((ht,pt))
                        s.settimeout(2.0)
                        #print("This is the socket")
                        #print(s)
                        s.send(data_new)
                    except:
                        pass
                    
                    cach=''
                    while(1):
                        try:
                            res=s.recv(size)
                            #sleep(0.2)
                            #print(res)
                        
                            if(res):
                                cach=cach+res
                                
                                so.send(res)
                            else:
                                print("Inside else...................")
                                cache_dict[url_hash]=cach
                                #print(cache_dict)
                                curr_stamp=datetime.datetime.now()
                                #print(curr_stamp)
                                timeout_dict[url_hash]=curr_stamp
                                print(len(cache_dict))
                                print(len(timeout_dict))
                                break
                        except socket.timeout:
                            print("Timedout")
                            #s.close()
                            #so.close()
                            break
                    #print(cache_dict)
                    #print(timeout_dict)
                    s.close()
                    so.close()
                        
                    #else:
                    #   print("Invalid URI")
                    #   header=("HTTP/1.0 400 Bad Request: Invalid URI\r\n"
                    #           "Connection: Keep-Alive\r\n (or Connection: close)\r\n"
                    #           "\r\n")
                    #   so.send(header.encode('utf8'))
                    #   print("Header sent")
                    #   so.send(("Error 400 Bad request: Invalid URI:"+vers).encode('utf8'))
                    #   print("Message sent")
                    #   so.close()
                    
                else:
                    print("The proxy server only forwards HTTP/1.0 requests. This is not a HTTP/1.0 request")
                    so.close()
                #    header=("HTTP/1.0 400 Bad Request: Invalid HTTP Version\r\n"
                #            "Connection: Keep-Alive\r\n (or Connection: close)\r\n"
                #            "\r\n")
                #    so.send(header.encode('utf8'))
                #    so.send(("Error 400 Bad request: Invalid HTTP request:"+vers).encode('utf8'))
                #    so.close()
                    
            else:
                print("Not a GET request")
                so.close()
                #header=("HTTP/1.0 400 Bad Request: Invalid Method\r\n"
                #        "Connection: Keep-Alive\r\n (or Connection: close)\r\n"
                #        "\r\n")
                #so.send(header.encode('utf8'))
                #so.send("Error 400 Bad request: Not a GET request".encode('utf8'))
                #so.close()
            #url=first_line.split(' ')[2]
            #print(url)
        

def checkArgs():
    if(len(sys.argv)!=2):
        print("Kindly provide the port number for the proxy server to listen")
        sys.exit()
    else:
        pr,tout=(sys.argv[1]).split('&')
        #print(pr,tout)
        return pr,tout


if __name__=="__main__":
    Main()