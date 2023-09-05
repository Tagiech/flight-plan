# flight-plan
Export flights from rossiya-airlines personal account and put them into google calendar

First of all, to run the project you need to add config files:
1. In root create folder "configs"
2. Add google service account's configuration file
3. In the folder create file "config.py"
4. Inside this file add this variables:
   
  a. login -- login for rossiya-airlines personal account
  
  b. password -- password for rossiya-airlines personal account
  
  c. SCOPES -- array of scopes of google api
  
  d. SERVICE_ACCOUNT_FILE -- configuration file's full name
  
  e. calendarId -- identification of calendar for events to create
