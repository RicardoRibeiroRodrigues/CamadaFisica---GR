import sounddevice as sd
import soundfile as sf
from funcoes_LPF import LPF
from signalCalc import *

calc = signalCalc()
fs = 44100  # taxa de amostragem (sample rate)
sd.default.samplerate = fs
sd.default.channels = 1
audio, samplerate = sf.read("Siuu.wav")
yaudio = audio[:, 1]

print(f"Samplerate: {samplerate}")
audio_filtrado = LPF(yaudio, 2500, fs)
samplesaudio = len(audio_filtrado)
audio_time = samplesaudio / fs

# Plot the audio_filtrado signal
plt.figure()
t = np.linspace(0, audio_time, len(audio_filtrado))
plt.plot(t, audio_filtrado)
plt.title("Audio filtrado - Dominio do tempo")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude [V]")

# Plot the FFT of the audio_filtrado signal
xf, yf = calc.calcFFT(audio_filtrado, fs)
plt.figure()
plt.plot(xf, np.abs(yf))
plt.title("Filtrado - Dominio da frequencia")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude [V]")

res = input("Deseja escutar o audio filtrado? (s/n)")
if res == "s":
    sd.play(audio_filtrado)
    sd.wait()

# Modulate the signal to a carrier with frequency of 13kHz
print(f"Tempo do audio: {audio_time}")
x, portador = calc.generateSin(13_000, 1, audio_time, fs)
modulado = portador * audio_filtrado

# Plot the modulado signal
plt.figure()
plt.plot(x, modulado)
plt.title("Modulado - Tempo")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude [V]")

# Plot the FFT of modulado signal
xf, yf = calc.calcFFT(modulado, fs)
plt.figure()
plt.plot(xf, np.abs(yf))
plt.title("Modulado - Fourier")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude [V]")

# normalize the signal
normalizado = modulado / np.max(np.abs(modulado))
res = input("Deseja escutar o audio modulado e normalizado? (s/n)")

# Plot the normalizado signal
plt.figure()
plt.plot(x, normalizado)
plt.title("Normalizado - Tempo")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude [V]")
plt.show()


if res == "s":
    sd.play(normalizado)
    sd.wait()

# Save the signal in a file called 'final.wav'
sf.write("final.wav", normalizado, fs)
