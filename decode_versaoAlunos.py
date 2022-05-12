#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

# Importe todas as bibliotecas
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from suaBibSignal import *
import peakutils
import sys


DTMF_MAP = {
    1: (697, 1206),
    2: (697, 1339),
    3: (697, 1477),
    "A": (697, 1633),
    4: (770, 1206),
    5: (770, 1339),
    6: (770, 1477),
    "B": (770, 1633),
    7: (852, 1206),
    8: (852, 1339),
    9: (852, 1477),
    "C": (852, 1633),
    "X": (941, 1206),
    0: (941, 1339),
    "#": (941, 1477),
    "D": (941, 1633),
}


def signal_handler(signal, frame):
    print("You pressed Ctrl+C!")
    sys.exit(0)


# funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10 * np.log10(s)
    return sdB


def caractere_mais_prox(frequencias):
    mais_prox = None
    menor_dist = (10, 10)
    for char, tupla in DTMF_MAP.items():
        diff_0 = abs(frequencias[0] - tupla[0]) < menor_dist[0]
        diff_1 = abs(frequencias[1] - tupla[1]) < menor_dist[1]
        if diff_0 and diff_1:
            mais_prox = char
            menor_dist = (diff_0, diff_1)
    return mais_prox


def main():

    # declare um objeto da classe da sua biblioteca de apoio (cedida)
    # declare uma variavel com a frequencia de amostragem, sendo 44100

    # voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    fs = 44_100
    sd.default.samplerate = fs  # Taxa de amostragem
    sd.default.channels = 2  # Voce pode ter que alterar isso dependendo da sua placa
    # Tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    duration = 2
    signal = signalMeu()

    # Faça um print na tela dizendo que a captacao comecará em n segundos. e entao
    # Use um time.sleep para a espera
    print("A captação de audio comecará em 2 segundos")
    time.sleep(2)
    # Faça um print informando que a gravacao foi inicializada
    print("iniciando a gravação")
    # Declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ...
    # Calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = duration * fs
    freqDeAmostragem = fs
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")

    # analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...

    y = audio[:, 0]
    # grave uma variavel com apenas a parte que interessa (dados)

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    inicio = 0
    fim = duration
    numPontos = int(fs * duration)
    t = np.linspace(inicio, fim, numPontos)

    # plot do gravico  áudio vs tempo!
    plt.plot(t, y)
    plt.title("Audio no tempo")
    plt.xlabel("Tempo em segundos")
    plt.ylabel("Sinal")

    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(y, fs)
    plt.figure("F(y)")
    plt.plot(xf, np.abs(yf))
    plt.grid()
    plt.title("Fourier audio")

    # esta funcao analisa o fourier e encontra os picos
    # voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    # voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    # frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.

    index = peakutils.indexes(np.abs(yf), thres=0.1, min_dist=200)
    freq_picos = xf[index]
    # printe os picos encontrados!
    for freq in xf[index]:
        print(f"Frequencia de pico: {freq}")

    # encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    tecla = caractere_mais_prox(freq_picos)
    print(f"A tecla é a {tecla}")

    # print a tecla.

    ## Exibe gráficos
    plt.show()


if __name__ == "__main__":
    main()
