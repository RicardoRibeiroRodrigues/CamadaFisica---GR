def para_inteiro(byte):
    return int.from_bytes(byte, "big")


def bytes_to_list(byte_string):
    return [byte for byte in byte_string]
