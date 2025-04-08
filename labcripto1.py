def cesar_cipher():
    entrada = input()
    texto, n = entrada.rsplit('"', 1)
    texto = texto.strip('"')
    desplazamiento = int(n.strip())
    resultado = ''
    for c in texto:
        if c == ' ':
            resultado += ' '
        elif c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            resultado += chr((ord(c) - base + desplazamiento) % 26 + base)
    print(resultado)
    
cesar_cipher()
