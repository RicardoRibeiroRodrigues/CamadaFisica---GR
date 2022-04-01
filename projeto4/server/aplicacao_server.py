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
from utils import bytes_to_list, para_inteiro

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyACM0"  # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM6"  # Windows(variacao de)

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


def resposta(com1, head, resposta, n_pacote=1):

    n_pacote = n_pacote.to_bytes(1, byteorder="big")
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
    pacote = header + b"\x00" + EOP
    com1.sendData(np.asarray(pacote))
    time.sleep(0.01)


def main():
    # TODO: Implementar os logs para envio e recebimento.
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()
        content = b""

        while True:
            ocioso = True

            rxBufferHeader, nRx = com1.getData(10)
            i = 1
            while ocioso:
                # NOTE: Acho que esse loop é desnecessario e perigoso pro programa, cria risco de loop infinito
                if rxBufferHeader[0] == para_inteiro(TIPO_1):
                    ocioso = False
                    message_size = 0
                    client = rxBufferHeader[5]
                elif rxBufferHeader[0] == para_inteiro(TIPO_3):
                    message_size = rxBufferHeader[5]
                    ocioso = False
            # Podiamos fazer do nosso jeito, com os erros msm
            # time.sleep(1)
            size = rxBufferHeader[3]
            info, _ = com1.getData(message_size)
            final, _ = com1.getData(4)
            # Condicao para finalizacao do loop
            if i == size:
                with open("img/icon.png", "wb") as img:
                    img.write(content)
                print("Receba!!!! Graças a deus, SIUUUUU!!!")
                break
            if rxBufferHeader[0] == para_inteiro(TIPO_1):
                resposta(com1, rxBufferHeader, TIPO_2)
                ocioso = True
            elif rxBufferHeader[0] == para_inteiro(TIPO_3):
                pacote_certo = rxBufferHeader[4] == i
                # NOTE: Acho que esse if quebra o programa um pouco, se entrar nesse, nao entra no else
                # e consequentemente nao trata o problema de pacote incorreto.
                if not pacote_certo:
                    print(
                        "O número do pacote está incorreto, reenviando número do pacote correto!"
                    )
                if bytes_to_list(final) == bytes_to_list(EOP) and pacote_certo:
                    content += info
                    i += 1
                    # NOTE: Oq seria o head na funcao resposta, e pq nao esta sendo usado ? -> nesse caso causa erro
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
    # TODO: Implementar os diferentes tipos de timeout para todos os timers propostos no fluxograma.
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
