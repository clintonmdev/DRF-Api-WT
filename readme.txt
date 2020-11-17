Weather service technical Challenge By Clinton M.
=========================================

Set up :
------

* Create a virtual environment
* make migrations
* install the libraries from the requirements.txt
* run the server


The service :
------------

-*- health check : $ curl -si http://localhost:8080/ping

Because the api has been secured, you will need login or provide a token to access its functionalities.

There is user already created that you can use for that matter : 

	username = admin & password = secret. 


If you want to get the authentication token yourself, you can make the following call :

	curl -X POST http://localhost:8080/api-token-auth/ -d 'username=admin&password=secret'



Otherwise it should have provided you this line : d6e37f351eaa82640eccad9cd247f094dfa8a60a

-*- to get the current weather : 

	 curl -si http://localhost:8080/forecast/london/ -H 'Authenticate: Token d6e37f351eaa82640eccad9cd247f094dfa8a60a' 

-*- you can configure the temperature unit by adding 

	'/(temperature unit of your choice)'.

Test :
-----

All you need to is to run the test command.
I have provided a copy of the Api key used for this challenge on the documentations.txt file.


Extra:
______

I have added the cache functionality to the api to avoid making unnecessary requests to the 3rd party api. This app uses memcache because I judged it to be the most efficient approach for this project as the database is almost unnecessary apart for the User model.
