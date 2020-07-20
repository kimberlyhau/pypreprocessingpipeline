import pandas as pd

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
            self.df = self.df.append(pd.read_csv(file, names = ["ts", "val"]), sort= False)
        
        self.signal_count = 0   #tracks for next
		
    def next (self):
        signal = Signal (self.df.ts[self.signal_count:self.signal_count+self.batchsize], self.df.val[self.signal_count:self.signal_count+self.batchsize])
        self.signal_count+=self.batchsize
        return signal

if __name__ == "__main__":
    filenames = ["ex1.csv", "ex2.csv", "ex3.csv"]
    signals = CSVSignal(filenames, 2)
    print(signals.df)
    e = CSVSignal.next
	
