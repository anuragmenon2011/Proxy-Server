Data Communication programming Assignment 3

Code deesign and implementation.

1. The proxy serverlistens to the port number provided by the user. The user also provides a cache timeout value.
2. CheckArgs() method verifies the arguments provided by the user.
3. The program enters themain program and a TCP socket is createdand stores the address and port number of the client
   and creates a thread using the thread utility of python and passes control to the proxy call method.
4. This is the method were actual request is sent to the webserver requested.
5. The program checks if the TCP requestmethod is 'GET' and the version is HTTP/1.0. Only these requests are catered by
   the proxy server.
6. Using regular expression weextract the host and port from the request method and create a new TCP connection with the
   actual webserver using socket.connect.
7. We then forward the actual request to the web server and the response we receive is sent back to the client.

Content - Caching:

1. The response we get from the web server is stored in the dictionary and also the time stamp is added to another
   dictionary.
2. The key for both the dictionaries will be the sha256() of the request URL
3. Every time request comes we check if there is a value stored for the sha256() of the url.
4. If there exists a vlaue, we send the corresponding content back to the client and the request is not forwarded to the
   web server.
5. We also check if the difference between the current time stamp and the time stamp when the content was added to the
   dictionary is not greater than the timeout value. If so, we clear the dictionary and send the request to the web server
   and add that value to the dictionary. 