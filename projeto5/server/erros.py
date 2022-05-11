# Implementar aqui os erros personalizados.
class Timer1Error(Exception):
    """
    Erro para quando o tempo de espera por uma mensagem do client é maior que 2 segundos.
    """

    def __init__(
        self, mensagem="Cliente demorou mais do que o esperado no timer 1"
    ) -> None:
        self.mensagem = mensagem
        super().__init__(self.mensagem)


class Timer2Error(Exception):
    """
    Erro para quando o tempo de espera por uma mensagem do client é maior que 20 segundos.
    """

    def __init__(
        self, mensagem="Client demorou mais que o esperado no timer 2"
    ) -> None:
        self.mensagem = mensagem
        super().__init__(mensagem)
