startevent = 120
stopevent = 2122  #  startevent + 0

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib
#from matplotlib import dates
#import datetime as dt

def read_data_file(filename):
    try:
        frame = pd.read_csv(filename, header = None, index_col=0, sep='\s+', 
                            skiprows = 45, nrows = 800)

        off = [38, 39, 42, 43, 46, 47, 50, 51, 54, 55, 58, 59, 62, 63, 64]
        frame = frame.drop(columns = [x for x in off])
        frame = frame.drop(columns = [x for x in range(65,113)])
        return frame

    except Exception as e:
        errormsg = e.args[0]
        #errortype = errormsg.split('.')[0].strip()
        print(errormsg)
        return 'NULL'

''' чтение пьедесталов и коэффициентов для учета напряжения для событий '''
pied = pd.read_csv('piedestal01.csv', index_col=0)
print('len_pied', len(pied))

framecol = [ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 
            40, 41, 44, 45, 48, 49, 52, 53, 56, 57, 60, 61]

''' построение спектра '''

dirname = '../data.txt/'
startx,stopx = 450,600
binnum = 1000    ## bin number in hist

ss = [[0] * len(framecol)]* binnum
diff = pd.DataFrame(ss, columns=framecol)

for i in range(startevent,stopevent): #pied.shape[0]):
    #if i%5 == 1:

    ss = [[0] * len(framecol)]* binnum
    diff = pd.DataFrame(ss, columns=framecol)

    ## read data frame
    filename = dirname + str(pied.EID[i]) + '.txt'
    frame = read_data_file(filename) 
    print(i, filename)

    # ''' new column with parity '''
    for j in frame.index:
        frame.loc[j,'par'] = int(j%2) 

    #for chan in [1,22]:
    for chan in frame.columns[:-1]:

        ## ''' minus piedestal '''
        p0 = pied.loc[i, 'p0_'+str(chan)]
        p1 = pied.loc[i, 'p1_'+str(chan)]

        datum = (frame[chan] - (1 - frame.par) * p0 - frame.par * p1)[startx:stopx]
        hists = plt.hist(datum, bins=np.arange(0, binnum+1, 1))

        diff[chan] = diff[chan] + hists[0]
        plt.close()

    filename='diff.' + str(pied.EID[i]) + '.csv'
    diff.to_csv(filename)

## make integral spectrum
integral = pd.DataFrame([[0] * len(frame.columns[:-1])]* binnum)
for chan in frame.columns[:-1]:
    integral[chan] = diff[chan].sum() - diff[chan].cumsum()   

## save spectrums to file
filename='integral' + str(startevent) + '-' + str(stopevent) + '.csv'
integral.to_csv(filename)
filename='diff' + str(startevent) + '-' + str(stopevent) + '.csv'
diff.to_csv(filename)

print('OK')
