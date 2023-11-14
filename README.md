# URL-Filtering
# Network Proxy with URL Filtering

This repository contains a simple Python script (`filter.py`) that acts as a basic proxy server with URL filtering capabilities. 
The script intercepts incoming HTTP requests, extracts the requested URL, checks against a blacklist, and either allows or blocks the request.

Deployment and Running of the code:
  If we want to run the proxy server, whether from the custom HTTP proxy or using the mimtmproxy on your local machine, we use the loop back trick to revert the messages to our local machine So, If you are using Windows, you should open the proxy settings, and configure the local address of machine and port number the proxy listening to set up the proxy on your machine. The modules imported in the python script are cross-platform.
  
Features:
  Proxy Server:Acts as a proxy server between the user's browser and the actual web server.
  URL Filtering: Blocks access to websites listed in the provided `blacklist.txt` file.
  Dynamic Port Handling: Handles both HTTP and HTTPS requests on different ports.
  Error Handling: Provides basic error handling for different scenarios.

Prerequisites
    Python: Ensure you have Python installed on your system. The script is compatible with Python 3.
    mitmproxy: Install mitmproxy by following the instructions on the official mitmproxy installation guide.
      Refer: https://docs.mitmproxy.org/stable/overview-installation/

Configuration:
  Blacklist: Add websites to the `blacklist.txt` or `blocked_websites.txt` file, with each URL on a new line.
    Example `blacklist.txt`:
    ```
    example.com
    blocked-site.com
    ```
    
Notes:
  HTTPS Handling: The script currently does not handle HTTPS connections due to the lack of SSL certificate decryption.
  Blocking Message: When a blocked website is accessed, a simple "404 Page Not Found" message is sent to the client.

Contributing:
  Feel free to contribute by submitting issues or pull requests. Your feedback and contributions are highly appreciated!
