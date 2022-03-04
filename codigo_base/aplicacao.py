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
from random import randint
from datagrama import monta_header, monta_pacote

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"  # Windows(variacao de)

DADOS = b"\x01"
COMANDOS = b"\x02"
IPV4 = b"\x01"
IPV6 = b"\x02"
PC_RICARDO = b"\x01"
PC_FONTANA = b"\x02"
EOP = b"\xFF\xFF\xFF\xFF"


def handshake(com1):
    mensagem = bytes("vivo?", "utf-8")

    header = monta_header(
        DADOS,
        IPV6,
        b"\x01",
        int.to_bytes(len(mensagem), "big"),
        PC_FONTANA,
        PC_RICARDO,
        b"\x01",
        b"\x00\x00\x00",
    )
    while True:
        try:
            com1.sendData(np.asarray(header))
            com1.sendData(np.asarray(mensagem))
            com1.sendData(np.asarray(EOP))
            rxBuffer, _ = com1.getData(10)

            break
        except TimeoutError:
            resposta = input("Servidor inativo. Tentar novamente? S/N")
            if resposta == "N":
                break


def main():
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace("COM3")

        # Ativa comunicacao. Inicia os threads e a comunicação serial
        com1.enable()
        # Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.

        # aqui você deverá gerar os dados a serem transmitidos.
        # seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o
        # nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.

        handshake(com1)

        # faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.

        # finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        # faça um print para avisar que a transmissão vai começar.
        # tente entender como o método send funciona!
        # Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!

        # Manda uma mensagem para avisar o servidor que acabou a transmissao

        print("Terminou a transmissao")
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus()
        # Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        # Observe o que faz a rotina dentro do thread RX
        # print um aviso de que a recepção vai começar.

        # Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        # Veja o que faz a funcao do enlaceRX  getBufferLen

        # acesso aos bytes recebidos

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
