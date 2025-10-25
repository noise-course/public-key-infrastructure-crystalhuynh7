# Write Up

## Task 1: Host a Local Web Server
In my assignment directory, I created a site directory that contains index.html with the header text "This is an unencripted site!!". I then used HTTP server in Python with the command "python3 -m http.server 8000" and opened the site in my browser.

![Local host screenshot](Local%20Host.png)


## Task 2: Identify why HTTP is not secure

Using Wireshark, I started capturing on loopback and filtering HTTP requests by port 8000, which is where my local server is being hosted. Once I refreshed and reloaded the site, I was able to see client requests (me refreshing) to the Python web sever (HTTP server). Upon inspecting the web traffic, I was able to find the GET HTTP request and the response.

![Web Traffic Capture](<Web Traffic Capture.png>)

When right-clicking the request, I was also able to follow the TCP stream from the HTTP request and highlight the response, which revealed my header text "This is an unencrypted site!!". Using Wireshark, I was able to capture and read the plain text that was on the site; meaning that others on the same network would be able to do so as well since it is not encrypted. 

![Following TCP Trace](<Following TCP Trace .png>)

## Task 3: Create a self-signed certificate and upgrade your web server to HTTPS

I cannot obtain an SSL certificate for my local web server from a certificate authority because my local web sever doesn't have a public domain name that can be traced back through DNS. The certificate authrority cannot confirm that I own the domain because my localhost server doesn't have a public DNS entry.

In order to generate an SSL certifcate, I used OpenSSL but I also created a separate SAN file file in case my Chrome tab didn't allow for my certificate to be recognized. I used the OpenSSL command to create my private key and my certificate. 

openssl req -x509 -nodes -newkey rsa:2048 \
  -keyout localhost.key -out localhost.crt \
  -days 365 -config san.cnf


To trust the certificate on my computer, I added the certificate to my Keychain Access. Then, I created a https.server file to encrypt my traffic with TLS using my certificate and key. This is where I ran into trouble - because I was ssh'ed in my linux.uchicago.edu, the server was running on the remote machine's 127.0.0.1 instead of my laptop's, so when I would run https://127.0.0.1:8443/ or https://127.0.0.1:9443/ (after I tried changing ports) it wouldn't connect. 

To fix this, I had to tunnel the remote machine's 8443 port to my laptop, which I did using ssh -N -L 127.0.0.1:9443:127.0.0.1:8443 crystalhuynh@IP ADDRESS on my local terminal. Once I did this, the port was working on my laptop and I could see the message "This is an unencrypted site!!" on port 8443. 

In Wireshark, I used the filter tls || tcp.port == 8443 to locate the port and the traffic revealed that when the request is made, it says Client Hello, and the response is Application Data, which is encrypted even when I follow the TCP trace. 

![Encrypted Traffic Capture](<Encrypted Capture.png>)

The main difference is that I am unable to access the HTML text. Instead of the GET request and the HTML response, there is a Client Hello request and a Application Data response. Due to the certificate, the contexts of the web server is hidden from those trying to access my information due to the encryption.