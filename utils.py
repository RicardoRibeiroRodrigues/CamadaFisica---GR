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
    if not pacote_enviado:
        pacote_enviado = ""
    if not total_pacotes:
        total_pacotes = ""

    with open(f"logs/{arquivo}", "a") as file:
        conteudo = f"{datetime.now()} /{io}/{tipo}/{tamanho_bytes}/{pacote_enviado}/{total_pacotes} \n"
        file.write(conteudo)
