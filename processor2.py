import pandas as pd
import numpy as np
from biosppy import signals
from biosppy.signals import tools
from sklearn.preprocessing import StandardScaler
import scipy

class Signal:
    def __init__(self, ts, val):
        self.ts = ts #int 
        self.val = val #list

class CSVSignal:
    def __init__(self, filenames, period, windowsize = 10):
        self.filenames = filenames #list
        self.period = period
        self.windowsize = windowsize
        self.filecount = -1
        self.linecount = 0
        self.df = pd.DataFrame()
        self.ts = 0

    def next(self):
        count = 0
        s = Signal(self.ts, [])
        while (count < self.windowsize):
            if (self.linecount >= len(self.df) or self.filecount == -1):
                self.filecount += 1
                self.df = pd.read_csv(self.filenames[self.filecount], names = ["ts", "val"])
                self.linecount=0
            if (self.df.ts[self.linecount] == self.ts):
                s.val.append(float(self.df.val[self.linecount]))
                self.linecount+=1
            else:
                s.val.append(None)
            self.ts+=self.period   
            count +=1 
        if all(v is None for v in s.val):
            return
        return s   

def normalize(signal):
    signal.val  = np.array(signal.val)
    scaler = StandardScaler()
    scaler = scaler.fit(signal.val.reshape(-1, 1))
    signal.val = scaler.transform(signal.val.reshape(-1, 1)).reshape(-1,)
    signal.val = list(signal.val)
    return signal

def filter_signal(signal, fs, freq1, freq2):
    """Filter raw ECG waveform with bandpass finite-impulse-response filter."""
    # Calculate filter order
    order = int(0.3 * fs)

    # Filter waveform
    signal.val, _, _ = tools.filter_signal(signal=signal.val, ftype='FIR', band='bandpass', order=order,
                                       frequency=(freq1, freq2), sampling_rate=fs)
    return signal

def join(signal1, signal2):
    if signal1.ts != signal2.ts:
        return
    value = list()
    for i in range(len(signal1.val)):
        value.append([signal1.val[i], signal2.val[i]])
    joined = Signal(signal1.ts,value)
    return joined 

def fillmean(signal):
    mean = sum(filter(None, signal.val))/(len(signal.val)-signal.val.count(None))
    signal.val = [mean if x== None else x for x in signal.val]
    return signal

def resample(signal, num):
    signal.val = list(scipy.signal.resample(np.array(signal.val), num))
    return signal

if __name__ == "__main__":
    filenames = ["ex1.csv", "ex2.csv", "ex3.csv"]
    signals = CSVSignal(filenames, 1, 4)
    s = signals.next()
    s1 = signals.next()
    print(s.val)
    print(s1.val) 
    print(s.ts)
    print(s1.ts)
    s = fillmean(s)
    s1 = fillmean(s1)
    print(s.val)
    print(s1.val)
    s = join(s,s1)
    print(s.val)
    print(s1.val)
