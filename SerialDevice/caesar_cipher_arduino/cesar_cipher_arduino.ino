#include <string.h>

const int BAUD_RATE = 9600;

String caesarCifrar(String mensaje, int desplazamiento) {
  String resultado = "";
  
  for (unsigned int i = 0; i < mensaje.length(); i++) {
    char c = mensaje[i];
    
    if ((c & 0xC0) == 0xC0) { 
      resultado += c; 
      i++;
      while (i < mensaje.length() && (mensaje[i] & 0xC0) == 0x80) {
        resultado += mensaje[i];
        i++;
      }
      i--;
    }
    else if (isUpperCase(c)) {
      resultado += (char)((c - 'A' + desplazamiento + 26) % 26 + 'A');
    } else if (isLowerCase(c)) {
      resultado += (char)((c - 'a' + desplazamiento + 26) % 26 + 'a');
    } else {
      resultado += c; 
    }
  }
  return resultado;
}

void setup() {
  Serial.begin(BAUD_RATE);
  while (!Serial); 
  
  Serial.println("Sistema de Cifrado Cesar (UTF-8)");
  Serial.println("Mensaje con formato: clave:mensaje");
  Serial.println("Ejemplo: 3:Hello");
  Serial.println("-----------------------------");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    
    int separator = input.indexOf(':');
    
    if (separator != -1) {
      String claveStr = input.substring(0, separator);
      String mensaje = input.substring(separator + 1);
      
      int clave = claveStr.toInt();
      String cifrado = caesarCifrar(mensaje, clave);
      
      Serial.print("Original: ");
      Serial.println(mensaje);
      Serial.print("Cifrado: ");
      Serial.println(cifrado);
      Serial.println("-----------------------------");
    } else {
      Serial.println("Error: Formato incorrecto. Use clave:mensaje");
    }
  }
}