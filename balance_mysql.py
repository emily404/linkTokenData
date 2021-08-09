
import requests
import json
import mysql.connector
from datetime import datetime
import logging
import dbconfig as cfg
import math

def main():
	initLogger()
	logging.info("start token balance ingestion")
	try:
		conn = initDbConn()
		tokenSymbol = "LINK"
		linkTokenContract = cfg.tokenSymbolMap["LINK"]
		addressList = getAddressOfInterest()
		for add in addressList:
			balance = queryBalance(linkTokenContract, add)
			balanceNum = float(balance) / math.pow(10, 18)
			logging.info("address %s, balance %s", add, balance)
			insertBalanceQuery = """INSERT INTO tokenBalance (balance, balanceNum, tokenSymbol, address) VALUES (%s, %s, %s, %s)"""
			balanceDataTuple = (balance, balanceNum, tokenSymbol, add)
			executeQuery(conn, insertBalanceQuery, balanceDataTuple)
	except Exception as e:
		logging.error(e)
	finally:
		logging.debug("finally")
		closeDbConn(conn)

def queryBalance(tokenContract, add):
	url = "https://api-cn.etherscan.com/api?module=account&action=tokenbalance&contractaddress=" + tokenContract + "&address=" + add + "&tag=latest&apikey=" + cfg.etherScan["apiKey"]
	response = requests.get(url)
	content = response.json()
	balance = content.get("result")
	return balance

def getAddressOfInterest():
	addressList = ["0x3cd751e6b0078be393132286c442345e5dc49699",
	"0x56178a0d5f301baf6cf3e1cd53d9863437345bf9",
	"0x21a31ee1afc51d94c2efccaa2092ad1028285549",
	"0x28c6c06298d514db089934071355e5743bf21d60",
	"0x37bC7498f4FF12C19678ee8fE19d713b87F6a9e6",
	"0xAe74faA92cB67A95ebCAB07358bC222e33A34dA7",
	"0xDfd03BfC3465107Ce570a0397b247F546a42D0fA",
	"0x789190466E21a8b78b8027866CBBDc151542A26C"]
	return addressList

def initLogger():	
	logging.getLogger().setLevel(logging.INFO)
	logFormat = "[%(asctime)s][%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
	logging.basicConfig(format=logFormat)
	logging.info("log initialized")

def initDbConn():
	logging.info("initialize db connection")
	conn = mysql.connector.connect(user=cfg.mysql["user"], password=cfg.mysql["pw"], host=cfg.mysql["host"], database=cfg.mysql["db"])
	return conn

def closeDbConn(conn):
	logging.info("closing db connection")
	try:
		conn.close()
	except Exception as e:
		logging.error(e)

def executeQuery(conn, query, dataTuple):
	logging.debug("start")
	try:
		cur = conn.cursor(prepared=True)
		cur.execute(query, dataTuple)
		conn.commit()
		cur.close()
	except mysql.connector.IntegrityError as err:
		logging.error("Integrity Error: %s", err)
	except Exception as e:
		logging.error("executeQuery Error: %s", e)

if __name__ == "__main__":
    main()