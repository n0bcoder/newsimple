#!/usr/bin/python3
from txns import TXN
import argparse, sys, json
import time
from web3 import Web3
import key
import re
import keyboard

bsc = key.wss
web3 = Web3(Web3.WebsocketProvider(bsc))

parser = argparse.ArgumentParser()
parser.add_argument('-hp', '--hp', action="store_true", help="Honeypot Checker, -hp to activate honeypot checker")
parser.add_argument('-sw', '--sw', action="store_true", help="Trade Check, -sw to Disable")
parser.add_argument("-t", "--t", action="store_true", help="Help you to Calculate Time")#calculatetime
parser.add_argument("-tx", "--tx", action="store_true", help="Check Tax, -tx to disable tax checker")#check Tax
parser.add_argument("-c", "--c", action="store_true", help="Check Mode, to check tax etc")#check Mode
parser.add_argument("-sl", "--sl", action="store_true", help="sell only")#check Mode
parser.add_argument("-n", "--n", help="amount of BNB you want to spend, default is 0.01")#nominal
parser.add_argument("-d", "--d", help="To skip certain block, in order to use this you must use high gas")#deadblock
parser.add_argument("-g", "--g", help="you can use this to change default gwei setting, default gwei is 20")#gwei
parser.add_argument("-gs", "--gs", help="costum gwei for sell ")#gweisell
args = parser.parse_args()


#PancakeFactory
pancake_factory = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'
pancake_factory_abi = key.pancake_factory_abi
fcontract = web3.eth.contract(address=pancake_factory, abi=pancake_factory_abi)

#WBNBFactory
wbnb = web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
wbnb_abi = key.wbnb_abi
wcontract = web3.eth.contract(address=wbnb, abi=wbnb_abi)

#Pancakeswap Router
pancake_router = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
pancake_router_abi = key.pancake_router_abi
prouter = web3.eth.contract(address=pancake_router, abi=pancake_router_abi)




