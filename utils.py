from datetime import datetime


def para_inteiro(byte):
    return int.from_bytes(byte, "big")


def bytes_to_list(byte_string):
    return [byte for byte in byte_string]


def escreve_log(
    arquivo: str,
    io: str,
    tipo: int,
    tamanho_bytes: int,
    pacote_enviado: int = None,
    total_pacotes: int = None,
):
    """
    Função com o objetivo de fazer os logs para cada uma das operações da transmissão.

    Parâmetros:
        arquivo(str): Nome do arquivo (dentro da pasta logs) em que o log será escrito.
        io (str): String indirando que operação está sendo feita (Envio, recebimento ou reenvio)
        tipo (int): Número do tipo do pacote.
        tamanho_bytes (int): Número do tamanho total da mensagem.
        pacote_enviado (int): Número do pacote (incremental durante a transmissão).
        total_pacotes (int): Número total de pacotes da transmissão atual.
    """
    if not pacote_enviado:
        pacote_enviado = ""
    if not total_pacotes:
        total_pacotes = ""

    with open(f"logs/{arquivo}", "a") as file:
        conteudo = f"{datetime.now()} /{io}/Tipo{tipo}/{tamanho_bytes}/{pacote_enviado}/{total_pacotes} \n"
        file.write(conteudo)
