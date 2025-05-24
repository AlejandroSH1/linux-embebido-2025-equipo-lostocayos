BAUD_RATE = 9600

def caesar_cifrar(mensaje, desplazamiento):
    resultado = ""
    i = 0
    while i < len(mensaje):
        c = mensaje[i]
        
        # Manejo de caracteres UTF-8 (bytes adicionales)
        if (ord(c) & 0xC0) == 0xC0:
            resultado += c
            i += 1
            while i < len(mensaje) and (ord(mensaje[i]) & 0xC0) == 0x80:
                resultado += mensaje[i]
                i += 1
            continue
        elif c.isupper():
            resultado += chr((ord(c) - ord('A') + desplazamiento + 26) % 26 + ord('A'))
        elif c.islower():
            resultado += chr((ord(c) - ord('a') + desplazamiento + 26) % 26 + ord('a'))
        else:
            resultado += c
        i += 1
    return resultado

def main():
    print("Sistema de Cifrado Cesar (UTF-8)")
    print("Mensaje con formato: clave:mensaje")
    print("Ejemplo: 3:Hello")
    print("-----------------------------")
    
    while True:
        try:
            input_str = input().strip()
            if not input_str:
                continue
                
            separator = input_str.find(':')
            
            if separator != -1:
                clave_str = input_str[:separator]
                mensaje = input_str[separator+1:]
                
                try:
                    clave = int(clave_str)
                    cifrado = caesar_cifrar(mensaje, clave)
                    
                    print(f"Original: {mensaje}")
                    print(f"Cifrado: {cifrado}")
                    print("-----------------------------")
                except ValueError:
                    print("Error: La clave debe ser un número entero")
            else:
                print("Error: Formato incorrecto. Use clave:mensaje")
        except KeyboardInterrupt:
            print("\nSaliendo del programa...")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()