from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from merchant_api.settings import NETWORK_SETTINGS
from merchant_api.consts import DECIMALS


class DucatuscoreInterface:

    endpoint = None
    settings = None

    def __init__(self):

        self.settings = NETWORK_SETTINGS['DUC']
        self.setup_endpoint()
        self.rpc = AuthServiceProxy(self.endpoint)
        self.check_connection()

    def setup_endpoint(self):
        self.endpoint = 'http://{user}:{pwd}@{host}:{port}'.format(
            user=self.settings['user'],
            pwd=self.settings['password'],
            host=self.settings['host'],
            port=self.settings['port']
        )
        return

    def check_connection(self):
        block = self.rpc.getblockcount()
        if block and block > 0:
            return True
        else:
            raise Exception('Ducatus node not connected')

    def transfer(self, prev_tx, address, amount, private_key):
        try:
            # value = amount / DECIMALS['DUC']
            # print('try sending {value} DUC to {addr}'.format(value=value, addr=address))
            # self.rpc.walletpassphrase(self.settings['wallet_password'], 30)
            # res = self.rpc.sendtoaddress(address, value)
            # print(res)
            # return res

            # prev_tx = listunspent()

            input_params = [{"txid": prev_tx, "vout": 0}]

            output_params = [{address: amount}]

            tx = self.rpc.createrawtransaction(input_params, output_params)

            signed = self.rpc.signrawtransactionwithkey(tx, [private_key])

            tx_hash = self.rpc.sendrawtransaction(signed['hex'])

            return tx_hash




        except JSONRPCException as e:
            print('DUCATUS TRANSFER ERROR: transfer for {amount} DUC for {addr} failed'
                  .format(amount=amount, addr=address), flush=True
                  )
            print(e, flush=True)