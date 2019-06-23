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

token = 'Atna|EwICIDakGgE_Cjjavt3p3RHdHbKWHhD-D2F0xYj8ws9l-N73nGSpBxz6HAlGhtBOMed_eAxAhnIoU86IPbfo_HGLX2g9MXI7-swkfKgKUWmfMiSES7bVdAEZ50_a3n7KMZQ2edgmrbWDQuYOmjUBW__qo48H88d4ota8x2MAC5Hy09A6WmeszycC7FHp0ff3KuCcqY0DSoU2xVFWa_W-PAbQuFh0m6HDC4EhuQMY5sfT3kGEBEj_OGC9ta12coo2ONgUEIOYKs0bWjHDOQHx_xruKmQziwLFjbZI-jQtI-GVMjMbky37VXUBMlAjmLxvDOEnjZOgtDWis8pQiHo3_WrIL-WKoNxWjLWuyJoL7V-a8yqJbA'


#***************************** CONEXION ***********************************************
app.config['MYSQL_HOST'] = '13.77.127.110'
app.config['MYSQL_USER'] = 'grabber001'
app.config['MYSQL_PASSWORD'] = '#$H.e5561699'
app.config['MYSQL_DB'] = 'main'

mysql = MySQL(app)

#***************************** FUNCIONES ***********************************************

def send_job(user_id,offer_id,area_id,time_start,time_end,surge,price,tips,	service_type):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO job (user_id, offer_id, area_id, time_start, time_end, surge, price, tips) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                (user_id, offer_id, area_id, time_start, time_end, surge, price, tips))        
    mysql.connection.commit()
    cur.close()

   
    
#***************************** RUTAS/VISTAS ***********************************************

@app.route('/')
def index():
     return render_template('index.html')

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
    contador = 0 
    denied = 0
    while True:
        print('---------------------------------------------------------------------------------------')            
        flex_id = '47243550-728c-410f-9a45-739a84b84914'
        print(flex_id)	
        amz_t= token           
        
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
        print("--- %s seconds ---" % round(time.time() - start_time,4))
        print (json_h)

        if json_h['offerList'] == [] :
            print ('naranjas')		
        else:
            print("--------Bloque Encontrado------------")
            bloque = json_h['offerList']		
            t = literal_eval(str(bloque)[1:-1])	

            #user_id, offer_id, area_id, time_start, time_end, surge, price, tips, service_type
            #send_job(1,t.get('offerId'),t.get('serviceAreaId'),t.get('startTime'),t.get('endTime'),t.get('surgeMultiplier'),t.get('priceAmount'),t.get('projectedTips'),t.get('serviceTypeId'))
            print('enviado a sql')
            break
		    # rechazar bloques para hoy

		    #time_now = date.today()
	        #print (time_now.timestamp())
	        #time_min = time_now.replace(day=time_now.day + 1, hour=0)
	        #print (time_min.timestamp())
           
	    #print(r.headers)
        #time.sleep(0.1)
	    #os.system('clear')
        print ("Paquete #", contador)
        contador = contador+1 

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
