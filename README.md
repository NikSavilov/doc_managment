# Document management application
## Done during "Web-programming" course at ITMO UNIVERSITY
### Author: Savilov N.S., group M3400

### Intro

lalala

## Installation
Firstly, clone the repository. Then:
```
cd doc_management
sudo -s
```

### MySQL
 
```
sudo yum update
sudo wget https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
sudo rpm -Uvh mysql80-community-release-el7-3.noarch.rpm
sudo yum install mysql-server
sudo systemctl start mysqld
sudo systemctl status mysqld
sudo grep 'password' /var/log/mysqld.log
```
Check root password in output, then change it by:
```
sudo mysql_secure_installation
```
Create db, user (remove <set password> by needed one)
```
mysql -u root -p
CREATE DATABASE docmanager;
CREATE USER 'django'@'localhost' IDENTIFIED BY '<set password>';
GRANT ALL PRIVILEGES ON docmanager.* TO 'django'@'localhost'
grant all privileges on test_docmanager.* to django@localhost;
FLUSH PRIVILEGES;
```

[MySQL Installation Tutorial](https://www.hostinger.ru/rukovodstva/ustanovka-mysql-na-centos-7/)

### Config Django to use MySql 

Create ./secret/MySql.cnf

```
[client]
database = docmanager
host = localhost
user = django
password = <password>
default-character-set = utf8
wait_timeout = 28800
```

### Setting up environment, installing requirements

```
python3 -m venv venv
source venv/bin/activate
sudo yum install python3-devel mysql-devel
python3 -m pip install -r requirements.txt
```

