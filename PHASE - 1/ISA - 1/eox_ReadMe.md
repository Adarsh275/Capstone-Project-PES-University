# EOS-3.0 DEV ENVIRONMENT SETUP


Development Environment setup for application development at EOX Vantage.

## Installations

### \* Please install the recommended markdown reader by the command mentioned below to read this readme properly

```bash
sudo apt install remarkable
```

## 1. Install Smartgit

### Install git command line

```bash
sudo apt install git
```

#### Download Smartgit from the Official Website

- Download the debian bundle of smartgit for easy installation

##### GIF: HOW TO INSTALL SMARTGIT

[smartgit-installation]

- Once Installed you can generate ssh keys and update them in your gitlab account for you to connect the git repository and enable you to do version control without password or you can enter your git account credential to pull code.

##### GIF: HOW TO GENERATE KEYS

[key generation]

- After you have generated the keys update the public part of key to gitlab account

##### GIF: HOW TO ADD KEYS TO GITLAB

![Add Keys]

- Open Smartgit and goto repository tab and select clone to start cloning the codebase to your local machine.

- You need to know the gitlab repository address to clone it which you can find in the gitlab server i.e `code.oxzion.com`.

- We have different branches for different projects going on. The QA branch is for Development Team. Please clone or checkout if already cloned to the required branch to work on.

##### GIF: HOW TO CLONE A REPOSITORY IN SMARTGIT

![clone]

## 2. Install Docker

To learn how to install Docker [click here.](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)

##### Link: HOW TO CLONE A REPOSITORY IN SMARTGIT OR RUN THE FOLLOWING COMMANDS in terminal

```bash
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
sudo apt install docker-ce
```

##### Docker should now be installed, the daemon started, and the process enabled to start on boot. Check that it’s running

```bash
sudo systemctl status docker
```

Note: Use `sudo` to run docker command

## 3. Install MySql 5.7

To learn how to install MySql on Ubuntu 18.04 [click here.](https://linuxize.com/post/how-to-install-mysql-on-ubuntu-18-04/)

To learn how to install MySql on Ubuntu 20.04 [click here.](https://computingforgeeks.com/how-to-install-mysql-on-ubuntu-focal/)

OR RUN THE FOLLOWING COMMANDS in terminal

```bash
sudo apt update
sudo apt install mysql-server
```

Once the installation is completed, the MySQL service will start automatically. To check whether the MySQL server is running, type

```bash
sudo systemctl status mysql
```

### Login to mysql client with superuser privilege for the first time

```bash
sudo mysql
```

After installing mysql update your root password. If you want to login to your MySQL server as root from an external program such as phpMyAdmin.

Change the authentication method from auth_socket to mysql_native_password. You can do that by running the following command:</h5>

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY  'very_strong_ password';
FLUSH PRIVILEGES;
```

To exit the client

```sql
\q or exit

```

After updating the root password you can login with the new password that you have set by the following

```sql
mysql -u 'user_name'  -p 'password'
```

## 5. Database Creation

- Update bind-address in mysql configuration to allow external connections using ipv4 address

```bash
vi /etc/mysql/mysql.conf.d/mysqld.cnf
```

look for `bind-address = 127.0.0.1`

update it to `0.0.0.0`

#### login to your mysql client

- Database for API

- create database oxzionapi;

- Database for workflow integration

- create database `process-engine`;

- Database for camel integration

- create database quartz_db;

## 6. Build API Docker using [docker-compose](https://docs.docker.com/compose/)

- For global credential update, copy .env.example to .env and change the credential according to your ip and other credentials

```bash
cp .env.example .env
```

- To start api, camunda workflow, camel with activemq, view run below command

```bash
docker-compose up -d --build
```

- Once the above service is up, you get into bash using below command for each services

Example for api (check docker-compose.yml for services name)

```bash
docker-compose run zf /bin/bash
```

- Copy local.php.dist to local.php inside api/v1

```bash
cp api/v1/config/autoload/local.php.dist api/v1/config/autoload/local.php
```

- At this point, you can visit http://localhost:8080 to see the site running.

- You can also run composer from the image. The container environment is named "zf", so you will pass that value to `docker-compose run`:

```bash
docker-compose run zf composer install
```

## 7. Build View Docker

### Prerequisites

- Copy `cp .env.example .env` in all the apps under `view/apps` to your host

#### _Example_

```bash
cd apps/Admin
cp .env.example .env
```

- Run the below command to setup the local,js and .env file in your view repo

```bash
cp view/bos/src/server/local.js.example view/bos/src/server/local.js
cp view/bos/src/osjs-server/.env.example view/bos/src/osjs-server/.env
cp view/bos/src/client/local.js.example view/bos/src/client/local.js
```

Once the changes to .

To build the docker

```bash
# Build the Docker
docker build -t view docker/
docker-compose up -d --build

# To enter in view bash mode run below command
$ docker exec -it view_vw_1 bash

# inside the view container you can run the following command
# To build and apps open the apps folder and run the following command
# Ex:

cd /app/view/apps/Admin
npm install
npm run build:dev
```

Repeat this for all the built-in apps inside the apps folder. You can run the above commands to build the themes `/app/view/themes/Vision` , Icons Packs `/app/view/themes/oxzioniconpack`

Once all the apps are built you can open the bos and build it

```bash
To build the bos
cd /app/view/bos
npm install # to install app
npm run build:dev # to run the build
npm run watch:dev # to watch the files, every files save will automatically build the view
npm run package:discover
```

Once the all the apps and bos is build you can start the view by running the below command in the `/app/view` folder

```bash
cd /app/view/
npm run serve
```

Now you can login to http://localhost:8081

## 8. Build MySQL using docker

Open `integrations/mysql` folder

Copy the `.env.example` to `.env` file and update the credentials for mysql that you want.

```bash
cp env.example .env
```

To run services in foreground mode

```bash
docker-compose up
```

To run services in background mode

```bash
docker-compose up -d
```

To shut down the services in background mode run this from the directory where the docker-compose.yml exists

```bash
docker-compose down
```

If running in Foreground mode

CTRL+C on the running terminal will start the shutdown of the services.

### Note

1. After the services have started successfully PhPMyAdmin page is available at http://localhost:8082.

2. To connect mysql from a client application running on the host machine use 3307 as the port the configurations.

3. A directory named 'sql' has been provided and it can be used to keep the scripts and database dumps.

4. To import any sql script including database dump a shell script has been provided for easy use. It uses two parameters to import. First the "database_name" and second the `dot-sql_filename` (.sql).

#### Example

To import database using script

1. Put the `dot-sql_filename` file inside the sql folder

2. Run the command

```bash
import.sh database_name dot-sql_filename
```