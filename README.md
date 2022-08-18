# Project - FullStack, Telegram Bot
## 	236369 - Managing Data on The World-Wide Web
### channel on Telegram - PollsBot

Full project which give service for admins for sending polls and view statistics from users at PollSBot channel on Telegram.

Note for configuration -
<br/>
Configuration for the project are at:
<br/>
 Backend - configuration\config.py - are the configuration for connecting postgres, Bot API and flask-server.
 <br/>
 Fronted - fronted_react\src\config.ts - the server path address for react for sending requests to.
 <br/>
 **!!Notice that server path on the fronted should matched the server path of the flask-server at the backend!!** (host and port).
 <br/>
 Also, You might encounter Cors-Policy blocking on the fronted side, if so, download, install and activate
 Allow CORS: Access-Control-Allow-Origin extension for Google Chrome. (2 minutes action)<br/>
 On the link : 
  <br/>
 https://chrome.google.com/webstore/detail/allow-cors-access-control/lhobafahddgcelffkeicbaginigeejlf?hl=en
 

How to start? 
<br/>

ALL STEPS SHOULD EXECUTE FROM CONDA ENVIRONMENT, working on win10 os! (try  from cmd, if it doesn't work try with anaconda prompt).
<br/>
Note that 2 and 3 steps can be done by by run run_project.py script.
<br/>
1. Create a new conda environment with the environment.yml file.
2. Run main.py which will run the backend of the app  
(initialize and connect to postgres DB, run the flask server and the telegram server).
3. Run npm install and  npm start inside the fronted_react to run the react server and open your browser.



 Enjoy! 
