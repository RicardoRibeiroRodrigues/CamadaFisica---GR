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
from utils import bytes_to_list

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM6"                  # Windows(variacao de)

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

DADOS = 2
COMANDOS = b"\x03"
CONFIRMACAO = b"\x04"
ERRO = b"\x05"
IPV4 = b"\x01"
IPV6 = b"\x02"
ID_SERVER = 0


def resposta(com1, head, resposta, n_pacote=0):

    n_pacote = n_pacote.to_bytes(1, byteorder='big')
    header = monta_header(
        resposta,
        IPV6,
        n_pacote,
        b"\x01",
        b"\x01",
        b"\x00",
        b"\x01",
        b"\x00\x00\x00",
    )
    pacote = (header+b"\x00"+EOP)
    com1.sendData(np.asarray(pacote))
    time.sleep(0.01)
"""     com1.sendData(np.asarray(b"\x00"))
    time.sleep(0.01)
    com1.sendData(np.asarray(EOP))
    time.sleep(0.01) """


def main():
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace('/dev/ttyACM0')

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()

        while True:
            ocioso = True
            content = b""
            rxBufferHeader, nRx = com1.getData(10)
            i = 0
            while ocioso:
                if rxBufferHeader[0] == TIPO_1:
                    ocioso = False
                elif rxBufferHeader[0] == TIPO_3:
                    message_size = rxBufferHeader[6]
                    ocioso = False
            time.sleep(1)
            client = rxBufferHeader[5]
            size = rxBufferHeader[3]
            info, _ = com1.getData(size)
            final, _ = com1.getData(4)
            if i == size:
                with open("img/icon.png", "wb") as img:
                    img.write(content)
                print("Receba!!!! Graças a deus, SIUUUUU!!!")
                break
            if rxBufferHeader[0] == TIPO_1:
                resposta(com1, rxBufferHeader, TIPO_2)
                ocioso = True
            elif rxBufferHeader[0] == TIPO_3:
                pacote_certo = rxBufferHeader[2] == i
                if not pacote_certo:
                    print("O número do pacote está incorreto, reenviando número do pacote correto!")
                if bytes_to_list(final) == bytes_to_list(EOP) and pacote_certo:
                    content += info
                    i += 1
                    resposta(com1, rxBufferHeader, TIPO_4)
                    print("uma resposta recebida")
                    ocioso = True
                else:
                    print("deu errado, to no else")
                    if com1.rx.getBufferLen() > 0:
                        print("Tamanho informado errado")
                    com1.rx.clearBuffer()
                    resposta(com1, rxBufferHeader, TIPO_6, i)
                    ocioso = True
    except TimeoutError:
        print("Tempo excedido! Tentar novamente.")
        resposta(com1, rxBufferHeader, TIPO_5, i)





                        


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
