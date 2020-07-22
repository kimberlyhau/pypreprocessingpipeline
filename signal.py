import pandas as pd
from scipy import signal
class Signal:
    def __init__(self, ts, val):
        self.ts = ts
        self.val = val

class CSVSignal:
    def __init__(self, filenames, batchsize = 10):
        self.batchsize = batchsize
        self.df = pd.DataFrame()
        #self.df=pd.read_csv(filenames[0], names = ["ts", "val"])
        #self.df = self.df.append(pd.read_csv(filenames[1], names = ["ts", "val"]), sort = False)
        
        for file in filenames:
            self.df = self.df.append(pd.read_csv(file, names = ["ts", "val"]), ignore_index = True, sort= False)
        
        self.signal_count = 0   #tracks for next
		
    def next (self):
        signal = Signal (self.df.ts[self.signal_count:self.signal_count+self.batchsize], self.df.val[self.signal_count:self.signal_count+self.batchsize])
        self.signal_count+=self.batchsize
        #print(signal.ts)
        return signal

def normalize(signal, transfer):   #transfer is array for denom of transfer function?
    return signal.normalize(signal, transfer)

def resample(signal, num):
    return signal.resample(signal, num)

def filter(signal):
     

if __name__ == "__main__":
    filenames = ["ex1.csv", "ex2.csv", "ex3.csv"]
    signals = CSVSignal(filenames, 2)
    #print(signals.df)
    e = signals.next()
    print(type(e.val))
    s = signals.next()
    print(s.ts)
	
