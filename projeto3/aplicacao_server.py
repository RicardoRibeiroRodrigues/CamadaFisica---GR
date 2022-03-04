#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from enlace import *
import time
import numpy as np
from datagrama import monta_header

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM6"                  # Windows(variacao de)

HANDSHAKE = b"\x00"
RESPOSTA_HANDSHAKE = b"\x01"
DADOS = b"\x02"
COMANDOS = b"\x03"
CONFIRMACAO = b"\x04"
ERRO = b"\x05"
IPV4 = b"\x01"
IPV6 = b"\x02"
PC_RICARDO = b"\x01"
PC_FONTANA = b"\x02"
EOP = b"\xFF\xFF\xFF\xFF"

def resposta(com1, head, resposta):

    header = monta_header(
        resposta,
        IPV6,
        b"\x01",
        len(mensagem).to_bytes(1, "big"),
        PC_RICARDO,
        PC_FONTANA,
        b"\x01",
        b"\x00\x00\x00",
    )
    com1.sendData(np.asarray(header))
    time.sleep(0.01)
    com1.sendData(np.asarray(mensagem))
    time.sleep(0.01)
    com1.sendData(np.asarray(EOP))
    time.sleep(0.01)


def main():
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace('/dev/ttyACM0')

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()

        while True:
            rxBufferHeader, nRx = com1.getData(10)
            print("Recebi head!")
            if rxBufferHeader[0] == HANDSHAKE:
                resposta(com1, rxBufferHeader, RESPOSTA_HANDSHAKE)
            if rxBufferHeader[0] == DADOS:
                resposta(com1, rxBufferHeader, CONFIRMACAO)
            final, _ = com1.getData(4)
            if final == EOP:
                print("receba!")
                break

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
