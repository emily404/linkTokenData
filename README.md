# linkTokenData

# Create Linux server and SQL server
GCP->ComputeEngine->CreateInstance->Select boot image Ubuntu 18.04 LTS \
GCP->SQL->CreateInstance->Select MySQL 8.0

# Install MySQL client on Linux server
sudo apt-get update \
sudo apt-get install default-mysql-server \
mysql --host=35.241.96.104 --user=root --password

# Install python libraries on Linux server
sudo apt-get install python3-pip \
pip3 install requests \
pip3 install mysql-connector 

# Run data ingestion script manually
python3 tx_mysql.py \
python3 balance_mysql.py 
