# Projeto 6 - Serialização UART.

## Objetivos:
1. Produzir a serialização de um byte e enviá-lo através de 1 pino digital
qualquer de um Arduino para outro Arduino, que receberá a mensagen no padrão UART através de outro pino
digital qualquer.<br>
2. Codificar o caractere através da tabela ASCII e enviar os
bits de acordo com frame UART com 1 bit de paridade, 1 start,
1 stop bit e 9600 bits/s de 𝑏𝑎𝑢𝑑𝑟𝑎𝑡𝑒 (o código receptor está
esperando essa configuração de envio).

## Requisitos:
- 2 arduinos.
- Cabos jumper para conexões.
- 1(2) computador(es) com arduino IDE instalado.

## Montagem e execução do código:
Para rodar, conecte o pino digital 4 de um arduino (receptor) ao pino digital 3 de outro (emissor), e conecte um GND no outro.        
Em seguida, envie os códigos para os arduinos e modifique a mensagem no [TX](https://github.com/RicardoRibeiroRodrigues/CamadaFisicaGR/blob/main/projeto6/due_sw_uart_TX/due_sw_uart_TX.ino), se tudo estiver certo, você deverá ver a mensagem no monitor serial do arduino receptor.
