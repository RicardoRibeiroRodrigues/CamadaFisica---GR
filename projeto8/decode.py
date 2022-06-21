import soundfile as sf
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import signalCalc as sc
import funcoes_LPF as lpf

calc = sc.signalCalc()

# Read a sound file named 'final.wav'
fs = 44_100  # (sample rate [Hz])
sd.default.samplerate = fs
sd.default.channels = 1
audio, samplerate = sf.read("final.wav")

# Separate only the y of the signal
# yaudio = audio[:, 1]

# Calculate the FFT of the signal
xf, yf = calc.calcFFT(audio, samplerate)

# Plot the fft
plt.figure()
plt.plot(xf, np.abs(yf))
plt.title("Fourier - Received audio")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude [V]")
plt.xlim(8_500, 17_500)
# Make a vertical line at 10500 hz
plt.axvline(x=10_500, color="orange", label="Lower limit", linestyle="--")
# Make a vertical line at 15500 hz
plt.axvline(x=15_500, color="red", linestyle="dashed", label="Upper limit")
plt.legend()
plt.show()

# Demodulate the signal to a carrier with frequency of 13kHz
samplesaudio = len(audio)
audio_time = samplesaudio / fs
x, carrier = calc.generateSin(13_000, 1, audio_time, fs)
demodulated = carrier * audio

# Plot the demodulated signal
plt.figure()
plt.plot(x, demodulated)
plt.title("Demodulado - Tempo")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude [V]")
# Plot the FFT of demodulated signal on frequency domain
xf, yf = calc.calcFFT(demodulated, fs)
plt.figure()
plt.plot(xf, np.abs(yf))
plt.title("Demodulado - Dominio da frequencia")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude [V]")


# Filter the signal with a low pass filter (cutoff frequency = 2500Hz)
filtered_audio = lpf.LPF(demodulated, 2500, fs)

# Plot the fft of the filtered signal
xf, yf = calc.calcFFT(filtered_audio, fs)
plt.figure()
plt.plot(xf, np.abs(yf))
plt.title("Filtrado e demodulado - Dominio da frequencia")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude [V]")
plt.show()

# Play the filtered audio
res = input("Deseja escutar o audio? (s/n)")

if res == "s":
    sd.play(filtered_audio)
    sd.wait()
