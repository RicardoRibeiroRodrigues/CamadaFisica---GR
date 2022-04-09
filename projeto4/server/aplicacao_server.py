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
from utils import bytes_to_list, para_inteiro, escreve_log
from erros import Timer1Error, Timer2Error

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"  # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"  # Windows(variacao de)

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
ARQUIVO_LOG = "server1.txt"


def resposta(com1, resposta, n_pacote=1) -> None:
    header = monta_header(
        resposta,
        b"\x00",
        b"\x00",
        (1).to_bytes(1, "big"),
        (n_pacote).to_bytes(1, "big"),
        b"\x01",
        (n_pacote).to_bytes(1, "big"),
        (n_pacote - 1).to_bytes(1, "big"),
        b"\x00",
        b"\x00",
    )
    pacote = header + EOP
    com1.sendData(np.asarray(pacote))
    time.sleep(0.01)
    escreve_log(ARQUIVO_LOG, "envio", para_inteiro(resposta), 1)


def main():
    # TODO: Implementar os logs para envio e recebimento.
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()
        content = b""
        i = 1
        reenvio = False

        while True:
            try:
                ocioso = True
                timer1 = time.time()
                if not reenvio:
                    timer2 = time.time()
                rxBufferHeader, nRx = com1.getData(10, timer1, timer2)

                while ocioso:
                    print("entrou no ocioso!")
                    if rxBufferHeader[0] == para_inteiro(TIPO_1):
                        ocioso = False
                        # Potencial de bug, mudar no cliente para o payload de fato ter tamanho 0.
                        message_size = 0
                        escreve_log(ARQUIVO_LOG, "recebimento", 1, 1)
                        # Essa var parece nao ter uso.
                        client = rxBufferHeader[5]
                    elif rxBufferHeader[0] == para_inteiro(TIPO_3):
                        message_size = rxBufferHeader[5]
                        escreve_log(ARQUIVO_LOG, "recebimento", 3, 1)
                        ocioso = False
                # time.sleep(1)
                size = rxBufferHeader[3]
                info, _ = com1.getData(message_size, timer1, timer2)
                final, _ = com1.getData(4, timer1, timer2)
                # Condicao para finalizacao do loop
                if i == size:
                    with open("img/icon.png", "wb") as img:
                        img.write(content)
                    print("Receba!!!! Graças a deus, SIUUUUU!!!")
                    break
                if rxBufferHeader[0] == para_inteiro(TIPO_1):
                    resposta(com1, TIPO_2)
                    ocioso = True
                elif rxBufferHeader[0] == para_inteiro(TIPO_3):
                    pacote_certo = rxBufferHeader[4] == i
                    if bytes_to_list(final) == bytes_to_list(EOP) and pacote_certo:
                        content += info
                        i += 1
                        resposta(com1, TIPO_4, i)
                        print("uma resposta recebida")
                    else:
                        if not pacote_certo:
                            print("Numero do pacote errado, reenviando.")
                        if com1.rx.getBufferLen() > 0:
                            print("Tamanho payload informado errado")
                        com1.rx.clearBuffer()
                        resposta(com1, TIPO_6, i)
                    ocioso = True
            except Timer1Error:
                print("Excedeu o tempo do timer 1")
                resposta(com1, TIPO_4, i)
                reenvio = True
            except Timer2Error:
                print("Excedeu o tempo do timer 2, finalizando o programa")
                ocioso = True
                resposta(com1, TIPO_5, i)
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
