import binascii
import base58
import json

class Serializer:

    def __init__(self, Trans):
        vrt = (int(Trans.param['vertion'])).to_bytes(4, 'little')
        in_count = self.makeVar(Trans.param['tx_in count'])
        out_count = self.makeVar(Trans.param['tx_out count'])
        lkt = (int(Trans.param['lock_time'])).to_bytes(4, 'little').hex()
        self.param = {
            'vertion': vrt.hex(),
            'input count': in_count,
            'input': self.serialize_input(Trans.param['tx_in']),
            'output count': out_count,
            'output': self.serialize_output(Trans.param['tx_out']),
            'lockTime': lkt
        }

    def serialize_input(self, tx_in):
        in_rt = list()
        for i in range(len(tx_in)):
            str = (binascii.unhexlify(tx_in[i]['Previous txid'])[::-1].hex() +
                (int(tx_in[i]['Previous Tx Index']).to_bytes(4, 'little')).hex() +
                self.makeVar(tx_in[i]['Script Length']) +
                tx_in[i]['Signature Script'] + tx_in[i]['Sequence'])
            in_rt.append(str)
        return in_rt

    def serialize_output(self, tx_out):
        out = list()
        for i in range(len(tx_out)):
            str = ((int(tx_out[i]['value'])).to_bytes(8, 'little').hex() +
            (self.makeVar(tx_out[i]['Script Length'])) + tx_out[i]['Public Script'])
            out.append(str)
        return out


    def make(self):
        inp = ""
        out = ""
        for i in range(len(self.param['input'])):
            inp = inp + self.param['input'][i]
        for i in range(len(self.param['output'])):
            out = out + self.param['output'][i]
        str = (self.param['vertion'] + self.param['input count'] +
                inp + self.param['output count'] + out)
        return str

    def makeVar(self, strval):
        tmp = int(strval)
        if (tmp <= 255):
            bt = 1
            prf = ""
        elif tmp <= 65535:
            bt = 2
            prf = 'fd'
        elif tmp <= 4294967295:
            bt = 4
            prf = 'fe'
        else:
            bt = 8
            prf = 'ff'
        res = (int(strval)).to_bytes(bt, 'big')
        final = prf + res.hex()
        return final

class Deserializer:

    def __init__(self, str):
        inputCounterVal, inputCounterEnd = Deserializer.getVar(str[8:], 8)
        ilen, inp = self.getInput(inputCounterVal, str[inputCounterEnd:])

        outputCounterVal, outputCounterEnd = Deserializer.getVar(str[inputCounterEnd + ilen:], inputCounterEnd + ilen)
        olen, out = self.getOut(outputCounterVal, str[outputCounterEnd:])
        self.param = {
            'Vertion': str[0 : 8],
            'Input Count': inputCounterVal,
            'Inputs': inp,
            'Output Count': outputCounterVal,
            'Outputs': out,
            'Locktime': str[-8 : ]
        }

    @staticmethod
    def getVar(str, start):
        if str[:2] == 'fd':
            end = start + 6
            val = int(str[2: 6], 16)
        elif str[:2] == 'fe':
            end = start + 8
            val = int(str[2: 10], 16)
        elif str[:2] == 'ff':
            end = start + 16
            val = int(str[2: 18], 16)
        else:
            end = start + 2
            val = int(str[:2], 16)
        return val, end

    def getInput(self, len, str):
        inp = list()
        txid = 64
        vout = 8
        seqence = 8
        round = 0
        for i in range(len):
            scr_len, endScriptvar = Deserializer.getVar(str[(txid + vout) + round:], (txid + vout) + round)
            bytesScriptvar = endScriptvar - (txid + vout + round)
            inp.append({
                'TXID': str[:round + txid],
                'VOUT': str[round + txid: round + txid + vout],
                'ScriptSig Size': scr_len,
                'ScriptSig': str[round + txid + vout + bytesScriptvar: round + txid + vout + bytesScriptvar + scr_len * 2],
                'Sequence': str[round + txid + vout + bytesScriptvar + scr_len * 2: round + txid + vout + bytesScriptvar + scr_len * 2 + seqence]
            })
            round = round + txid + vout + bytesScriptvar + scr_len * 2 + seqence
        return round, inp

    def getOut(self, len, str):
        out = list()
        value = 16
        round = 0
        for i in range(len):
            scr_len, endScriptvar = Deserializer.getVar(str[value + round:], value + round)
            bytesScriptvar = endScriptvar - (value + round)
            out.append({
                'Value': str[:round + value],
                'ScriptPubKey Size': scr_len,
                'ScriptPubKey': str[round + value + bytesScriptvar: round + value + bytesScriptvar + scr_len * 2]
            })
            round = round + value + bytesScriptvar + scr_len * 2
        return round, out

    def make(self):
        self.param['Vertion'] = (binascii.unhexlify(self.param['Vertion'])[::-1]).hex()
        for i in range(len(self.param['Inputs'])):
            self.param['Inputs'][i]['TXID'] = (binascii.unhexlify(self.param['Inputs'][i]['TXID'])[::-1]).hex()
            self.param['Inputs'][i]['VOUT'] = (binascii.unhexlify(self.param['Inputs'][i]['VOUT'])[::-1]).hex()
        for i in range(len(self.param['Outputs'])):
            self.param['Outputs'][i]['Value'] = (binascii.unhexlify(self.param['Outputs'][i]['Value'])[::-1]).hex()

    def toJSON(self):
        return json.dumps(self.param, default=lambda o: o.__dict__,
            sort_keys=True, indent=6)
