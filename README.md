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
modify env[dataFilePath] in dbconfig.py \
python3 tx_mysql.py \
python3 balance_mysql.py 

# Dashboard
https://app.powerbi.com/links/hwYyxXRli5?ctid=4c1b219d-8712-4495-a92c-31e6db6d1883&pbi_source=linkShare \
https://app.powerbi.com/links/07zgnHPfXs?ctid=4c1b219d-8712-4495-a92c-31e6db6d1883&pbi_source=linkShare
