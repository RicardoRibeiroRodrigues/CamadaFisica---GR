# Projeto 3 - – Fragmentação, hand-shake e datagrama

## Objetivos:

### Parte I – Datagrama:
As mensagens entre client e server devem ser enviadas usando pacotes compondo datagramas, considerando o seguinte datagrama:
- HEAD – 10 BYTES - fixo.
- PAYLOAD – variável entre 0 e 114 BYTES (pode variar de pacote para pacote).
- EOP – 4 BYTES – fixo (valores de sua livre escolha).

### Parte II – Handshake
Antes do início do envio da mensagem, o client deve enviar uma mensagem para verificar se o server está
“vivo”, pronto para receber o arquivo a ser enviado. O server então deve responder como uma mensagem
informando que ele está pronto para receber.
Caso o servidor responda ao cliente em menos de 5 segundos, o cliente deve iniciar a transmissão do arquivo.

### Parte III – Fragmentação
Como seu payload é menor que o arquivo a ser enviado, ele deverá ser enviado em partes (pacotes).

### Parte IV – Acknowledge / Not acknowlwdge
Durante a transmissão de dados é muito comum troca de mensagens como confirmação de recebimento de
um pacote ou mesmo informando um problema na recepção do pacote. Esse tipo de comunicação gera uma
robustez para a transmissão, embora possa afetar a velocidade de transmissão. Existe então um compromisso entre
a velocidade de transmissão e a segurança da transmissão no que diz respeito à integridade dos dados.

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
```
