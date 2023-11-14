import os
from mitmproxy import http

class Blocker:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.blocked_websites = [line.strip() for line in file]

        # Get the absolute path to the directory containing the Python script
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the HTML file
        html_file_path = os.path.join(script_directory, 'blocked_page.html')

        with open(html_file_path, 'r') as html_file:
            self.html_content = html_file.read()

    def request(self, flow: http.HTTPFlow) -> None:
        if any(website in flow.request.pretty_url for website in self.blocked_websites):
            flow.response = http.Response.make( 403, self.html_content.encode("utf-8"),
               {"Content-Type": "text/html"}
            )


addons = [
    Blocker(r"/Path/to/blocked_websites.txt/")  # replace with your file path
]
