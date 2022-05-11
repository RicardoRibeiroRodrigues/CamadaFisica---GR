#include "sw_uart.h"
#pragma GCC optimize("-O3")

void sw_uart_setup(due_sw_uart *uart, int rx, int stopbits, int databits, int paritybit)
{

  uart->pin_rx = rx;
  uart->stopbits = stopbits;
  uart->paritybit = paritybit;
  uart->databits = databits;
  pinMode(rx, OUTPUT);
}

int calc_even_parity(char data)
{
  int ones = 0;

  for (int i = 0; i < 8; i++)
  {
    ones += (data >> i) & 0x01;
  }

  return ones % 2;
}

unsigned int *loop_over_int(due_sw_uart *uart, unsigned int number)
{
  static unsigned int bits[8];
  int i = 0;
  while (number != 0)
  {
    unsigned int bit = number & 1;
    bits[i] = bit;
    number >>= 1;
    i++;
  }
  while (i < uart->databits)
  {
    bits[i] = 0;
    i++;
  }
  return bits;
}

int sw_uart_send_byte(due_sw_uart *uart, char caractere)
{
  digitalWrite(uart->pin_rx, HIGH);

  // Start bit
  digitalWrite(uart->pin_rx, LOW);

  // Converte para ascii
  unsigned int letra = (unsigned int) caractere;
  // Array of bits of the letter
  unsigned int *bits = loop_over_int(uart, letra);

    _sw_uart_wait_T(uart);
  // Start sending data
  for (int i = 0; i < uart->databits; i++)
  {
    digitalWrite(uart->pin_rx, *(bits + i));
    _sw_uart_wait_T(uart);
  }

  int even_parity = calc_even_parity(caractere);

  // parity
  if (uart->paritybit != SW_UART_NO_PARITY)
  {
    digitalWrite(uart->pin_rx, even_parity);
    _sw_uart_wait_T(uart);
  }

  // Send stop bit
  for (int i = 0; i < uart->stopbits; i++)
  {
    digitalWrite(uart->pin_rx, HIGH);
    _sw_uart_wait_T(uart);
  }

  return SW_UART_SUCCESS;
}

// MCK 21MHz
void _sw_uart_wait_half_T(due_sw_uart *uart)
{
  for (int i = 0; i < 1093; i++)
    asm("NOP");
}

void _sw_uart_wait_T(due_sw_uart *uart)
{
  _sw_uart_wait_half_T(uart);
  _sw_uart_wait_half_T(uart);
}
