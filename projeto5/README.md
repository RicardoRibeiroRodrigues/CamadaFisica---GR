# Projeto 5 - CRC

## Objetivo:
Implementar o CRC para cada pacote enviado no [projeto 4](https://github.com/RicardoRibeiroRodrigues/CamadaFisicaGR/tree/main/projeto4). O CRC deve ser de 16bits.

## Requisitos:
- 2 arduinos.
- Cabos jumper para fazer as conexões.
- 1(ou 2) computador(es) com python instalado.  
Instalação das dependências:
```cmd
pip install pyserial
```

## Montagem e execução do código:
Para a montagem, conecte o pino rx de um arduino ao pino tx do outro arduino faça isso para os dois, assim como o pino reset no GND e um GND de um arduino no GND do outro, feito isso conecte os arduinos às portas USB do(s) computador(es).
<br/>
Para executar o código, crie uma pasta "img" na pasta do server e rode o arquivo "aplicacao_server.py" em um terminal:
```cmd
python aplicacao_server.py
```
Em seguida em outro terminal rode o arquivo "aplicacao_client.py":      
(Você pode trocar a imagem dentro da pasta img para a transmissão se for desejado)
```cmd
python aplicacao_client.py
