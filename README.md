# Zecwallet-Python

###### A wrapper around Zecwallet Command Line LightClient, written in Python

------------

# Table of Contents

- [About](#about "About")
- [Installation](#installation "Installation")
- [Usage](#usage "Usage")
- [Examples](#examples "Examples")

# About

Zecwallet-Python is a simple wrapper around the Zecwallet Command Line LightClient written in Python, allowing Python programs to easily interact with a fully-capable, lightweight Zcash wallet. Using this package with Zecwallet, one can easily send and receive (shielded) transactions, encrypt and decrypt messages, fetch the current, market value of Zcash, and so much more. This package makes all of the Zecwallet functionality easily available in Python, and uses no dependencies outside of Zecwallet, and the Python Standard Library. Common use cases for this package include cryptocurrency trading bots, online payment processing for Zcash (including support for shielded transactions), and encrypted communication systems.

###### Please note that this project is independent from [Zecwallet](https://www.zecwallet.co/), and has not been audited for security and reliability. Use at your own risk.

# Installation

To use Zecwallet-Python, you will need to install [Zecwallet Command Line LightClient](https://github.com/adityapk00/zecwallet-light-cli/releases) first. You can do this by downloading their latest release, unzipping it, and then making note of the filepath to the `zecwallet-cli` executable on your system.

###### Note: The latest version of Zecwallet to be tested for full compatibility with Zecwallet-Python is v1.7.7

Example installation for most Linux distributions:

```bash
wget https://github.com/adityapk00/zecwallet-light-cli/releases/download/v1.7.7/linux-zecwallet-cli-v1.7.7.zip -O /tmp/zecwallet.zip
unzip /tmp/zecwallet.zip -d /home/ubuntu/ZcashWallet
```

Next, you will need to install Zecwallet-Python, which can by done using [pip](https://pypi.org/project/pip/):

```bash
pip3 install zecwallet
```

Alternatively, you may copy the `wallet.py` file from [our GitHub repository](https://github.com/P5vc/Zecwallet-Python/blob/main/zecwallet/wallet.py), and import that locally into your project.

# Usage

To interact with your Zcash wallet in Python, you must first import the Wallet class, then initialize it, providing the full filepath to the `zecwallet-cli` executable and your wallet decryption key. It is not required nor recommended to provide the wallet decryption key unless you need to take advantage of functionality that requires the key.

```python3
from zecwallet.wallet import Wallet
myWallet = Wallet('/path/to/zecwallet-cli' , 'MyDecryptionKey')
```

Once you've instantiated your wallet, you'll have access to all of the following functions. These functions accept (sometimes optional) arguments as indicated below, and return the same datatypes returned by the Zecwallet CLI (usually a dictionary or a list).

###### Note that, as a wrapper, the descriptions, functionality, and returned results are nearly identical to those provided by Zecwallet.

```
 |  addresses()
 |      List current addresses in the wallet
 |  
 |  balance()
 |      Show the current ZEC balance in the wallet
 |      
 |      Transparent and Shielded balances, along with the addresses they belong to are displayed
 |  
 |  clear()
 |      Clear the wallet state, rolling back the wallet to an empty state.
 |      
 |      This command will clear all notes, utxos and transactions from the wallet, setting up the wallet to be synced from scratch.
 |  
 |  communicate(command)
 |      Send a custom command directly to zecwallet
 |  
 |  decrypt()
 |      Completely remove wallet encryption, storing the wallet in plaintext on disk
 |      Note 1: This will decrypt the seed and the sapling and transparent private keys and store them on disk.
 |      Note 2: If you've forgotten the password, the only way to recover the wallet is to restore
 |      from the seed phrase.
 |  
 |  decryptMessage(encryptedMessageBase64)
 |      Attempt to decrypt a message with all the view keys in the wallet.
 |  
 |  defaultFee(blockHeight='')
 |      Returns the default fee in zats for outgoing transactions
 |  
 |  encrypt(WALLET_ENCRYPTION_KEY)
 |      Encrypt the wallet with a password
 |      Note 1: This will encrypt the seed and the sapling and transparent private keys.
 |      Use 'decrypt' to permanatly remove the encryption
 |      Note 2: If you forget the password, the only way to recover the wallet is to restore
 |      from the seed phrase.
 |  
 |  encryptMessage(address, memo)
 |      Encrypt a memo to be sent to a z-address offline
 |      
 |      NOTE: This command only returns the encrypted payload. It does not broadcast it. You are expected to send the encrypted payload to the recipient offline
 |  
 |  encryptionStatus()
 |      Check if the wallet is encrypted and if it is locked
 |  
 |  export()
 |      Export private key for an individual wallet addresses.
 |      Note: To backup the whole wallet, use the 'seed' command insted
 |  
 |  getOption(optionName)
 |      Get a wallet option
 |  
 |  height()
 |      Get the latest block height that the wallet is at.
 |  
 |  importKey(spendingOrViewingKey, birthday, noRescan=False)
 |      Import an external spending or viewing key into the wallet
 |      
 |      Birthday is the earliest block number that has transactions belonging to the imported key. Rescanning will start from this block. If not sure, you can specify '0', which will start rescanning from the first sapling block.
 |      Note that you can import only the full spending (private) key or the full viewing key.
 |  
 |  info()
 |      Get info about the lightwalletd we're connected to
 |  
 |  lastTXID()
 |      Show the latest TxId in the wallet
 |  
 |  list(allMemos=False)
 |      List all incoming and outgoing transactions from this wallet
 |      
 |      If you include the 'allmemos' argument, all memos are returned in their raw hex format
 |  
 |  newShieldedAddress()
 |      Create a new shielded address in this wallet
 |  
 |  newTransparentAddress()
 |      Create a new transparent address in this wallet
 |  
 |  notes(all=False)
 |      Show all sapling notes and utxos in this wallet
 |      
 |      If you supply the "all = True" argument, all previously spent sapling notes and spent utxos are also included
 |  
 |  quit()
 |      Save the wallet to disk and quit
 |      
 |      Destroys the wallet instance
 |  
 |  rescan()
 |      Rescan the wallet, rescanning all blocks for new transactions
 |      
 |      This command will download all blocks since the intial block again from the light client server
 |      and attempt to scan each block for transactions belonging to the wallet.
 |  
 |  save()
 |      Save the wallet to disk
 |      
 |      The wallet is saved to disk. The wallet is periodically saved to disk (and also saved upon exit)
 |      but you can use this command to explicitly save it to disk
 |  
 |  seed()
 |      Show the wallet's seed phrase
 |      
 |      Your wallet is entirely recoverable from the seed phrase. Please save it carefully and don't share it with anyone
 |  
 |  send(destinationAddress, amountInZatoshis, memo='')
 |      Send ZEC to a given address(es)
 |      
 |      NOTE: The fee required to send this transaction is additionally deducted from your balance.
 |  
 |  sendProgress()
 |      Get the progress of any send transactions that are currently computing
 |  
 |  setOption(optionName, optionValue)
 |      Set a wallet option
 |      
 |      List of available options:
 |      download_memos : none | wallet | all
 |  
 |  shield(optionalAddress='')
 |      Shield all your transparent funds
 |      
 |      NOTE: The fee required to send this transaction is additionally deducted from your balance.
 |  
 |  sync()
 |      Sync the light client with the server
 |  
 |  syncStatus()
 |      Get the sync status of the wallet
 |  
 |  zecPrice()
 |      Get the latest ZEC price in the wallet's currency (USD)
```

# Examples

```python3
>>> from zecwallet.wallet import Wallet
>>> myWallet = Wallet('/home/ubuntu/ZcashWallet/zecwallet-cli' , 'decryptionKey')
>>> myWallet.zecPrice()
{'zec_price': Decimal('93.12'), 'fetched_at': Decimal('1654321098'), 'currency': 'USD'}
>>> myWallet.newShieldedAddress()
['zs1tnk62y6sn4mwrwyxrhjxjth6lzlsaggmnkEXAMPLEwsftk760yxrsme44kp997eps0w6z4g7vd9']
>>> myWallet.save()
{'result': 'success'}
>>> myWallet.encryptMessage('zs1d0fx24crh2kuyqs7yp0jf4wswyuEXAMPLE8mgejmf7qev2jnhjhwevhvzgjczcjzptl9xsace80' , 'Hello World!')
{'encrypted_base64': 'WmNhc2hPZmZsaW5lTWVtSHORTENEDEXAMPLEUi0JRXAleZ4ep2yg=='}
>>> myWallet.send('zs1d0fx24crh2kuyqs7yp0jf4wswyuEXAMPLE8mgejmf7qev2jnhjhwevhvzgjczcjzptl9xsace80' , 123456 , 'Paying you back for coffee. Thanks again!')
{'result': 'success'}
```
