#!/usr/bin/python3
from web3 import Web3
import json, sys
import key




from decimal import * 
# More than 8 Decimals are not supportet in the input from the token buy amount! No impact to Token Decimals!
getcontext().prec = 8

class TXN():
    def __init__(self, token_address, quantity):
        self.w3 = self.connect()
        self.token_address = Web3.toChecksumAddress(token_address)
        self.token_contract = self.setup_token()
        self.swapper_address, self.swapper = self.setup_swapper()
        self.quantity = quantity 


    def connect(self):

        w3 = Web3(Web3.WebsocketProvider(key.wss))
        return w3


    def get_token_decimals(self):
        return self.token_contract.functions.decimals().call()



    def setup_swapper(self):
        #honeypot checker and tax
        swapper_address = Web3.toChecksumAddress("0x06Ebf173418591927E645937536eb54a6D4060Cc") 
        with open("./BSC_Swapper.json") as f:
            contract_abi = json.load(f)
        swapper = self.w3.eth.contract(address=swapper_address, abi=contract_abi)
        return swapper_address, swapper

    def setup_token(self):
        with open("./bep20_abi_token.json") as f:
            contract_abi = json.load(f)
        token_contract = self.w3.eth.contract(address=self.token_address, abi=contract_abi)
        return token_contract

    

    def checkToken(self):
        tokenInfos = self.swapper.functions.getTokenInformations(self.token_address).call()
        buy_tax = round((tokenInfos[0] - tokenInfos[1]) / tokenInfos[0] * 100) 
        sell_tax = round((tokenInfos[2] - tokenInfos[3]) / tokenInfos[2] * 100)
        if tokenInfos[5] and tokenInfos[6] == True:
            honeypot = False
        else:
            honeypot = True
        return buy_tax, sell_tax, honeypot
    

    def checkifTokenBuyDisabled(self):
        disabled = self.swapper.functions.getTokenInformations(self.token_address).call()[4] #True if Buy is enabled, False if Disabled.
        #todo: find a solution for bugged tokens that never can be buy.
        return disabled


 