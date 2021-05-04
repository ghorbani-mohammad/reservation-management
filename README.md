## This is a my interview task


This task is about reservation system. Users can create their rooms and and also reserve rooms. As mentioned in the document nor Authentication or Authorization considered. So a user can update or delete room of other users.

## Features

- Used Docker for easily start APP
- Used pip-compile for package dependency management
- Included Postman collection to easily review provided APIs
- Used bash script (mng-api.sh) for some management actions. (like make migrations or migrate them)
- Provided a populate script that create sample users for testing purposes


## Start APP

In the main directory use bellow command to run app.
```
docker-compose up -d
```
Then for migrating migrations use bellow command. This command will create tables.
```
./mng-api.sh migrate
```
Then bash into api container and go to db_scripts/populate directory and then run populate script. Commands are at below:
```
./mng-api.sh bash
cd db_scripts/populate/
python 01_add_users.py
```
Now everything is ready and you can use APIs. For convenience I prepared a Postman collection. Import it into your Postman app and check Provided APIs.

## License

MIT

**Free Software, Hell Yeah!**
