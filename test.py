from pylab import *

dt = 0.0005
t = arange(0.0, 20.0, dt)
s1 = sin(2*pi*500*t)
s2 = 2*sin(2*pi*400*t)

# create a transient "chirp"
mask = where(logical_and(t>10, t<12), 1.0, 0.0)
s2 = s2 * mask

# add some noise into the mix
nse = 0.01*randn(len(t))

x = s1  # the signal
NFFT = 1024       # the length of the windowing segments
Fs = int(1.0/dt)  # the sampling frequency

# Pxx is the segments x freqs array of instantaneous power, freqs is
# the frequency vector, bins are the centers of the time bins in which
# the power is computed, and im is the matplotlib.image.AxesImage
# instance
a=[1,2,3,4,5]
b=[9,8]
print(concatenate((a[:1],a[:-1]),1))
a[0]=b
print(a)
#ax1 = subplot(211)
#plot(t, x)
#subplot(212, sharex=ax1)
#Pxx, freqs, bins, im = specgram(x, NFFT=NFFT, Fs=Fs, noverlap=900,
#                                cmap=cm.gist_heat)
#show()
