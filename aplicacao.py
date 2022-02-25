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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"  # Windows(variacao de)


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

        # Cria a lista de comandos a ser enviado (Client side)
        COMANDO_1 = b"\x00\xFF\x00\xFF"
        COMANDO_2 = b"\x00\xFF\xFF\x00"
        COMANDO_3 = b"\xFF"
        COMANDO_4 = b"\x00"
        COMANDO_5 = b"\xFF\x00"
        COMANDO_6 = b"\x00\xFF"

        LISTA_TODOS_COMANDOS = [
            COMANDO_1,
            COMANDO_2,
            COMANDO_3,
            COMANDO_4,
            COMANDO_5,
            COMANDO_6,
        ]

        n_comandos = randint(10, 30)

        lista_comandos = [
            LISTA_TODOS_COMANDOS[randint(0, 5)] for _ in range(n_comandos)
        ]

        # faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.

        # finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        # faça um print para avisar que a transmissão vai começar.
        # tente entender como o método send funciona!
        # Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
        i = 1
        COMANDO_OK = b"\x10"
        for comando in lista_comandos:
            # Primeiro manda uma mensagem avisando o tamanho do comando
            com1.sendData(np.asarray(len(comando).to_bytes(1, byteorder="big")))

            time.sleep(0.01)

            rxBuffer, _ = com1.getData(1)
            print("Servidor recebeu!")
            if rxBuffer != COMANDO_OK:
                break

            # Em seguida, o comando em si
            print(f"COMANDO({i}) ENVIADO: {comando}")
            com1.sendData(np.asarray(comando))

            time.sleep(0.01)

            rxBuffer, _ = com1.getData(1)
            print("Servidor recebeu!")
            if rxBuffer != COMANDO_OK:
                break

            i += 1
            # rxBuffer, nRx = com1.getData(len(comando))

            # print(f"Enviado: {comando}, Recebido {rxBuffer}")

        # Manda uma mensagem para avisar o servidor que acabou a transmissao
        COMANDO_FIM = b"\x11"
        com1.sendData(np.asarray(COMANDO_FIM))

        # Recebe a resposta do numero de comandos pelo servidor
        rxBuffer, _ = com1.getData(1)
        n_comandos = int.from_bytes(rxBuffer, "big")
        print(
            f"O servidor recebeu {n_comandos}, foi a quantidade certa? {'Sim' if n_comandos == len(lista_comandos) else 'Não'}"
        )

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
        print(f"Tamanho da mensagem: {len(lista_comandos)}")
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
