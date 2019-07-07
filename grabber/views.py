"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from flask_mysqldb import MySQL
from grabber import app
#import requests
import time
import json
import os
import datetime
import threading
import faster_than_requests as requests
import gzip



from ast import literal_eval
#****************************GLOBALES****************************************************

token = 'Atna|EwICIP7jmXj9d03Nmmt7LtX7C3clcoyIcNRFHNqI-XIGDPnXt9_O-OUwihy_tmSTS_ApbApQhJFY-a86Yt1dSUtk6Wl9vZFPvHMgR0uGe_-c3XDI_cO_iAn2eXWhrP4qFKft1AoGb1a7dM8PyTCCUe65ZhMsrPR_XoWsnUV2YgFrTJQN4SyVckNq_yE9SXZQwovHo6EO08ApTG1SReVxBeoVDbnFdJHY4GeSCHM4QKucvVnexlzrDudVdr7q-2pbXfCiTE6NCBjXgdVXwjWWV1S7mpCE_ulYePnOTSoiNw5tIAnNFsnWsiohvtImbwWV3-lspNkkigGEWvS0isfsoDHCVKXy3Rinrc_CCwyGhotksMEIzg'
USER_ID = 1
JOBS = []

#***************************** CONEXION ***********************************************
app.config['MYSQL_HOST'] = '13.77.127.110'
app.config['MYSQL_USER'] = 'grabber001'
app.config['MYSQL_PASSWORD'] = '#$H.e5561699'
app.config['MYSQL_DB'] = 'main'

mysql = MySQL(app)

#***************************** FUNCIONES ***********************************************

def send_job(user_id, offer_id, area_id, time_start, time_end, surge, price, tips, status, times):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO job (user_id, offer_id, area_id, time_start, time_end, surge, price, tips, status , times) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (user_id, offer_id, area_id, time_start, time_end, surge, price, tips, status, times))        
    mysql.connection.commit()
    cur.close()

def add_times_last_job():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE job SET times = times +1 WHERE user_id = %s ORDER BY id DESC LIMIT 1", (USER_ID,))        
    mysql.connection.commit()
    cur.close()

def get_last_job():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM job WHERE user_id = %s ORDER BY id DESC LIMIT 1' , (USER_ID,) )
    data = cur.fetchone()
    return data[2]

def get_token():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM token WHERE user_id = %s ORDER BY id DESC LIMIT 1", (USER_ID,))
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
    
    t_ciclo = time.time()
    while True:        
        juego = time.time()
        flex_id = '47243550-728c-410f-9a45-739a84b84914'
        #print(flex_id)	
        amz_t= get_token()           
        # calculando tiempo en ml/s 
        tempo = str(int(round(time.time() * 1000)))
        #print (tempo)

       
        #print (amz_t)
        headers = [
			("x-amz-access-token", amz_t),
		    #"X-Amzn-RequestId": flex_id,
		    ("User-Agent", "Dalvik/2.1.0 (Linux; U; Android 9; SM-G965U Build/PPR1.180610.011) RabbitAndroid/3.19.38.0"),
		    ("X-Flex-Client-Time", tempo),
		    ("x-flex-instance-id", flex_id),
		    ("Content-Type", "application/json"),
		    ("host", "flex-capacity-na.amazon.com"),
		    ("Connection", "Keep-Alive"),
		    ("Accept-Encoding", "gzip")
		    ]
        
        requests.setHeaders( headers)
        get_time = time.time()
        r = requests.gets("https://flex-capacity-na.amazon.com/GetOffersForProvider?1496f58f-ca2d-43c7-817b-ec2c3613390d&serviceAreaIds=1496f58f-ca2d-43c7-817b-ec2c3613390d&apiVersion=V2")
        #r = requests.gets("https://hookb.in/jeaDbkY3XXu1012zmKE1")
        print("Tiempo GET %s seconds" % round(time.time() - get_time,4))        
        try:
            response = json.loads(r.get('body'))
        except:
            r2 = gzip.decompress(r.get('body'))
            response = json.loads(r2)

        v = response.get('offerList')
        
        if('Message' in response):
            message = response['Message']
            if ('TokenException' in message):
                print ('Token exception')
                break                
            else:
                print(message)
                break


        if len(v)> 1 :            
            for i in range(len(v)):
                print("* CAPTURANDO BLOQUE *")
                if v[i]('startTime') < v[i]('startTime')+420*60:
                    if t.get('serviceAreaId') == '1496f58f-ca2d-43c7-817b-ec2c3613390d':
                        post_time = time.time()
                        r2 = requests.posts("https://flex-capacity-na.amazon.com/AcceptOffer", """{"__type": "AcceptOfferInput:http://internal.amazon.com/coral/com.amazon.omwbuseyservice.offers/", t.get('offerId')}""")                    
                        print("Tiempo POST %s seconds" % round(time.time() - post_time,4))
                        print(r2)
                        break
                    else:
                        print('Trabajo rechazado: Warehouse')
                        break
                else:
                    print('Trabajo rechazado: Comienza pronto')
                    break
        else:
            print('naranjas')            
            contador = contador+1 
            print("Intento # %s " %contador)
            print("Tiempo Ciclo %s seconds" % round(time.time() - t_ciclo,4))
            t_ciclo = time.time()
            print('------------------------------------')
            time.sleep(0.2)
        
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

