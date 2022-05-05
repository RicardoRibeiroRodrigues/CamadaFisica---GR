#include "sw_uart.h"

due_sw_uart uart;

void setup() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 3, 1, 8, SW_UART_EVEN_PARITY);
  pinMode(3, OUTPUT);
}

void loop() {
 send_byte();
// envio();
 delay(4000);
}


void send_byte() {
  char data;
  String mensagem = "Boa tarde Carareto, quero nosso 10";
  int i = 0;
  while (i < mensagem.length()){
    data = mensagem[i];
    String printMsg = String("Caractere enviado: " + String(data));
    Serial.println(printMsg);
    int code = sw_uart_send_byte(&uart, data);
    if(code == SW_UART_SUCCESS) {
       Serial.print("Sucesso\n");
       i++;
    } else if(code == SW_UART_ERROR_PARITY) {
      Serial.println("\nPARITY ERROR");
    } else {
      Serial.println("\nOTHER");
      Serial.print(code);
    }
    delay(50);
  }
  // Ultimo byte para sinalizar que a string acabou
  int code = sw_uart_send_byte(&uart, '\0');
}

void envio()
{
    digitalWrite(3, LOW);
    _sw_uart_wait_T(&uart);
    digitalWrite(3, HIGH);
    _sw_uart_wait_T(&uart);
    digitalWrite(3, LOW);
    _sw_uart_wait_T(&uart);
    digitalWrite(3, HIGH);
    _sw_uart_wait_T(&uart);
    digitalWrite(3, LOW);
    _sw_uart_wait_T(&uart);
    digitalWrite(3, LOW);
    _sw_uart_wait_T(&uart);
    digitalWrite(3, HIGH);
    _sw_uart_wait_T(&uart);
    digitalWrite(3, LOW);
    _sw_uart_wait_T(&uart);
    digitalWrite(3, LOW);
    _sw_uart_wait_T(&uart);
    digitalWrite(3, HIGH);
    _sw_uart_wait_T(&uart);
    digitalWrite(3, HIGH);
    _sw_uart_wait_T(&uart);
}
