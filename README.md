# HTTP server made using Python

Server made using [this](https://bhch.github.io/posts/2017/11/writing-an-http-server-from-scratch/) tutorial as guidance.

Made for the purpose of understanding the HTTP protocol, the HTTP server is built on a TCP echo server made using Python's socket library. 

In the future I intend to write an article explaining HTTP and TCP and how this server works.

# How to Run the Project

### Make a GET request

- In your terminal, navigate outside the main.py file and run:

`python main.py`

- Visit localhost and append the html file name you want to visit:

`http://127.0.0.1:8888/index.html`

### Make a POST request to one of the HTML pages and change the contents of the document.

- First run the server

`python main.py`

- Then make a POST request using curl

`curl -v -X POST http://localhost:8888/index.html`