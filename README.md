# BD-Project

Project for the DataBase subject.

# DataBase Setup

To setup all configs of your database, you need to access your postgreSQL DMBS by `psql` or `pgadmin4`.
We used the `psql client` with the follow command:

```bash
# Use the default credentials:
# Username: postgres
# Password: postgres

psql -h localhost -p 5432 -U postgres
```

After acess, let's creat a `database` where are all tables and work about `database design` and connect to him:

```bash
CREATE DATABASE dbshop;

# if you run:
\l
# it should list all available databases
# a similar result:
#                                  List of databases
#   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges   
#-----------+----------+----------+-------------+-------------+-----------------------
# dbshop    | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
# postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
# template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
#           |          |          |             |             | postgres=CTc/postgres
# template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
#           |          |          |             |             | postgres=CTc/postgres
#(4 rows)

# run this command to connect to him
\c dbshop
```

Now the `database` created, everything is ready to add tables and data

```bash
\i schema.sql       # create the tables schemas
\i data.sql         # add data
```


# Co-workers

João Moreira - joaomoreira@student.dei.uc.pt https://github.com/JoaoESmoreira

Tomás Pinto - tomaspinto@student.dei.uc.pt https://github.com/TC121121