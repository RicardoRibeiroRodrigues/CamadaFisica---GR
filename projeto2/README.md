# Projeto 2 - Client-Server em tempo real

## Objetivo: 
1. Uma aplicação (client) deverá enviar via transmissão serial UART uma
sequência de comandos (lista de bytes) para outra aplicação (server).
2. A sequência deve ter entre 10 e 30 comandos, a ser determinada pelo client (aleatoriamente).
3. Após a recepção, o server deverá retornar ao client uma mensagem informando o número de comandos que foi
recebido.
4. Assim que o client receber a resposta com este número, poderá verificar se todos os comandos foram recebidos, e o
processo termina.
5. Caso o número de comandos informado pelo server não esteja correto, o cliente deverá expor uma mensagem
avisando a inconsistência.
6. Se o server não retornar nada em até 10 segundos, o cliente deverá expor uma mensagem de “time out”.


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
Para executar o código, rode primeiro o arquivo "aplicacao_server.py" em um terminal:
```cmd
python aplicacao_server.py
```
Em seguida em outro terminal rode o arquivo "aplicacao_client.py":
```cmd
python aplicacao_client.py
```
