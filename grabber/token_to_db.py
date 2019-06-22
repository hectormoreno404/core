import mysql.connector

mydb = mysql.connector.connect( host="13.77.127.110", user="grabber001", passwd="#$H.e5561699", database="main")
mycursor = mydb.cursor()
user_id=1
token ='test'
time_in='test'
mycursor.execute("INSERT INTO token(user_id, token, time_in) VALUES (%s, %s, %s)", (user_id, token, time_in))

mydb.commit()

print(mycursor.rowcount, "record inserted.")