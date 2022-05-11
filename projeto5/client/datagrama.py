import numpy as np
import time
from crc import CrcCalculator, Crc16
from utils import para_inteiro, escreve_log, ARQUIVO_LOG


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


class Datagrama:
    # Tipos de pacote -> Constates do datagrama.
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
    # Fim do pacote
    EOP = b"\xAA\xBB\xCC\xDD"

    def __init__(
        self,
        tipo_msg,
        n_pacotes,
        n_pacote,
        tamanho_id,
        pac_solicitado,
        ultimo_pac,
        crc_check: int = None,
    ) -> None:
        self.tipo = tipo_msg
        self.n_pacotes = n_pacotes
        self.n_pacote = n_pacote
        self.tamanho_id = tamanho_id
        self.pac_solicitado = pac_solicitado
        self.ultimo_pac = ultimo_pac
        self.crc_calculator = CrcCalculator(Crc16.CCITT)
        if crc_check:
            self.crc_check = crc_check

    def monta_header(self, crc_result: int) -> bytes:
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
        h0 = (self.tipo).to_bytes(1, "big")
        h3 = (self.n_pacotes).to_bytes(1, "big")
        h4 = (self.n_pacote).to_bytes(1, "big")
        h5 = (self.tamanho_id).to_bytes(1, "big")
        h6 = (self.pac_solicitado).to_bytes(1, "big")
        h7 = (self.ultimo_pac).to_bytes(1, "big")
        h8_9 = crc_result.to_bytes(2, "big")
        return h0 + b"\x00\x00" + h3 + h4 + h5 + h6 + h7 + h8_9

    @classmethod
    def from_bytes(cls, bytes: bytes) -> "Datagrama":
        return cls(
            bytes[0],
            bytes[3],
            bytes[4],
            bytes[5],
            bytes[6],
            bytes[7],
            crc_check=bytes[8:],
        )

    def send_msg(self, com1, payload="") -> None:
        if payload:
            # Faz a verificação com o crc
            checksum = self.crc_calculator.calculate_checksum(payload)
            # para segunda parte da entrega.
            # checksum = 0

            pacote = self.monta_header(checksum) + payload + self.EOP
        else:
            pacote = self.monta_header(0) + self.EOP

        escreve_log(
            ARQUIVO_LOG,
            "envio",
            self.tipo,
            len(payload) + 14,
            self.n_pacote,
            self.n_pacotes,
        )
        com1.sendData(np.asarray(pacote))
        time.sleep(0.01)

    def is_same_package(self, i: int) -> bool:
        return self.n_pacote == i

    def is_confirmation(self) -> bool:
        return self.tipo == para_inteiro(self.TIPO_4)

    def is_error(self) -> bool:
        return self.tipo == para_inteiro(self.TIPO_6)
