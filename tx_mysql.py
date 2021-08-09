
import requests
import json
import mysql.connector
from datetime import datetime
import logging
import dbconfig as cfg
import math
from collections import defaultdict

def main():
	initLogger()
	logging.info("start token tx ingestion")
	try:
		# conn = ""
		# prevHash = ""
		conn = initDbConn()
		linkTokenSymbol = "LINK"
		linkTokenContract = cfg.tokenSymbolMap["LINK"]
		prevHash = getLatestHash(conn, linkTokenSymbol)
		result = getTokenTransactions(linkTokenContract, 10000)
		processTxs(conn, prevHash, result)
	except Exception as e:
		logging.error(e)
	finally:
		logging.info("finally")
		closeDbConn(conn)

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

def getLatestHash(conn, symbol):
	logging.info("start")
	cur = conn.cursor(prepared=True)
	query = """SELECT hash FROM tokenTransaction where tokenSymbol=%s ORDER BY id desc LIMIT 1"""
	cur.execute(query, (symbol, ))
	result = cur.fetchone()
	prevHash = ""
	if(cur.rowcount > 0):
		prevHash = result[0].decode()
		logging.info("Lastest hash from tokenTransaction table: %s", prevHash)
	cur.close()
	return prevHash

def getTokenTransactions(contractAddress, count):
	logging.info("start")
	etherScanApiKey = "XSU69HHDU44UH4WBEWJVPU5C8QZ6E7KUAD"
	url = "https://api-cn.etherscan.com/api?module=account&action=tokentx&contractaddress=" + contractAddress + "&page=1&offset=" + str(count) + "&sort=desc&apikey=" + etherScanApiKey
	response = requests.get(url)
	address_content = response.json()
	result = address_content.get("result")
	return result

def dumpFile(txs):
	logging.info("start")
	filePath = "/home/emilych404/data/"
	fileName = datetime.now().strftime('tx-%Y-%m-%d-%H-%M-%S.json')
	jsonObject = json.dumps(txs, indent = 4)
	jsonFile = open(filePath+fileName, "w")
	jsonFile.write(jsonObject)
	jsonFile.close()
	logging.info("exit")

def processTxs(conn, prevHash, txs):	
	logging.info("start processing %d txs", len(txs))
	if(len(txs) != 0):
		valueAccumulator = 0
		newTx = []
		hashCount = defaultdict(int)

		# find where we stopped last time
		for count, tx in enumerate(txs):
			hash = tx.get("hash")
			if hash == prevHash:
				logging.info("Break after processing record %d", count)
				break
			newTx.append(tx)
			hashCount[hash] += 1 # dict to track multi-transfer transactions
		hashCountCopy = hashCount.copy()
		dumpFile(newTx)

		for i in range(len(newTx)-1, -1, -1): # iterate in reverse order
			# parse data
			tx = newTx[i]
			blockNumber = tx.get("blockNumber")
			timeStamp = tx.get("timeStamp")
			hash = tx.get("hash")
			nonce = tx.get("nonce")
			blockHash = tx.get("blockHash")
			txFrom = tx.get("from")
			tokenSymbol = tx.get("tokenSymbol")
			txTo = tx.get("to")
			value = tx.get("value")
			transactionIndex = tx.get("transactionIndex")
			gas = tx.get("gas")
			gasPrice = tx.get("gasPrice")
			gasUsed = tx.get("gasUsed")
			cumulativeGasUsed = tx.get("cumulativeGasUsed")
			input = tx.get("input")
			confirmations = tx.get("confirmations")
			fee = int(gasPrice) * int(gasUsed)
			formattedDate = datetime.fromtimestamp(int(timeStamp))
			valueAccumulator += int(value)

			# prepare SQL insert
			txDataTuple = (formattedDate, blockNumber, timeStamp, hash, nonce, blockHash, txFrom, tokenSymbol, txTo, str(valueAccumulator), transactionIndex, gas, gasPrice, gasUsed, str(fee), cumulativeGasUsed, input, confirmations)
			transferDataTuple = (blockNumber, timeStamp, hash, nonce, blockHash, txFrom, tokenSymbol, txTo, value, transactionIndex, gas, gasPrice, gasUsed, cumulativeGasUsed, input, confirmations)

			insertTxQuery = """INSERT INTO tokenTransaction (txDate, blockNumber, timeStamp, hash, nonce, blockHash, txFrom, tokenSymbol, txTo, value, transactionIndex, gas, gasPrice, gasUsed, fee, cumulativeGasUsed, input, confirmations) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			insertTransferQuery = """INSERT INTO tokenTransfer (blockNumber, timeStamp, hash, nonce, blockHash, txFrom, tokenSymbol, txTo, value, transactionIndex, gas, gasPrice, gasUsed, cumulativeGasUsed, input, confirmations) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

			if(hashCount.get(hash) == 1):
				logging.debug("insert %s to transaction table", hash)
				executeQuery(conn, insertTxQuery, txDataTuple)
				valueAccumulator = 0
			else:
				logging.debug("insert %s to transfer table", hash)
				executeQuery(conn, insertTransferQuery, transferDataTuple)
				hashCountCopy[hash] -= 1
				if(hashCountCopy.get(hash) == 0):
					logging.debug("insert last %s to transaction table", hash)
					executeQuery(conn, insertTxQuery, txDataTuple)
					valueAccumulator = 0
	logging.info("exit")

def executeQuery(conn, query, dataTuple):
	logging.debug("start")
	logging.debug(dataTuple)
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