import pandas as pd
from biosppy import signals
from biosppy.signals import tools
from csv import reader
#from scipy import signal

class Signal:
    def __init__(self, ts, val):
        self.ts = ts
        self.val = val

class CSVSignal:
    def __init__(self, filenames, period,  batchsize = 10):
        self.batchsize = batchsize
        self.period = period
        count = 0
        self.df = pd.DataFrame(columns = ["ts","val"])
        for file in filenames:
            with open(file, 'r') as read_obj:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    while int(row[0]) != count:
                        #print(str(row[0])+"+"+str(count))
                        self.df.loc[count/self.period] = [count, None]
                        count+=self.period
                    self.df.loc[count/self.period] = row
                    count+=self.period
        self.signal_count = 0   #tracks for next
		
    def next (self):
        if all(v is None for v in self.df.val[self.signal_count:self.signal_count+self.batchsize].tolist()):
            return 
        signal = Signal (self.df.ts[self.signal_count:self.signal_count+self.batchsize].tolist(), self.df.val[self.signal_count:self.signal_count+self.batchsize].tolist())
        self.signal_count+=self.batchsize
        #print(signal.ts)
        if (None in signal.val):
            signal = fillmean(signal)
        return signal

#def normalize(signal, transfer):   #transfer is array for denom of transfer function?
    #use _scale_amplitude
    #use mean and standard deviation to normalize

def resample(signal, num):
    for i in range(len(signal.ts)):
        signal.ts[i] = int(signal.ts[i])
        signal.val[i] = float(signal.val[i])
    index = pd.date_range('1/1/2000', periods=len(signal.ts), freq='T')
    series = pd.Series(signal.ts, index=index)
    series = series.resample(str(num)+'S').mean()
    signal.ts = series.tolist()
    series = pd.Series(signal.val, index=index)
    series = series.resample(str(num)+'S').mean()
    signal.val = series.tolist()
    return signal

def passfilter(signal):
    signal.val = tools.filter_signal(signal.val, 'FIR', 'bandpass')
    return signal
    
def join_streams(stream1, stream2):
    count1, count2 = 0, 0
    joined = list()
    while (count1 != len(stream1)-1 and count2 != len(stream2)-1):
        if (stream1[count1].ts == stream2[count2].ts):
            joined.append(join(stream1[count1], stream2[count2]))
            count1+=1
            count2+=1
        elif (stream1[count1].ts[0] < stream2[count2].ts[0]):
            index = count1
            while (stream1[index].ts[0]!= stream2[count2].ts[0] and index < len(stream1)):
                index+=1
            if index <len(stream1):
                joined.append(join(stream1[index], stream2[count2]))
                count2+=1
                count1 = index+1
        elif (stream1[count1].ts[0] > stream2[count2].ts[0]):
            index = count2
            while (stream2[index].ts[0]!= stream1[count1].ts[0] and index < len(stream2)):
                index+=1
            if index <len(stream2):
                joined.append(join(stream1[count1], stream2[index]))
                count1+=1
                count2 = index+1
    return joined

def join(signal1, signal2):
    if signal1.ts != signal2.ts:
        return
    value = list()
    for i in range(len(signal1.val)):
        value.append([signal1.val[i], signal2.val[i]])
    joined = Signal(signal1.ts,value)
    return joined 
            
def fillmean(signal):
    mean = 0     
    count = 0
    for value in signal.val:
        if value != None:
            count+=1
            mean+=int(value)
    mean /= count
    for i in range(len(signal.val)):
        if signal.val[i] == None:
            signal.val[i] = mean
    return signal
            
if __name__ == "__main__":
    filenames = ["ex1.csv", "ex2.csv", "ex3.csv"]
    #signals = CSVSignal(filenames, 2, 2)
    s1 = Signal([1,2,3,4,5,6],[1,2,3,4,5,6])
    print(filter(s1).val)
    #print(resample(s1,30).ts)
    #print(resample(s1,30).val)
    s2 = Signal([1,2,3,4,5,6],[1,2,3,4,5,6])
    #print(join(s1, s2).val)
