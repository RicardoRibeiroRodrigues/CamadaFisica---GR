# Projeto 8 - Modulação AM

## Objetivo:
O objetivo é transmitir um áudio que ocupe bandas de baixas frequências (entre 20 Hz e 2.500 Hz)
através de um canal de transmissão em que você possa utilizar apenas as bandas entre 10.500 Hz e 15.500 Hz. Após
a transmissão via sinal acústico, o receptor, que gravou o sinal transmitido, deverá demodular o sinal e reproduzi-lo,
de maneira audível novamente. 

## Requisitos:
- 1 computador com python instalado.  
Instalação das dependências:
```cmd
pip install peakutils sounddevice matplotlib numpy soundfile
```

## Execução do código:
Para executar o código, baixe um áudio no formato .wav e rode o arquivo "encode.py" em um terminal:      
(Note que você tem que trocar no encode.py o arquivo que vai ser lido na linha 10).
```cmd
python encode.py
```
Em seguida em outro terminal rode o arquivo "decode.py":     
(Ao rodar o encode.py, deve ter sido salvo um arquivo "final.wav" no seu pc, ele é necessário para rodar o decode.py). 
```cmd
python decode.py
```