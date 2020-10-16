# Document management application
## Done during "Web-programming" course at ITMO UNIVERSITY
### Author: Savilov N.S., group M3400

### Intro

lalala

### Installation

MySQL 
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


```
