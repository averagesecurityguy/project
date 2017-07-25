#!/bin/bash


# Shell script to setup the database and service.
ROOTPWD=$(openssl rand 12 -hex)
USERPWD=$(openssl rand 12 -hex)
INSTALL_DIR=/opt/project


# Install Dependencies
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password $ROOTPWD"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $ROOTPWD"
sudo apt install -y mysql-server python3-pip libmysqlclient-dev
sudo pip3 install tornado mysqlclient


# Configure Database
mysql -uroot -p${ROOTPWD} -e "CREATE DATABASE project;"
mysql -uroot -p${ROOTPWD} -e "CREATE USER project@localhost IDENTIFIED BY '${USERPWD}';"
mysql -uroot -p${ROOTPWD} -e "GRANT ALL PRIVILEGES ON project TO 'project'@'localhost';"
mysql -uroot -p${ROOTPWD} -e "CREATE TABLE IF NOT EXISTS \`project.table\` (  \`id\` INTEGER NOT NULL AUTO_INCREMENT, \`val1\` VARCHAR(255) CHARACTER SET utf8mb4 NOT NULL, \`val2\` VARCHAR(255) CHARACTER SET utf8mb4 NOT NULL, PRIMARY KEY (\`id\`) );"

echo "MySQL passwords"
echo "  root: $ROOTPWD"
echo "  user: $USERPWD"

# Update password in config file
sed "s/password = ''/password = '${USERPWD}'/" < ${INSTALL_DIR}/project/config.py > ${INSTALL_DIR}/project/config.tmp
mv ${INSTALL_DIR}/project/config.tmp ${INSTALL_DIR}/project/config.py

# Configure Service
sudo cp service.sh /etc/init.d/project
sudo chmod +x /etc/init.d/project
sudo update-rc.d project defaults

# Start Service
sudo service project start
