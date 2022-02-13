#!/usr/bin/python3
import requests
import re
import json
from web3 import Web3
import time
from datetime import datetime
import key
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument("-g", "--g")
parser.add_argument("-n", "--n")
args = parser.parse_args()

bsc = key.rpc
web3 = Web3(Web3.HTTPProvider(bsc))

#shitcoin
print(key.CVIOLET +'###########################################################'+key.RESET)
print(key.CRED +'Enter Contract Address:'+key.RESET)
token = input().lower()
#replacestring
rstring = token.replace('zero', '0').replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4').replace('five', '5').replace('six', '6').replace('seven', '7').replace('eight', '8').replace('nine', '9').replace('ten', '10').replace('eleven', '11').replace('twelve', '12').replace('thirteen', '13').replace('fourteen', '14').replace('fifteen', '15').replace('sixteen', '16').replace('seventeen', '17').replace('eighteen', '18').replace('nineteen', '19').replace('twenty', '20').replace('remove', '').replace('delete', '').replace('beginning', '').replace('middle', '').replace('end', '').replace('first', '').replace('second', '').replace('third', '').replace('space', '')

#replace karakter
rcharact = re.sub(r'[^a-zA-Z0-9]','',rstring)
shit = web3.toChecksumAddress(rcharact)

#print(shit)
#asu = input()

#PancakeFactory
pancake_factory = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'
pancake_factory_abi = key.pancake_factory_abi
fcontract = web3.eth.contract(address=pancake_factory, abi=pancake_factory_abi)

#WBNBFactory
wbnb = web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
wbnb_abi = key.wbnb_abi
lp = web3.eth.contract(address=wbnb, abi=wbnb_abi)

#Pancakeswap Router
pancake_router = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
pancake_router_abi = key.pancake_router_abi
prouter = web3.eth.contract(address=pancake_router, abi=pancake_router_abi)

#sellcontract
sell_router = web3.toChecksumAddress(shit)
sell_router_abi = key.sellAbi
selltcontract = web3.eth.contract(sell_router, abi=sell_router_abi)

#buytoken

nonce = web3.eth.get_transaction_count(key.account)
start = time.time()

#gwei and amount of token setup

gwei1 = key.gwei1
gwei2 = args.g
if gwei2 == None:
	gwei = gwei1
else:
	gwei = gwei2

#amountbuy######

nom1 = key.nonimal1
nom2 = args.n
if nom2 == None:
	nominal = nom1
else: 
	nominal = nom2
#Buying
print(key.CVIOLET +'Buying Token'+key.RESET)

pancakeswap2_txn = prouter.functions.swapExactETHForTokens(
0, # set to 0, or specify minimum amount of tokeny you want to receive - consider decimals!!!
[wbnb,shit],
key.account,
(int(time.time()) + 10000)
).buildTransaction({
'from': key.account,
'value': web3.toWei((nominal),'ether'),#This is the Token(BNB) amount you want to Swap from
'gas': 2000000,
'gasPrice': web3.toWei((gwei),'gwei'),
'nonce': nonce,
})
signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=key.private)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
rs = (web3.toHex(tx_token))

#checking transaction status
print(key.CYELLOW +'https://bscscan.com/tx/'+rs+key.RESET)
print(key.CBLUE +'Checking Transaction Status'+key.RESET)
resi = web3.eth.wait_for_transaction_receipt(rs)
block = resi['status']
if block == 1:
    print(key.CGREEN+'Transaction Succesfull'+key.RESET)
if block == 0:
    print(key.CRED+'Transaction Failed'+key.RESET)
    sys.exit()
print(key.CBLUE +'---------------------------------'+key.RESET)
print(key.CYELLOW +'Approving Token'+key.RESET)
#TokenInfo 
balance = selltcontract.functions.balanceOf(key.account).call()
symbol = selltcontract.functions.symbol().call()
readable = web3.fromWei(balance,'ether')
tokenValue = balance

#Approve Token before Selling
start = (int(time.time()) + 10000)
approve = selltcontract.functions.approve(pancake_router, 115792089237316195423570985008687907853269984665640564039457584007913129639935).buildTransaction({
            'from': key.account,
            'gasPrice': web3.toWei('5','gwei'),
            'nonce': web3.eth.get_transaction_count(key.account),
            })

signed_txn = web3.eth.account.sign_transaction(approve, private_key=key.private)
tx_token2 = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
#preparing
ar = (web3.toHex(tx_token2))
aresi = web3.eth.wait_for_transaction_receipt(ar)
apr = aresi['status']
if apr == 1:
    print(key.CGREEN+'Approved'+key.RESET)
if apr == 0:
    print(key.CRED+'Failed'+key.RESET)
    sys.exit()
#check profit    
cont = print(key.CYELLOW+'Checking Profit!'+key.RESET)

try:
    while True:
        check = prouter.functions.getAmountsOut(int(balance),[shit, wbnb]).call()
        rbnb = web3.fromWei(check[1],'ether')
        print (key.CYELLOW+'Your Profit: '+key.RESET+key.CGREEN+str(rbnb)+' BNB'+key.RESET)
        time.sleep(1)
except KeyboardInterrupt:
        pass
print(key.CBLUE+'Swapping Token.........'+key.RESET)
#selltoken
pancakeswap2_txn = prouter.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            int(tokenValue),0,
            [shit, wbnb],
            key.account,
            (int(time.time()) + 1000000)

            ).buildTransaction({
            'from': key.account,
			'gas': 2000000,
            'gasPrice': web3.toWei('6','gwei'),
            'nonce': web3.eth.get_transaction_count(key.account),
            })
    
signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=key.private)
tx_token3 = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

jt = (web3.toHex(tx_token3))
jresi = web3.eth.wait_for_transaction_receipt(jt)
jpr = jresi['status']
if jpr == 1:
	print(key.CGREEN+'Success'+key.RESET)
if jpr == 0:
	print(key.CRED+'Failed'+key.RESET)
print(key.CGREEN+'https://bscscan.com/tx/'+jt+key.RESET)
print(key.CBLUE +'---------------------------------'+key.RESET)
mbal = web3.eth.get_balance(key.account)
rmbal = web3.fromWei(mbal,'ether')
print('Balance :'+str(rmbal)+key.CYELLOW +' BNB'+key.RESET)
print(key.CGREEN +'---------------------------------'+key.RESET)