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
from erros import timer1Error
from utils import bytes_to_list, para_inteiro, escreve_log

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM1"  # Windows(variacao de)

# Tipos de pacote
# Chamado do cliente para o servidor (HandShake)
TIPO_1 = b"\x01"
# Resposta do servidor para o cliente ao HandShake
TIPO_2 = b"\x02"
# Mensagem do tipo de dados.
TIPO_3 = b"\x03"
# Mensagem recebida pelo servidor
TIPO_4 = b"\x04"
# Mensagem de time out -> Dois lados
TIPO_5 = b"\x05"
# Mensagem de erro -> Servidor envia
TIPO_6 = b"\x06"

EOP = b"\xAA\xBB\xCC\xDD"

ARQUIVO_LOG = "Client1.txt"


def fragmenta(mensagem):
    lista_payloads = []
    tamanho_msg = len(mensagem)
    num_payloads = (
        tamanho_msg // 114 if not tamanho_msg % 114 else 1 + tamanho_msg // 114
    )
    for i in range(num_payloads):
        lista_payloads.append(mensagem[i * 114 : (i + 1) * 114])

    return lista_payloads


def handshake(com1, tamanho_msg: int):
    reenvio = False
    header = monta_header(
        TIPO_1,
        b"\x00",
        b"\x00",
        tamanho_msg.to_bytes(1, "big"),
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
        b"\x00",
    )
    while True:
        try:
            print("Mandou o HandShake, esperando resposta!")
            pacote = header + EOP
            com1.sendData(np.asarray(pacote))
            time.sleep(0.01)
            # Faz o log do envio
            timer1 = time.time()
            if not reenvio:
                escreve_log(ARQUIVO_LOG, "envio", 1, 1, 0, tamanho_msg)
                timer2 = time.time()
            else:
                reenvio = False
                escreve_log(ARQUIVO_LOG, "reenvio", 1, 1, 0, tamanho_msg)

            # Recebe a resposta do servidor
            rxBuffer, _ = com1.getData(10, timer1, timer2)
            print("Recebeu o HEAD do server")

            id_arquivo = rxBuffer[5]
            resposta_server = rxBuffer[0]

            if resposta_server == 1:
                print("O servidor respondeu!")

            # Pega a msg de resposta do servidor (payload)
            # rxBuffer, _ = com1.getData(0, timer1, timer2)
            rxBuffer, _ = com1.getData(4, timer1, timer2)

            if bytes_to_list(rxBuffer) == bytes_to_list(EOP):
                print("Handshake deu certo!")
                # Log de recebimento
                escreve_log(ARQUIVO_LOG, "recebe", 2, id_arquivo, 0, tamanho_msg)
                return True

            print("Algo deu errado, refazendo o handshake")
        except timer1Error:
            reenvio = True
        except TimeoutError:
            resposta = input("Servidor inativo. Tentar novamente?(S/N) ")
            if resposta == "N":
                return False


def envia_mensagem(lista_payloads, com1):
    i = 1
    reenvio = False
    n_pacotes = len(lista_payloads).to_bytes(1, "big")

    while i < len(lista_payloads):
        try:
            # Define parametros de header
            n_pacote = i.to_bytes(1, byteorder="big")
            payload = lista_payloads[i]

            tamanho_pacote = (len(payload)).to_bytes(1, byteorder="big")
            # Monta o header com os parametros
            header = monta_header(
                TIPO_3,
                b"\x00",
                b"\x00",
                n_pacotes,
                n_pacote,
                tamanho_pacote,
                n_pacotes,
                b"\x00",
                b"\x00",
                b"\x00",
            )
            print(f"Numero do pacote: {i}")

            # Manda o pacote para o servidor
            pacote = header + payload + EOP
            com1.sendData(np.asarray(pacote))
            time.sleep(0.01)

            timer1 = time.time()
            if not reenvio:
                timer2 = time.time()
            print("Enviou a mensagem")
            if not reenvio:
                escreve_log(
                    ARQUIVO_LOG, "envio", 3, n_pacote, tamanho_pacote, n_pacotes
                )
            else:
                reenvio = True
                escreve_log(
                    ARQUIVO_LOG, "reenvio", 3, n_pacote, tamanho_pacote, n_pacotes
                )

            # Confirma que o servidor recebeu corretamente
            header_server, _ = com1.getData(10, timer1, timer2)
            print("Recebe o HEAD")

            _, _ = com1.getData(header_server[5], timer1, timer2)
            final_server, _ = com1.getData(4, timer1, timer2)

            # Condicoes para a mensagem estar correta
            confirma = header_server[0] == para_inteiro(TIPO_4)
            final_pacote = bytes_to_list(final_server) == bytes_to_list(EOP)
            mensagem_t6 = header_server[0] == para_inteiro(TIPO_6)

            if confirma and final_pacote:
                escreve_log(
                    ARQUIVO_LOG, "recebimento", 4, header_server[5], n_pacote, n_pacotes
                )
                print("O servidor recebeu o payload corretamente, mandando o prox")
                i += 1
            elif mensagem_t6:
                escreve_log(
                    ARQUIVO_LOG, "recebimento", 6, header_server[5], n_pacote, n_pacotes
                )
                if i != header_server[4]:
                    print("O numero do pacote estava incoerente com o do server")
                i = header_server[4]
                com1.rx.clearBuffer()
                print("Algo deu errado, tentando novamente")
        except timer1Error:
            reenvio = True
        except TimeoutError:
            print("O servidor demorou demais para responder")
            header = monta_header(
                TIPO_5,
                b"\x00",
                b"\x00",
                n_pacotes,
                n_pacote,
                tamanho_pacote,
                n_pacotes,
                b"\x00",
                b"\x00",
                b"\x00",
            )
            pacote = header + b"\x00" + EOP
            com1.sendData(np.asarray(pacote))
            time.sleep(0.01)
            com1.disable()
            return


def main():
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação serial
        com1.enable()

        with open("img/icon.png", "rb") as file:
            mensagem = fragmenta(file.read())

        res = handshake(com1, len(mensagem))

        if res:
            envia_mensagem(mensagem, com1)

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
    #     envia_mensagem(fragmenta(coisa), com1)
