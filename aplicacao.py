#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from email import header
from enlace import *
import time
import numpy as np
from random import randint
from datagrama import monta_header

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"  # Windows(variacao de)

# Tipos de pacote
HANDSHAKE = b"\x00"
RESPOSTA_HANDSHAKE = b"\x01"
DADOS = b"\x02"
COMANDOS = b"\x03"
CONFIRMACAO = b"\x04"
ERRO = b"\x05"

# Outras infos do header
IPV4 = b"\x01"
IPV6 = b"\x02"
PC_RICARDO = b"\x01"
PC_FONTANA = b"\x02"
EOP = b"\xFF\xFF\xFF\xFF"


def fragmenta(mensagem):
    lista_payloads = []
    tamanho_msg = len(mensagem)
    num_payloads = (
        tamanho_msg // 114 if not tamanho_msg % 114 else 1 + tamanho_msg // 114
    )
    for i in range(num_payloads):
        lista_payloads.append(mensagem[i * 114 : (i + 1) * 114])

    return lista_payloads


def handshake(com1):
    header = monta_header(
        HANDSHAKE,
        IPV6,
        b"\x01",
        b"\x01",
        PC_FONTANA,
        PC_RICARDO,
        b"\x01",
        b"\x00\x00\x00",
    )
    print(header)
    while True:
        try:
            com1.sendData(np.asarray(header))
            time.sleep(0.01)
            com1.sendData(np.asarray(b"\x00"))
            time.sleep(0.01)
            com1.sendData(np.asarray(EOP))
            time.sleep(0.01)
            # Recebe a resposta do servidor
            rxBuffer, _ = com1.getData(10)
            print("Recebeu o HEAD do server")
            payload = rxBuffer[3]
            resposta = rxBuffer[0]
            if resposta == RESPOSTA_HANDSHAKE:
                print("O servidor respondeu")
            # Pega a msg de resposta do servidor (payload)
            rxBuffer, _ = com1.getData(payload)
            rxBuffer, _ = com1.getData(4)
            if rxBuffer == EOP:
                print("Handshake deu certo!")
                return True
            print("Algo deu errado, refazendo o handshake")
        except RuntimeError:
            resposta = input("Servidor inativo. Tentar novamente?(S/N) ")
            if resposta == "N":
                return False


def envia_mensagem(lista_payloads, com1):
    i = 0
    while i < len(lista_payloads):
        # Define parametros de header
        n_pacote = i.to_bytes(1, "big")
        payload = lista_payloads[i]
        tamanho_pacote = len(payload).to_bytes(1, "big")
        n_pacotes = len(lista_payloads).to_bytes(1, "big")
        # Monta o header com os parametros
        header = monta_header(
            DADOS,
            IPV6,
            n_pacote,
            tamanho_pacote,
            PC_FONTANA,
            PC_RICARDO,
            n_pacotes,
            b"\x00\x00\x00",
        )
        # Manda o pacote para o servidor
        com1.sendData(np.asarray(header))
        time.sleep(0.01)
        com1.sendData(np.asarray(payload))
        time.sleep(0.01)
        com1.sendData(np.asarray(EOP))
        # Confirma que o servidor recebeu corretamente
        header_server, _ = com1.getData(10)
        _, _ = com1.getData(header_server[3])
        final_server, _ = com1.getData(4)
        if header_server[0] == CONFIRMACAO and final_server == EOP:
            print("O servidor recebeu o payload corretamente, mandando o prox")
            i += 1


def main():
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação serial
        com1.enable()

        res = handshake(com1)

        if res:
            pass

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
    # with open("img/icon.png", "rb") as img:
    #     coisa = img.read()
    #     print(len(coisa))
    #     print(len(fragmenta(coisa)))
