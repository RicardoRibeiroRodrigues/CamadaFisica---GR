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

int sw_uart_send_byte(due_sw_uart *uart, unsigned int letter)
{
  digitalWrite(uart->pin_rx, HIGH);

  // Start bit
  digitalWrite(uart->pin_rx, LOW);

  // Array of bits of the letter
  unsigned int *bits = loop_over_int(letter);

    _sw_uart_wait_half_T(uart);
  // Start sending data
  for (int i = 0; i < uart->databits; i++)
  {
    digitalWrite(uart->pin_rx, *(bits + i));
    _sw_uart_wait_T(uart);
  }

  int even_parity = calc_even_parity((char)letter);

  // parity
  int rx_parity = 0;
  if (uart->paritybit != SW_UART_NO_PARITY)
  {
    rx_parity = digitalRead(uart->pin_rx);
    _sw_uart_wait_T(uart);
  }

  // get stop bit
  for (int i = 0; i < uart->stopbits; i++)
  {
    if (digitalRead(uart->pin_rx) == LOW)
    {
      return SW_UART_ERROR_FRAMING;
    }
    _sw_uart_wait_T(uart);
  }

  int parity = 0;
  if (uart->paritybit == SW_UART_EVEN_PARITY)
  {
    parity = calc_even_parity(aux);
  }
  else if (uart->paritybit == SW_UART_ODD_PARITY)
  {
    parity = !calc_even_parity(aux);
  }

  if (parity != rx_parity)
  {
    return SW_UART_ERROR_PARITY;
  }

  *data = aux;
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
