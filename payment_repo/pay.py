from web3 import Web3
import requests
import configparser
import datetime
import qrcode
import os
from dataclasses import dataclass
import concurrent.futures

# Set up web3 connection
config=configparser.ConfigParser()
config.read('config.ini')
web3 = Web3(Web3.HTTPProvider(config['infura']['api_url']))

@dataclass
class payments:

    def generate_qr_code(self,link):
        #os.makedirs('./qrcode',exist_ok=True)
        file_time=datetime.datetime.now().strftime('%H_%M_%S')
        filename='qr_code'+file_time+'.png'
        

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save(os.path.join('./static/'+filename))
        return filename,file_time


    def merchant_inputs(self,usd_value, merchant_wallet_address,payment_assest):
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

        response = requests.get(url)
        data = response.json()

        eth_price = data['ethereum']['usd']
        
        usdc_price = 1  # 1 USDC is equal to 1 USD

        # Calculate equivalent amounts
        eth_amount = usd_value / eth_price
        usdc_amount = usd_value / usdc_price

        # Create the payment string
        eth_payment_string = f"ethereum:{merchant_wallet_address}?amount={eth_amount}"
        usdc_payment_string = f"usdc:{merchant_wallet_address}?amount={usdc_amount}"
        
        if payment_assest=='usdc':
            return usdc_payment_string
        else:
            return eth_payment_string

    

    def get_transaction_status(self,tx_hash,wallet_address):

        transaction = web3.eth.get_transaction(tx_hash)
        

        if transaction is None:
            return "Transaction not found"

        if transaction.blockNumber is None:
            return "Transaction is still pending"

        transaction_receipt = web3.eth.get_transaction_receipt(tx_hash)

        if transaction_receipt.status == 0:
            return "Transaction failed"
        elif transaction['to']==wallet_address or transaction['from']==wallet_address:
            return "Transaction succeeded"
        
        

    

    def auto_payment(self,wallet_address):
        found_transactions = []

        def process_transaction(tx_hash):
            tx = web3.eth.get_transaction(tx_hash)
            if tx['to'] == wallet_address:
                print(tx)
                found_transactions.append((tx['hash'], tx['from'], tx['to']))

        block = web3.eth.get_block('latest')
        transactions = block.transactions

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_results = [executor.submit(process_transaction, tx) for tx in transactions]

        # Get results from completed futures
        for future in concurrent.futures.as_completed(future_results):
            result = future.result()
            if result:
                found_transactions.append(result)

        return found_transactions

        # result = auto_payment()

        # # Print the found transactions
        # for tx in result:
        #     print(f"Transaction Hash: {tx[0]}")
        #     print(f"From: {tx[1]}")
        #     print(f"To: {tx[2]}")
        #     print()





