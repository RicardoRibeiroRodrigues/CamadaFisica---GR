class timer1Error(Exception):
    """Erro levantado quando o tempo de espera do RxBuffer é maior que 5 segundos"""

    def __init__(self, mensagem="Servidor demorou mais de 5 segundos para responder"):
        self.mensagem = mensagem
        super().__init__(self.mensagem)
