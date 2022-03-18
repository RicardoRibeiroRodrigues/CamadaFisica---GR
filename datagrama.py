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


def monta_header(
    h0: bytes,
    h1: bytes,
    h2: bytes,
    h3: bytes,
    h4: bytes,
    h5: bytes,
    h6: bytes,
    h7: bytes,
    h8: bytes,
    h9: bytes,
):
    """
    Parametros:
        h0(byte): Tipo do pacote (dados, comando etc.).
        h1(byte): Livre.
        h2(byte): Livre.
        h3(bytes): Número de pacotes da mensagem inteira.
        h4(byte): Número do pacote (incremental durante a transmissão).
        h5(byte): Se a mensagem for do tipo HandShake, representa o id do arquivo,
        se for do tipo de dados: representa o tamanho do payload.
        h6(byte): pacote solicitado para recomeço quando a erro no envio.
        h7(byte): último pacote recebido com sucesso.
        h8(byte): CRC.
        h9(byte): CRC.
    """
    return h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9


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
