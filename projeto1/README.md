# Projeto 1 - loop back
Transmissão e recepção serial simultâneas.
<br>

## Objetivo:
1. Enviar uma imagem (a menor possível) através da porta de comunicação serial.
2. Receber a imagem simultaneamente ao envio e salva-la como uma cópia. Para isso a recepção do Arduino
(pino rx) deve estar curto-circuitada com o pino de transmissão (pino tx).
## Requisitos:
- 1 arduino.
- 1 computador com python instalado.  
Instalação das dependências:
```cmd
pip install pyserial
```
## Montagem e execução do código:
Para utilizar o código, conecte o pino rx ao pino tx do arduino, assim como o pino reset no GND, feito isso conecte o arduino à porta USB do computador.   
Para executar o código, crie uma pasta "img" na pasta do projeto, coloque nela a imagem a ser transmitida e rode o aquivo "aplicacao.py".
```cmd
python aplicacao.py
```
