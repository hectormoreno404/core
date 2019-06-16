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

from ast import literal_eval
#***************************** CONEXION ***********************************************
app.config['MYSQL_HOST'] = '40.70.220.187'
app.config['MYSQL_USER'] = 'hector'
app.config['MYSQL_PASSWORD'] = '#$H.e5561699'
app.config['MYSQL_DB'] = 'main'

mysql = MySQL(app)

#***************************** FUNCIONES ***********************************************

def send_job(user_id,offer_id,area_id,time_start,time_end,surge,price,tips,	service_type):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO job(user_id,offer_id,area_id,time_start,time_end,surge,price,tips,	service_type) VALUES (%i, %s, %s, %s, %s, %i, %i, %s)", (user_id,offer_id,area_id,time_start,time_end,surge,price,tips,	service_type))
    




#***************************** RUTAS/VISTAS ***********************************************
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        user_id = details['user_id']
        token = details['token']
        time_in = details['time_in']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO token(user_id, token, time_in) VALUES (%s, %s, %s)", (user_id, token, time_in))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')

@app.route('/core')
def core():
    e = 0
    denied = 0
    while True:
        print('---------------------------------------------------------------------------------------')
        #print ("Flex ID:")
	    #f = open("/home/proxy/flex-id.txt", "r")
	    #flex_id = f.read().strip()
        flex_id = '47243550-728c-410f-9a45-739a84b84914'
        print(flex_id)	
        #print('Token:')
        #f = open("/home/scripts/amazon/source/amazon-token.txt", "r")
	    #amz_t = f.read().strip()
        amz_t= 'Atna|EwICIHUCaPY2WhCDyNjT63j5QGUElO98Mi6U8eHPrlT33tRMgdM-BOqZmRkhWmmtozDKDOO6qZ6TVsyvwIkYbJWFISNMz-DtJU5zBnyI8nqWxPbcyoCtEXP8lTUT12ZjREXHOADcD_MUDauxlx2AQnHqGnRSZzOv6SAjk17lkZ3UeZnVSq4Ou814zqxJSij0eMHgjC2v6lL0ZY7DrWc3uhlPl_GSILyC-4w4vvKchxb0b-5uBlP5fecQFfOoXy1UrBSSrvTVByUxmVDJ8eQpDCQu-Slh1hvhQdfjo0MwHPnoVrX-vTK9f1W0M2t4WcAse6R5Lzdt-wI4fFSB-DpqG-73N2vY03ZWc08b85BQaMqw2TmpIA'
	    #print(amz_t)
	    #print('\n')
        print("Bloquesrechazados:",denied)
        
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
        r = requests.get('https://flex-capacity-na.amazon.com/GetOffersForProvider?1496f58f-ca2d-43c7-817b-ec2c3613390d&serviceAreaIds=1496f58f-ca2d-43c7-817b-ec2c3613390d&apiVersion=V2' , headers=headers)
        json_h = r.json()
        print (json_h)

        if json_h['offerList'] == [] :
            print ('naranjas')		
        else:
            print("--------Bloque Encontrado------------")
            bloque = json_h['offerList']		
            t = literal_eval(str(bloque)[1:-1])	

            #user_id, offer_id, area_id, time_start, time_end, surge, price, tips, service_type
            send_job(1,t.get('offerId'),t.get('serviceAreaId'),t.get('startTime'),t.get('endTime'),t.get('surgeMultiplier'),t.get('priceAmount'),t.get('projectedTips'),t.get('serviceTypeId'))
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
        print ("Paquete #", e)
        e = e+1

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
