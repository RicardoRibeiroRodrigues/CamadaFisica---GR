# Projeto 4 - Protocolo de comunicação UART ponto a ponto.

## Objetivo:
Ano de 2026. Agora você é um(a) engenheiro(a) de computação recém-contratado(a) para desenvolver a comunicação entre
sensores de campo (que enviam periodicamente dados) e aplicações locais que armazenam os dados em um banco SQL. Os
sensores não têm a funcionalidade de envio de dados via protocolo TCP-IP, porém têm um processador que pode rodar uma
aplicação Python e também possui um chip UART, podendo comunicar-se serialmente.<br>
Você então tem a tarefa de implementar uma aplicação para os sensores se comunicarem serialmente com padrão UARTde
maneira segura, sem perda de dados . A comunicação deve ser feita para envio de arquivos para os servidores, sendo uma rotina
de envio executada pelo sensor toda vez que este tem um arquivo a ser enviado.<br>
Seu cliente lhe contratou exigindo que a camada superior da comunicação deve funcionar seguindo
uma estratégia já definida, onde os arquivos são enviados em pacotes, respeitando o datagrama definido a seguir.
### Datagrama:
- HEAD:
  - h0 – tipo de mensagem
  - h1 – livre
  - h2 – livre
  - h3 – número total de pacotes do arquivo
  - h4 – número do pacote sendo enviado
  - h5 – se tipo for handshake:id do arquivo
  - h5 – se tipo for dados: tamanho do payload
  - h6 – pacote solicitado para recomeço quando a erro no envio.
  - h7 – último pacote recebido com sucesso.
  - h8 – h9 – CRC
- PAYLOAD – variável entre 0 e 114 bytes. Reservado à transmissão dos arquivos.
- EOP – 4 bytes: 0xAA 0xBB 0xCC 0xDD
### Protocolo UART:
#### Padrão:
UART, baudrate de 115200, sem bit de paridade.
#### Datagrama:
Cada envio deve ser feito como um datagrama completo, contendo head, payload e eop, ou seja, não é permitido envios que não
contenham head, payload(ocasionalmente nulo) e eop. O tamanho do payload não pode ultrapassar 114 bytes e o tamanho do
datagrama não deve ser maior que 128 bytes

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
