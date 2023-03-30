This are the following files that requires manual change:
middleware/fileUpload.js -> ./uploads #Change to where location of folder to store images
config/databaseConfig.js #Change credentials


What is docker?
- It removes the "It works on my computer" problem.
- It standardises the environment so nothing needs to be changed, just run a command.

Should you decide use the docker version run the following command:

sudo docker-compose up -d #To turn on
sudo docker-compose down  #To turn off

#Change the docker-compose.yml environment password, if u want a different password as well as config/databaseConfig.js


Data entry contains "all" the insert I used for testing and all the postman converted to curl


What is the difference between workbench.sql and db.sql?
- workbench is the exported one from workbench
- db.sql was manually typed by me