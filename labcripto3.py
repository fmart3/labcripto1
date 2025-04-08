from scapy.all import sniff, ICMP
from colorama import init, Fore

init(autoreset=True)

mensaje = ""

# ---------- Fuerza bruta de cifrado César ----------

def cesar_bruteforce(texto):
    opciones = []
    for d in range(1, 26):
        descifrado = ""
        for c in texto:
            if c.isalpha():
                ascii_offset = 65 if c.isupper() else 97
                descifrado += chr((ord(c) - ascii_offset - d) % 26 + ascii_offset)
            else:
                descifrado += c
        opciones.append((d, descifrado))
    return opciones

def puntuar(texto):
    return sum(1 for c in texto.lower() if c in "aeiou ")

def probar_todos_los_desplazamientos(texto_cifrado):
    print("\n[*] Probando todos los desplazamientos posibles:\n")
    opciones = cesar_bruteforce(texto_cifrado)
    opciones.sort(key=lambda x: -puntuar(x[1]))  # mejor puntuado al inicio

    mejor = opciones[0][1]
    for d, msg in opciones:
        if msg == mejor:
            print(Fore.GREEN + f"[+] Desplazamiento {d}: {msg}")
        else:
            print(f"[-] Desplazamiento {d}: {msg}")

# ---------- Procesamiento de paquetes ICMP ----------

def procesar_paquete(paquete):
    global mensaje
    if ICMP in paquete and paquete[ICMP].type == 8:  # Echo Request
        carga = bytes(paquete[ICMP].payload)
        if len(carga) == 1:
            char = carga.decode('utf-8', errors='ignore')
            if char.isalpha() or char == ' ':  # aceptar letras y espacios
                if char == '+':  # carácter de cierre
                    print("\n[+] Mensaje recibido (cifrado):", mensaje)
                    probar_todos_los_desplazamientos(mensaje)
                    return True
                else:
                    mensaje += char


# ---------- Iniciar escucha de red ----------

print("[*] Escuchando paquetes ICMP... Esperando mensaje oculto.")
sniff(filter="icmp", prn=procesar_paquete)
