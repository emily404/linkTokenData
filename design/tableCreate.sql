create table token(
createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
tokenSymbol VARCHAR(32) NOT NULL,
tokenName VARCHAR(32) NOT NULL,
tokenDecimal INT NOT NULL,
contractAddress VARCHAR(64) NOT NULL,
   PRIMARY KEY ( tokenSymbol )
);

create table tokenTransaction(
id INT NOT NULL AUTO_INCREMENT,
createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
txDate TIMESTAMP NOT NULL,
blockNumber INT NOT NULL,
timeStamp INT NOT NULL,
hash VARCHAR(128) NOT NULL,
nonce INT NOT NULL,
blockHash VARCHAR(72) NOT NULL,
txFrom VARCHAR(64) NOT NULL,
tokenSymbol VARCHAR(32) NOT NULL,
txTo VARCHAR(64) NOT NULL,
value VARCHAR(64) NOT NULL,
transactionIndex INT NOT NULL,
gas INT NOT NULL,
gasPrice VARCHAR(64) NOT NULL,
gasUsed INT NOT NULL,
fee VARCHAR(64) NOT NULL,
cumulativeGasUsed VARCHAR(64) NOT NULL,
input BLOB,
confirmations INT NOT NULL,
   PRIMARY KEY ( hash ),
   UNIQUE KEY (id),
   INDEX h_ind (hash),
   FOREIGN KEY (tokenSymbol)
        REFERENCES token(tokenSymbol)
);

create table tokenTransfer(
id INT NOT NULL AUTO_INCREMENT,
blockNumber INT NOT NULL,
timeStamp INT NOT NULL,
hash VARCHAR(128) NOT NULL,
nonce INT NOT NULL,
blockHash VARCHAR(72) NOT NULL,
txFrom VARCHAR(64) NOT NULL,
tokenSymbol VARCHAR(32) NOT NULL,
txTo VARCHAR(64) NOT NULL,
value VARCHAR(64) NOT NULL,
transactionIndex INT NOT NULL,
gas INT NOT NULL,
gasPrice VARCHAR(64) NOT NULL,
gasUsed INT NOT NULL,
cumulativeGasUsed VARCHAR(64) NOT NULL,
input BLOB,
confirmations INT NOT NULL,
   PRIMARY KEY ( id ),
   INDEX h_ind (hash)
);

create table tokenBalance(
id INT NOT NULL AUTO_INCREMENT,
createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
balance VARCHAR(64) NOT NULL,
tokenSymbol VARCHAR(32) NOT NULL,
address VARCHAR(64) NOT NULL,
   PRIMARY KEY ( id ),
   INDEX a_ind (address),
   FOREIGN KEY (tokenSymbol)
        REFERENCES token(tokenSymbol)
);


