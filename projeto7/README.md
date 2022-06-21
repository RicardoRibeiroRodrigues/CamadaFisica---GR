# Projeto 7 - DTMF

## Objetivos:
Implementar via software um sistema de transmissão do dual tone multi frequency, um sinal de
áudio utilizado pelas empresas de telefonia para detectar o sinal digitado pelo usuário.

## Requisitos:
- 2 computadores com python instalado.  
Instalação das dependências:
```cmd
pip install peakutils sounddevice matplotlib numpy
```

## Execução do código:
Para executar o código, rode o arquivo "encode_versaoAlunos.py" em um terminal e digite a tecla que deseja enviar:
```cmd
python encode_versaoAlunos.py
```
Em seguida em outro terminal rode o arquivo "decode_versaoAlunos.py":      
```cmd
python decode_versaoAlunos.py
```
OBS: Os computadores devem estar perto o suficiente para que o som do teclado DTMF seja detectado pelo receptor.
