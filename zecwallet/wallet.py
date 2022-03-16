from decimal import Decimal
from json import loads
from subprocess import PIPE , Popen



class Wallet():
	def __init__(self , WALLET_EXEC_FULL_PATH , WALLET_DECRYPTION_KEY = ''):
		self._WALLET_DECRYPTION_KEY = WALLET_DECRYPTION_KEY
		self._sp = Popen([WALLET_EXEC_FULL_PATH] , stdout = PIPE , stdin = PIPE)
		self._readOutput()


	def __del__(self):
		self._sendCommand('quit')
		self._sp.stdin.close()
		self._sp.terminate()


	def addresses(self):
		'''
		List current addresses in the wallet
		'''

		addressesCommand = ('addresses')
		return self.communicate(addressesCommand)


	def balance(self):
		'''
		Show the current ZEC balance in the wallet

		Transparent and Shielded balances, along with the addresses they belong to are displayed
		'''

		balanceCommand = ('balance')
		return self.communicate(balanceCommand)


	def communicate(self , command):
		'''
		Send a custom command directly to zecwallet
		'''

		for i in range(3):
			self._sendCommand(command)
			commandResults = self._fetchResult()
			if (('error' in commandResults) and (commandResults['error'] == 'Wallet is locked')):
				self._unlockWallet()
			else:
				return commandResults


	def clear(self):
		'''
		Clear the wallet state, rolling back the wallet to an empty state.

		This command will clear all notes, utxos and transactions from the wallet, setting up the wallet to be synced from scratch.
		'''

		clearCommand = ('clear')
		return self.communicate(clearCommand)


	def decrypt(self):
		'''
		Completely remove wallet encryption, storing the wallet in plaintext on disk
		Note 1: This will decrypt the seed and the sapling and transparent private keys and store them on disk.
		Note 2: If you've forgotten the password, the only way to recover the wallet is to restore
		from the seed phrase.
		'''

		if (not(self._WALLET_DECRYPTION_KEY)):
			raise RuntimeError('A wallet decryption key must be provided in order to run this command.')

		decryptionCommand = ('decrypt ' + self._WALLET_DECRYPTION_KEY)
		results = self.communicate(decryptionCommand)
		if (results['result'] == 'success'):
			self._WALLET_DECRYPTION_KEY = ''
		return results


	def decryptMessage(self , encryptedMessageBase64):
		'''
		Attempt to decrypt a message with all the view keys in the wallet.
		'''
		decryptMessageCommand = ('decryptmessage ' + encryptedMessageBase64)
		return self.communicate(decryptMessageCommand)


	def defaultFee(self , blockHeight = ''):
		'''
		Returns the default fee in zats for outgoing transactions
		'''

		defaultFeeCommand = ('defaultfee ' + str(blockHeight))
		return self.communicate(defaultFeeCommand)


	def encrypt(self , WALLET_ENCRYPTION_KEY):
		'''
		Encrypt the wallet with a password
		Note 1: This will encrypt the seed and the sapling and transparent private keys.
		Use 'decrypt' to permanatly remove the encryption
		Note 2: If you forget the password, the only way to recover the wallet is to restore
		from the seed phrase.
		'''

		encryptionCommand = ('encrypt ' + WALLET_ENCRYPTION_KEY)
		results = self.communicate(encryptionCommand)
		if (results['result'] == 'success'):
			self._WALLET_DECRYPTION_KEY = WALLET_ENCRYPTION_KEY
		return results


	def encryptionStatus(self):
		'''
		Check if the wallet is encrypted and if it is locked
		'''

		encryptionStatusCommand = ('export')
		return self.communicate(encryptionStatusCommand)


	def encryptMessage(self , address , memo):
		'''
		Encrypt a memo to be sent to a z-address offline

		NOTE: This command only returns the encrypted payload. It does not broadcast it. You are expected to send the encrypted payload to the recipient offline
		'''

		encryptMessageCommand = ('encryptmessage ' + address + ' "' + memo + '"')
		return self.communicate(encryptMessageCommand)


	def export(self):
		'''
		Export private key for an individual wallet addresses.
		Note: To backup the whole wallet, use the 'seed' command insted
		'''

		exportCommand = ('export')
		return self.communicate(exportCommand)


	def getOption(self , optionName):
		'''
		Get a wallet option
		'''

		getOptionCommand = ('getoption ' + optionName)
		return self.communicate(getOptionCommand)


	def height(self):
		'''
		Get the latest block height that the wallet is at.
		'''

		heightCommand = ('height')
		return self.communicate(heightCommand)


	def importKey(self , spendingOrViewingKey , birthday , noRescan = False):
		'''
		Import an external spending or viewing key into the wallet

		Birthday is the earliest block number that has transactions belonging to the imported key. Rescanning will start from this block. If not sure, you can specify '0', which will start rescanning from the first sapling block.
		Note that you can import only the full spending (private) key or the full viewing key.
		'''

		if (noRescan):
			importCommand = ('import ' + spendingOrViewingKey + ' ' + str(birthday) + ' norescan')
		else:
			importCommand = ('import ' + spendingOrViewingKey + ' ' + str(birthday))
		return self.communicate(importCommand)



	def info(self):
		'''
		Get info about the lightwalletd we're connected to
		'''

		infoCommand = ('info')
		return self.communicate(infoCommand)


	def lastTXID(self):
		'''
		Show the latest TxId in the wallet
		'''

		txidCommand = 'lasttxid'
		return self.communicate(txidCommand)


	def list(self , allMemos = False):
		'''
		List all incoming and outgoing transactions from this wallet

		If you include the 'allmemos' argument, all memos are returned in their raw hex format
		'''

		if (allMemos):
			listCommand = ('list allmemos')
		else:
			listCommand = ('list')
		return self.communicate(listCommand)


	def newShieldedAddress(self):
		'''
		Create a new shielded address in this wallet
		'''

		newZCommand = ('new z')
		return self.communicate(newZCommand)


	def newTransparentAddress(self):
		'''
		Create a new transparent address in this wallet
		'''

		newTCommand = ('new t')
		return self.communicate(newTCommand)


	def notes(self , all = False):
		'''
		Show all sapling notes and utxos in this wallet

		If you supply the "all = True" argument, all previously spent sapling notes and spent utxos are also included
		'''

		if (all):
			notesCommand = ('notes all')
		else:
			notesCommand = ('notes')
		return self.communicate(notesCommand)


	def rescan(self):
		'''
		Rescan the wallet, rescanning all blocks for new transactions

		This command will download all blocks since the intial block again from the light client server
		and attempt to scan each block for transactions belonging to the wallet.
		'''

		rescanCommand = ('rescan')
		return self.communicate(rescanCommand)


	def save(self):
		'''
		Save the wallet to disk

		The wallet is saved to disk. The wallet is periodically saved to disk (and also saved upon exit)
		but you can use this command to explicitly save it to disk
		'''

		saveCommand = ('save')
		return self.communicate(saveCommand)


	def seed(self):
		'''
		Show the wallet's seed phrase

		Your wallet is entirely recoverable from the seed phrase. Please save it carefully and don't share it with anyone
		'''

		seedCommand = ('seed')
		return self.communicate(seedCommand)


	def send(self , destinationAddress , amountInZatoshis , memo = ''):
		'''
		Send ZEC to a given address(es)

		NOTE: The fee required to send this transaction is additionally deducted from your balance.
		'''

		sendCommand = ('send ' + destinationAddress + ' ' + str(amountInZatoshis) + ' "' + memo + '"')
		return self.communicate(sendCommand)


	def sendProgress(self):
		'''
		Get the progress of any send transactions that are currently computing
		'''

		sendProgressCommand = ('sendprogress')
		return self.communicate(sendProgressCommand)


	def setOption(self , optionName , optionValue):
		'''
		Set a wallet option

		List of available options:
		download_memos : none | wallet | all
		'''

		setOptionCommand = ('setoption ' + optionName + '=' + optionValue)
		return self.communicate(setOptionCommand)


	def shield(self , optionalAddress = ''):
		'''
		Shield all your transparent funds

		NOTE: The fee required to send this transaction is additionally deducted from your balance.
		'''

		shieldCommand = ('shield ' + optionalAddress)
		return self.communicate(shieldCommand)


	def sync(self):
		'''
		Sync the light client with the server
		'''

		syncCommand = ('sync')
		return self.communicate(syncCommand)


	def syncStatus(self):
		'''
		Get the sync status of the wallet
		'''

		syncStatusCommand = ('syncstatus')
		return self.communicate(syncStatusCommand)


	def quit(self):
		'''
		Save the wallet to disk and quit

		Destroys the wallet instance
		'''

		self.__del__()


	def zecPrice(self):
		'''
		Get the latest ZEC price in the wallet's currency (USD)
		'''

		priceCommand = ('zecprice')
		return self.communicate(priceCommand)


	def _fetchResult(self):
		rawOutput = self._readOutput()
		loadableOutput = ''

		jsonStarted = False
		for line in rawOutput.split('\n'):
			if (line):
				if ((line[0] == '{') or (line[0] == '[')):
					jsonStarted = True
				if (jsonStarted):
					loadableOutput += (line + '\n')
					if ((line[0] == '}') or (line[0] == ']')):
						break

		return loads(loadableOutput , parse_float = Decimal , parse_int = Decimal)


	def _readOutput(self):
		output = ''
		while (True):
			outputLine = self._sp.stdout.readline().decode()
			output += outputLine
			if ((not(outputLine)) or (outputLine[0] == '}') or (outputLine[0] == ']') or (outputLine[0:2] == '[]')):
				return output


	def _sendCommand(self , command):
		command = (command.encode('utf-8') + b'\n')
		self._sp.stdin.write(command)
		self._sp.stdin.flush()


	def _unlockWallet(self):
		if (not(self._WALLET_DECRYPTION_KEY)):
			raise RuntimeError('A wallet decryption key must be provided in order to run this command.')

		unlockCommand = ('unlock ' + self._WALLET_DECRYPTION_KEY)
		self._sendCommand(unlockCommand)
		if (self._fetchResult()['result'] == 'error'):
			raise RuntimeError('Wallet decryption failed. Please double check the decryption key provided.')