class SniperBot():

    def __init__(self):
        self.parseArgs()
        
    
    def SayWelcome(self):
        print("---------------------------------")
        print(key.CYELLOW+"Amount :"+key.RESET+'\n'+ str(self.amount) + " BNB")
        print(key.CYELLOW+"Contract Address :"+key.RESET+'\n'+str(self.token))
        
    def parseArgs(self):
        print(key.CRED+"Enter Contract Address :"+key.RESET)
        ca = input().lower()
        token = ca
        #replacestring
        rstring = token.replace('zero', '0').replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4').replace('five', '5').replace('six', '6').replace('seven', '7').replace('eight', '8').replace('nine', '9').replace('ten', '10').replace('eleven', '11').replace('twelve', '12').replace('thirteen', '13').replace('fourteen', '14').replace('fifteen', '15').replace('sixteen', '16').replace('seventeen', '17').replace('eighteen', '18').replace('nineteen', '19').replace('twenty', '20').replace('remove', '').replace('delete', '').replace('beginning', '').replace('middle', '').replace('end', '').replace('first', '').replace('second', '').replace('third', '').replace('space', '')

        #replace karakter
        rcharact = re.sub(r'[^a-zA-Z0-9]','',rstring)
        shit = web3.toChecksumAddress(rcharact)
        self.token = web3.toChecksumAddress(shit)
        #amount
        nom1 = key.nonimal1
        nom2 = args.n
        if nom2 == None:
            nominal = nom1
        else: 
            nominal = nom2
        token = nominal
        self.amount = token    
        #self.tx = args.txamount
        self.amountForSnipe = float(self.amount)
        self.hp = args.hp


    def paircheck(self):
        #Pair checker
        pancake_factory = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'
        pancake_factory_abi = key.pancake_factory_abi
        fcontract = web3.eth.contract(address=pancake_factory, abi=pancake_factory_abi)
        token1 = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
        token2 = web3.toChecksumAddress(self.token)
        none = '0x0000000000000000000000000000000000000000'
        pair = fcontract.functions.getPair(token1,token2).call()
        if pair == none:
            print(key.CBLUE + 'Cheking Pair Please Wait.....'+key.RESET+'\n'+key.CGREEN + 'Pair Not Detected '+'\n'+key.RESET+key.CVIOLET+'Waiting Pairs !'+key.RESET)
            while True:
                pair = fcontract.functions.getPair(token1,token2).call()
                time.sleep(0.3)
                if pair != none:
                    break
        print(key.CGREEN + 'Pair Detected at block '+key.RESET+key.CBLUE+str(web3.eth.blockNumber)+key.RESET+'\n'+key.CRED + pair + key.RESET+'\n'+ key.CYELLOW+'Checking Liquidity !'+key.RESET)
        #WBNBFactory
        wbnb = web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
        wbnb_abi = key.wbnb_abi
        wcontract = web3.eth.contract(address=wbnb, abi=wbnb_abi)
        #LPchecker
        simbol = wcontract.functions.symbol().call()
        cek = wcontract.functions.balanceOf(pair).call()
        totallp = web3.fromWei(cek,'ether')
        if totallp < 0.5:
            print(key.CRED + 'Liquadity Not Detected '+'\n'+key.RESET+key.CVIOLET+'Waiting Dev Add The Liquadity !'+key.RESET)
            while True:
                pair = fcontract.functions.getPair(token1,token2).call()
                cek = wcontract.functions.balanceOf(pair).call()
                totallp = web3.fromWei(cek,'ether')
                time.sleep(0.3)
                if totallp > 0.5:
                    break
        print(key.CGREEN + 'Liquadity is Detected '+'\n'+key.RESET+str(totallp) +key.CYELLOW+' '+simbol+key.RESET+'\n'+key.CRED+'Checking Trade Status !'+key.RESET)

    def awaitEnabledBuy(self):
        while True:
            try:
                if self.TXN.checkifTokenBuyDisabled() == True:
                    break
            except Exception as e:
                if "UPDATE" in str(e):
                    print(e)
                    sys.exit()
                continue
        print(key.CGREEN+'Trade is Enabled'+key.RESET)
    
    def maketx(self):

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
        #buytoken

        nonce = web3.eth.get_transaction_count(key.account)
        start = time.time()
        pancakeswap2_txn = prouter.functions.swapExactETHForTokens(
        0, # set to 0, or specify minimum amount of tokeny you want to receive - consider decimals!!!
        [wbnb, self.token],
        key.account,
        (int(time.time()) + 10000)
        ).buildTransaction({
        'from': key.account,
        'value': web3.toWei((nominal),'ether'),#This is the Token(BNB) amount you want to Swap from
        'gas': 5000000,
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
    
    def selltx(self):

        #sellcontract
        sell_router = web3.toChecksumAddress(self.token)
        sell_router_abi = key.sellAbi
        selltcontract = web3.eth.contract(sell_router, abi=sell_router_abi)
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
                check = prouter.functions.getAmountsOut(int(balance),[self.token, wbnb]).call()
                rbnb = web3.fromWei(check[1],'ether')
                print (key.CYELLOW+'Your Profit: '+key.RESET+key.CGREEN+str(rbnb)+' BNB'+key.RESET)
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        print(key.CBLUE+'Swapping Token.........'+key.RESET)
        #gwei for sell
        gweis1 = key.gsell
        gweis2 = args.gs
        if gweis2 == None:
            gweis = gweis1
        else:
            gweis = gweis2

        #selltoken
        pancakeswap2_txn = prouter.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
                int(tokenValue),0,
                [self.token, wbnb],
                key.account,
                (int(time.time()) + 1000000)

                ).buildTransaction({
                'from': key.account,
                'gas': 3000000,
                'gasPrice': web3.toWei((gweis),'gwei'),
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

    def selltxonly(self):

        #sellcontract
        sell_router = web3.toChecksumAddress(self.token)
        sell_router_abi = key.sellAbi
        selltcontract = web3.eth.contract(sell_router, abi=sell_router_abi)
        #TokenInfo 
        balance = selltcontract.functions.balanceOf(key.account).call()
        symbol = selltcontract.functions.symbol().call()
        readable = web3.fromWei(balance,'ether')
        tokenValue = balance

        #gwei for sell
        gweis1 = key.gsell
        gweis2 = args.gs
        if gweis2 == None:
            gweis = gweis1
        else:
            gweis = gweis2

        #selltoken
        pancakeswap2_txn = prouter.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
                int(tokenValue),0,
                [self.token, wbnb],
                key.account,
                (int(time.time()) + 1000000)

                ).buildTransaction({
                'from': key.account,
                'gas': 3000000,
                'gasPrice': web3.toWei((gweis),'gwei'),
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

    #everythingrunfromhere
    def StartUP(self):
        self.TXN = TXN(self.token, self.amountForSnipe)
        #time
        start = time.time()
        #maketx and sell
        if args.sl == False:
            #welcome
            self.SayWelcome()
            #pairandLPcheck
            self.paircheck()       
            #tradecheck
            if args.sw == False:
                self.awaitEnabledBuy()
            #deadblock
            block = web3.eth.blockNumber
            dead1 = key.dead1
            dead2 = args.d
            if dead2 != None and (int(dead2) > int(0)):
                rdead = block+int(dead2)
                dead = rdead
                print(key.CGREEN+'Current block :'+str(block)+key.RESET+'\n'+key.CRED+'Skiping '+dead2+' block'+key.RESET+'\n'+key.CVIOLET+'Buying at block :'+str(rdead)+key.RESET)
                fdead = dead-int(1)
                while True:
                    block = web3.eth.blockNumber
                    if block == fdead:
                        break
            #honeychecktax
            honeyTax = self.TXN.checkToken()
            if args.tx == False:
                print('Buy Tax : '+key.CRED+str(honeyTax[0])+'%  '+key.RESET+'Sell Tax : '+key.CRED+str(honeyTax[1])+'%'+key.RESET)
                if honeyTax[0] > key.buytax:
                    print('Waiting Tax Low '+str(honeyTax[0])+'%')
                    while True:
                        honeyTax = self.TXN.checkToken()
                        time.sleep(0.07)
                        if honeyTax[0] < key.buytax:
                            break
            if self.hp == True:
                print(key.CRED +"Checking Honeypot..."+key.RESET)
                if honeyTax[2] == True:
                    print(key.CRED + 'Honeypot! bye-bye '+key.RESET)
                    sys.exit() 
                elif honeyTax[2] == False:
                    print(key.CGREEN + 'Not Honeypoot '+key.RESET)
            
            #endcalculatetime
            end = time.time()
            if args.t == True:
                print(end-start, 'Seconds')

            #checkmode
            if args.c == True:
                print('Check Mode !')
                sys.exit()

            #maketx and sell
            self.maketx()
            self.selltx()
            sys.exit()     
        #sellonly
        if args.sl == True:
            honeyTax = self.TXN.checkToken()
            if self.hp == True:
                print(key.CRED +"Checking Honeypot..."+key.RESET)
                while True:
                    time.sleep(0.07)
                    honeyTax = self.TXN.checkToken()
                    if honeyTax[2] == False:
                        print(key.CRED + 'Waiting .. '+key.RESET)
                        break
            elif honeyTax[2] == False:
                print(key.CGREEN + 'Not Honeypoot '+key.RESET)
            if honeyTax[1] > key.selltax:
                    print('Waiting Tax Low '+str(honeyTax[0])+'%')
                    while True:
                        honeyTax = self.TXN.checkToken()
                        time.sleep(0.07)
                        if honeyTax[1] < key.selltax:
                            break
            self.selltxonly()
            

SniperBot().StartUP()
