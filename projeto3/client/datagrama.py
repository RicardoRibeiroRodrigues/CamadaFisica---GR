EOP = b"\xFF\xFF\xFF\xFF"


def monta_header(
    tipo_pacote, versao, n_pacote, tamanho_payload, destino, origem, n_pacotes, etc
):
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
