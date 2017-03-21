![Sleepify logo](http://mufff.in/i/logo2.png)
## ee4-mhml (2016-2017) Coursework
---
### Abstract

---
### Usage
1. Clone the github repository using `git clone https://github.com/jeremych1000/ee4-mhml`
2. Download the Sleepify App from _link_ or compile it yourself.
3. OPTIONAL: Create a user account using `http://sleepify.zapto.org/accounts/signup/`
> This can be done later using the mobile app too.
---

### API Reference
All API links should be pre-pended with `http://sleepify.zapto.org/api/`. POST requests should have a CSRF token in the header/cookies to prevent Cross Site Request Forgery.

| Link | Available Methods | Description| Notes |
| --- | --- | --- | --- |
| /csrf/  | GET | Returns a CSRF token in the cookies for use when POSTing.
|  /auth/registration/ | POST  |  Register a new user. | <ul><li>username</li><li>email</li><li>password1</li><li>password2</li></ul> |
|  /auth/login/ | POST  |  Login a user. | <ul><li>username</li><li>email</li><li>password</li></ul> Returns token key. |
|  /auth/logout/ | POST  | Logout a user.  |  |
|  /auth/password/reset/ | POST  | Reset a forgotten password.  | <ul><li>email</li></ul> |
|  /auth/user/ | GET, PUT, PATCH  | Edit user details.  | <ul><li>username</li><li>first\_name</li><li>last\_name</li></ul> |
|  /raw_data/ | POST  | Send raw sensor data to the database.  | <ul><li>username</li><li>data<ul><li>timestamp</li><li>HR</li><li>RR</li><li>GSR</li><li>mode</li><li>AccX</li><li>AccY</li><li>AccZ</li></ul></li></ul> |
| /stats/last/`<number_of_days>`/`feature`/ | GET  | Returns a JSON object of the logged in user's raw data for the past X days. | |
| /stats/last/`<number_of_days>`/`feature`/graph/ | GET | Returns a 640x480 graph plotted by _matplotlib_ | |
| /stats/from/`<timestamp>`/to/`<timestamp>`/`feature`/|GET  |Returns a JSON object of the logged in user's raw data from timestamp to timestamp. | |
| /make\_default/ | GET | Make a default user model. | _For development._ |
| /migrate\_feature/ | GET | Put raw data in CSV files to database. |  _For development._ |
| /get\_cal\_events/ | GET | Get a list of calendar events for the logged in user for the next day. | |
| /import\_cal\_events/ | GET | Import the logged in user's calendar into the database. | Calling this URL will update the database, deleting all previous entries of the user's events. |
| /dummy/ | POST | Show whatever you have sent in the POST request. | _For debugging purposes._ |


---
### Development
You are welcome to clone the repository and develop Sleepify yourself. Please give credit where credit is due.
#### Web server
Sleepify runs at the following URL: `http://sleepify.zapto.org`. However, this is dependent on the host. If you want to develop Sleepify locally, or run Sleepify using your own web server, follow these instructions.
1. Assuming you already have cloned the repository, install the required libraries using 
> Windows `ee4-mhml/software/web_interface/get_pip_stuff.cmd`
> UNIX `ee4-mhml/software/web_interface/get_pip_stuff.sh`
2. Decide on a port to run the webserver on, and forward that port to your hosting server/PC. Detailed instructions depending on your router can be found [here](https://portforward.com/router.htm).
> HTTP server default: 80
> Django development server default: 8000
3. Setup the Django databases using `python manage.py makemigrations; python manage.py migrate`
4. Run the webserver with the following command: `python manage.py runserver 0.0.0.0:80` and verify that the server is running by visiting `http://<your-ip>/`, `http://localhost:80/`, or `http://127.0.0.1:80/`.
> To run the server just locally, `python manage.py runserver localhost:8000` or `python manage.py runserver 127.0.0.1:8000`.
> Replace 8000 with whatever port you have forwarded.
#### iOS Application
The iOS application can be downloaded at _link_, but to develop it yourself, follow these instructions (macOS only):
1. Assuming you have cloned the repository, install Cocoapods using `sudo gem install cocoapods`
2. Go to the app folder, `ee4-mhml/software/mhml_withbackground/`, and run `pod install`. It should automatically pick out the `Podfile` inside the app folder and install the required dependencies.
3. Open the workspace using XCode, not the project - `mhml.xcworkspace`
---
### Development
You are welcome to issue pull requests, the Sleepify team will be on hand to deal with that, alongside issues. We aim to provide a response within 7 working days.