import requests
import json

class RPC(object):
    dry_run = False

    def __init__(self, dry_run=False):
        self.dry_run = dry_run

    def rpc_call(self, data):
        if self.dry_run:
            print 'Would have sent following data'
            print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
            return {}
        else:
            resp = requests.post('http://[::1]:7076', data=json.dumps(data))
            if resp.ok:
                resp_data = resp.json()
                if 'error' in resp_data:
                    print 'Error response when processing'
                    print json.dumps(resp_data, sort_keys=True, indent=4, separators=(',', ': '))
                    return {}
                return resp_data
            else:
                print 'Non OK response code'
                print 'Response' + resp.reason
                print resp.text
                return {}


    def account_history(self, account, count=20):
        data = \
        {
          "action": "account_history",
          "account": account,
          "count": count
        }
        return self.rpc_call(data)

    def account_create(self, wallet):
        data = \
        {
          "action": "account_create",
          "wallet": wallet
        }
        return self.rpc_call(data)

    def account_balance(self, account):
        data = \
        {
          "action": "account_balance",
          "account": account,
        }
        return self.rpc_call(data)
    def send(self, wallet, source, destination, amount, transaction_id):
        if not isinstance(amount, basestring):
            amount = json.dumps(amount)
        data = \
        {
            "action": "send",
            "wallet": wallet,
            "source": source,
            "destination": destination,
            "amount": amount,
            "id": transaction_id
        }
        return self.rpc_call(data)
    def custom_call(self, **kwargs):
        return self.rpc_call(kwargs)
