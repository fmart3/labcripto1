from scapy.all import IP, ICMP, sr1
import time

def enviar_stealth_icmp(destino, mensaje):
    print(f"\n[+] Enviando mensaje oculto a {destino} en paquetes ICMP...")

    for i, caracter in enumerate(mensaje):
        paquete = IP(dst=destino)/ICMP(type=8)/caracter  # Echo Request con un solo caracter como data
        respuesta = sr1(paquete, timeout=1, verbose=0)
        print(f"Paquete {i+1}: enviado caracter '{caracter}'")
        time.sleep(0.3)  # retraso entre paquetes para parecer tráfico natural

    # Último paquete con '+' como señal de fin
    paquete_final = IP(dst=destino)/ICMP(type=8)/'+'
    sr1(paquete_final, timeout=1, verbose=0)
    print("Paquete final enviado con '+' para indicar fin del mensaje.")

# Mostrar un ping normal para comparar
def ping_normal(destino):
    print(f"[+] Enviando ping normal a {destino} para comparación...")
    respuesta = sr1(IP(dst=destino)/ICMP(), timeout=1, verbose=0)
    if respuesta:
        respuesta.show()
    else:
        print("No hubo respuesta al ping normal.")

# MAIN
if __name__ == "__main__":
    destino = input("IP de destino: ")
    mensaje = input("Mensaje a enviar: ")

    ping_normal(destino)
    enviar_stealth_icmp(destino, mensaje)
