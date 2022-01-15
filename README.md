# Project - FullStack, Telegram Bot
## 	236369 - Managing Data on The World-Wide Web
### channel on Telegram - PollsBot

Full project which give service for admins for sending polls and view statistics from users at PollSBot channel on Telegram.

Note for configuration:
Configuration for the project are at
 Backend - configuration\config.py - are the configuration for connecting postgres, bot api and flask-server.
 Fronted - fronted_react/src/app-constants - the server path address for react to send request from.
 Notice that server path on the fronted should matched the server path of the flask-server at the backend! (host and port).
 

How to start?
1. create a new conda environment with the environment.yml file.
2. Run main.py which will run the backend of the app. 
(initialize and connect to postgres DB, run the flask server and the telegram server).
3. run npm install and  npm start inside the fronted_react to run the react server and open your browser.


 Enjoy! 
