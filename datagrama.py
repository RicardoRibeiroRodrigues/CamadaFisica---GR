import numpy as np
import time


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
EOP = b"\xAA\xBB\xCC\xDD"


def monta_header(tipo_pacote, h1, h2, total_pacotes, n_pacote, h5, h7, h8, h9):
    """
    Parametros:
        tipo_pacote(byte): Tipo de pacote (dados, comando etc.).
        versao(byte): Versão (IPv4, IPv6).
        n_pacote(byte): Número do pacote (incremental durante a transmissão).
        tamanho_payload(byte): Tamanho do dado que o pacote pode transmitir.
        desitino(byte): O destinatário da mensagem.
        origem(byte): Quem manda a mensagem.
        n_pacotes(bytes): numero de pacotes da mensagem inteira.
        etc(byte): (?)
    """
    return (
        tipo_pacote
        + versao
        + n_pacote
        + tamanho_payload
        + destino
        + origem
        + n_pacotes
        + etc
    )


class Pacote:
    def __init__(self, header, payload, com1) -> None:
        self.tipo_msg = header[0]
        self.total_pacotes = header[3]
        self.n_pacote = header[4]
        self.h5 = header[5]
        self.pacote_recomeco = header[6]
        self.sucesso_anterior = header[7]
        self.h89 = header[8:10]
        self.pacote = header + payload + EOP
        self.com1 = com1

    def envia(self):
        self.com1.sendData(np.asarray(self.pacote))
        time.sleep(0.01)
