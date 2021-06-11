import numpy as np
from scipy import io
from scipy.signal import butter,filtfilt,lfilter
import math
from scipy import signal
from scipy.fft import fft
from matplotlib import pyplot as plt

mat_file_name='./.input_data/test.mat'
mat_file=io.loadmat(mat_file_name)
#data=mat_file('data')


data=mat_file['DATA']

used_data=data[0:2500, 0]
used_data2=data[0:2500,0]


cnt = 0
Fs=250
T=1/Fs

###########필터함수###########
def fir_filter(data, lowcut, highcut, fs, order=400):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    
    coeff = signal.firwin(order+1, [lowcut, highcut], nyq=nyq, window='hamming', pass_zero=False)
    output = signal.filtfilt(coeff, 1.0, data)
    return output
#####################################

k_end = len(used_data)/(10*Fs)
k_end=math.floor(k_end)


for k in range(k_end):
    if(len(used_data) < (k+1)*5*Fs):
        break;
       #used_data5s = used_data[k*5*Fs+1 : len(used_data)]
    else:
        used_data5s = used_data[(k*10*Fs) : ((k+1)*10*Fs)]
        
    L=len(used_data5s)
    
    #t = (0:L-1)*T
    temp_t=range(L)
    t=np.array(temp_t)
    t=T*t
   ###############호흡################
    ymr = fir_filter(used_data5s, 0.16, 0.66, 250, 400)
    num, properties = signal.find_peaks(ymr, prominence=(None,0.8))
    #w, h = signal.freqs(b, a)
    cnt += len(num)
    S2 = fft(ymr)

    P21 = abs(S2/L)
    P12 = P21[0:(L//2)]
    P12[1:len(P12)-2] = 2*P12[1:len(P12)-2]
    
   # f = Fs*[0:(L/2)]/L
    temp_f=range((L//2)+1)
    f=np.array(temp_f)
    f=Fs*f/L
    
    fL1 = np.argmax(P12[1:200]) + 1
    f11 = fL1*Fs/L
    ResL = 60*f11
    
    #####################심박############
    ymh = fir_filter(used_data5s, 0.83, 2.5, 250, 400)
    num, properties = signal.find_peaks(ymr, prominence=(None,0.8))
    #w, h = signal.freqs(b, a)
    cnt += len(num)
    S3 = fft(ymh)

    P23 = abs(S3/L)
    P13 = P23[0:(L//2)]
    P13[1:len(P13)-2] = 2*P13[1:len(P13)-2]
    

    
    fL2 = np.argmax(P13[1:200]) + 1
    f12 = fL2*Fs/L
    HR_L = 60*f12
    ###############################################
    #print(ymr)
    #plt.plot(used_data5s, 'y', label='origin')
    #plt.plot(ymr, 'b', label='filter')
    #plt.semilogx(w, 20*np.log10(abs(h)))
    #plt.xlabel('freq')
    #plt.ylabel('amp')
    #plt.plot(num, ymr[num], "x")
    #plt.legend()
    #plt.show() 
   ##########################################    

print('호흡수 : ',ResL)
print('심박수 : ',HR_L)
