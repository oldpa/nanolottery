from util import RPC
import os
import time
import json
import to_mongo

ping_wallet = os.environ["PINGWALLET"]
ping_account = os.environ["PINGACCOUNT"]

def main():
    rpc = RPC()
    while True:
        try:
            history = rpc.account_history(ping_account)
            to_mongo.refresh_blocks(history['history'])
            received = []
            sent = []
            # Get account history and split into sent and received
            # Iterate from oldest to newest transactions
            for row in history['history'][::-1]:
                if row['type'] == 'receive':
                    received.append((row['account'], row['amount'], row['hash']))
                if row['type'] == 'send':
                    sent.append((row['account'], row['amount']))

            print 'History'
            print json.dumps(history, sort_keys=True, indent=4, separators=(',', ': '))

            # Filter out received transactions without matching sent
            for send in sent:
                for i in xrange(len(received)):
                    if send[:2] == received[i][:2]:
                        del received[i]
                        break


            print 'To send to'
            print json.dumps(received, sort_keys=True, indent=4, separators=(',', ': '))
            # Send transactions
            for rec in received:
                destination, amount, transaction_id = rec
                print transaction_id
                print rpc.send(ping_wallet, ping_account, destination, amount, transaction_id)
            history = rpc.account_history(ping_account)
            to_mongo.refresh_blocks(history['history'])
            time.sleep(1)
        except Exception as e: print(e)


if __name__ == "__main__":
    main()

