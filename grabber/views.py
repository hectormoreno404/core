"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from flask_mysqldb import MySQL
from grabber import app
import requests
import time
import json
import os
import datetime
import threading


from ast import literal_eval
#****************************GLOBALES****************************************************

token = 'Atna|EwICIMiAP94Qse2fDllqYHpzcnMzLPxfMlIIe0jgJ96yyP2YStwEO-02O7k8Jb9Rf5q7GNNxu3CrS46AZBqaeJCpbtDgETSZ6h_CA2xZxyuGOS-Eo7f0tlu3dzgUOIQKECd0fUHeECQLNxAGd_8cl3bZnb_DJQ0s4EEXd_d81kwyQGChWFmorK8i8h7ZAM5vP3OwbjEungsczoP17nyrCLoczNSLt8HLuJ7AHqXhv9E4fnZYOvgxV80eKYpjhWKknNc4MsVn4Cacthe87hhmwDiYmxTS6w9tMmr6Li-b7RNTODmyi_LKQBFBiWGXz-Pn03nLn1do60LM89ffvodu2jHZnclob0t2ixDYqKixkZpVax79xQ'
USER_ID = 1

#***************************** CONEXION ***********************************************
app.config['MYSQL_HOST'] = '13.77.127.110'
app.config['MYSQL_USER'] = 'grabber001'
app.config['MYSQL_PASSWORD'] = '#$H.e5561699'
app.config['MYSQL_DB'] = 'main'

mysql = MySQL(app)

#***************************** FUNCIONES ***********************************************

def send_job(user_id, offer_id, area_id, time_start, time_end, surge, price, tips):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO job (user_id, offer_id, area_id, time_start, time_end, surge, price, tips, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (user_id, offer_id, area_id, time_start, time_end, surge, price, tips, status))        
    mysql.connection.commit()
    cur.close()

def get_token():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM token WHERE user_id = 1 ORDER BY id DESC LIMIT 1' )
    data = cur.fetchone()
    return data[2]
   
    
#***************************** RUTAS/VISTAS ***********************************************

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/t')
def t():
    get_token()
    return ('termino')

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == "POST":
        details = request.form
        user_id = int(details['user_id'])
        offer_id = str(details['offer_id'])
        area_id = str(details['area_id'])
        time_start = str(details['time_start'])
        time_end = str(details['time_end'])
        surge = int(details['surge'])
        price = int(details['price'])
        tips = int(details['tips'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO job (user_id, offer_id, area_id, time_start, time_end, surge, price, tips) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                    (user_id, offer_id, area_id, time_start, time_end, surge, price, tips))        
        mysql.connection.commit()        
        return 'success'
    return render_template('index.html')
i = 0
@app.route('/c')
def c():
    def contar():
        contador = 0
        while contador<100:
            contador+=1
            print('Hilo:', 
                  threading.current_thread().getName(), 
                  'con identificador:', 
                  threading.current_thread().ident,
                  'Contador:', contador)

    hilo1 = threading.Thread(target=contar)   
    hilo1.start()   
    return 'conto'



@app.route('/core')
def core():  
    captured = 0
    contador = 0 
    denied = 0
    
    while True:
        print('---------------------------------------------------------------------------------------')
        juego = time.time()
        flex_id = '47243550-728c-410f-9a45-739a84b84914'
        print(flex_id)	
        amz_t= get_token()           
        
        # calculando tiempo en ml/s 
        tempo = str(int(round(time.time() * 1000)))
        #print (tempo)

        headers = {
		    'x-amz-access-token': amz_t,
		    #'X-Amzn-RequestId': flex_id,
		    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; SM-G965U Build/PPR1.180610.011) RabbitAndroid/3.16.34.0',
		    'X-Flex-Client-Time': tempo,
		    'x-flex-instance-id': flex_id,
		    'Content-Type': 'application/json',
		    'host': 'flex-capacity-na.amazon.com',
		    'Connection': 'Keep-Alive',
		    'Accept-Encoding': 'gzip',
	    }
	    #ENVIO REQUEST
        start_time = time.time()
        r = requests.get('https://flex-capacity-na.amazon.com/GetOffersForProvider?1496f58f-ca2d-43c7-817b-ec2c3613390d&serviceAreaIds=1496f58f-ca2d-43c7-817b-ec2c3613390d&apiVersion=V2' , headers=headers)
        json_h = r.json()
        print("Tiempo get %s seconds" % round(time.time() - start_time,4))
        print (json_h)
        
        
        #if 'TokenException' in json_h['Message']:
        #    print('exeption')
        #    break
        
        if json_h['offerList'] == [] :
            print ('naranjas')		
        else:
            print("--------Bloque Encontrado------------")
            bloque = json_h['offerList']		
            t = literal_eval(str(bloque)[1:-1])            
            if t.get('startTime') < t.get('startTime')+120*60:
                if t.get('serviceAreaId') == '1496f58f-ca2d-43c7-817b-ec2c3613390d':
                    r2 = requests.post('https://flex-capacity-na.amazon.com/AcceptOffer', headers=headers , json={"__type": "AcceptOfferInput:http://internal.amazon.com/coral/com.amazon.omwbuseyservice.offers/","offerId": t.get('offerId')})
                    print(r2.text)
                    print("******Bloque Capturado yenviado a mysql*****")
                    captured = captured+1
                    print (t.get('startTime'))
                    for key in t:
                        print (key, ":", t[key])		
                    print (t.get('offerId'))
                    localtime = time.asctime( time.localtime(time.time()) )
                    print ("Local current time :", localtime)
                    status = 1
                else:
                    print('Bloque rechazado: warehouse no deseado')
                    denied = denied+1
                    status = 2
            else:                
                 print("Bloque rechazado: Inicia en menos de 2 HORAS")
                 denied = denied+1
            send_job(USER_ID, t.get('offerId'), t.get('serviceAreaId'), t.get('startTime'), t.get('endTime'), t.get('surgeMultiplier'), t.get('priceAmount'), t.get('projectedTips'), status)
            status = 0
        print ("Paquete #", contador)
        print ("Bloques rechazados ", denied)
        print ("Bloques captudados ", captured)
        contador = contador+1
        print("Tiempo juego %s seconds" % round(time.time() - start_time,4))

    return 'termino'


@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index2.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
