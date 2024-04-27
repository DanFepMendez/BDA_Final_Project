##################################################################################
import mysql.connector
#######
import pymongo                  # Import MongoDB Library
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
#######
#import numpy as np 
#import pandas as pd 
#######
import decimal
import multiprocessing as mp  # Import Multiprocessing
from datetime import datetime
#######
import enum
#######
import random
##################################################################################
##################################################################################
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
####
class MsgType(enum.Enum):
    HEADER = 1
    OKBLUE = 2
    OKCYAN = 3
    OKGREEN = 4
    WARNING = 5
    FAIL = 6
    ENDC = 7
    BOLD = 8
    UNDERLINE = 9
####
##################################################################################
# Función de impresión bonita
def prettyprint(msg_text, msg_type):
    if msg_type == MsgType.HEADER:
        print(f"{bcolors.HEADER}{msg_text}{bcolors.ENDC}")
    elif msg_type == MsgType.OKBLUE:
        print(f"{bcolors.OKBLUE}{msg_text}{bcolors.ENDC}")
    elif msg_type == MsgType.OKCYAN:
        print(f"{bcolors.OKCYAN}{msg_text}{bcolors.ENDC}")
    elif msg_type == MsgType.OKGREEN:
        print(f"{bcolors.OKGREEN}{msg_text}{bcolors.ENDC}")
    elif msg_type == MsgType.WARNING:
        print(f"{bcolors.WARNING}{msg_text}{bcolors.ENDC}")
    elif msg_type == MsgType.FAIL:
        print(f"{bcolors.FAIL}{msg_text}{bcolors.ENDC}")
    elif msg_type == MsgType.BOLD:
        print(f"{bcolors.BOLD}{msg_text}{bcolors.ENDC}")
    elif msg_type == MsgType.UNDERLINE:
        print(f"{bcolors.UNDERLINE}{msg_text}{bcolors.ENDC}")
####
def get_value_table(mysqldb, mongodb_host, mongodb_dbname, n_collection, master_table, slave_table):
    ####
    try:
        print(f"SiOk1")
        ######
        ######
        ######
        for i in master_table:
            print(i)
            mycursor = mysqldb.cursor(dictionary=True)
            mycursor.execute("SELECT * FROM `"+ i +"`;")
            rows = mycursor.fetchall()

        #
        mymongodb               = pymongo.MongoClient(mongodb_host)
        mydb_mongodb            = mymongodb[mongodb_dbname]
        mycollection_mongodb    = mydb_mongodb[n_collection]
        print(mymongodb, mydb_mongodb, mycollection_mongodb)

        if len(rows) > 0:
            #print("Detalle: ", len(rows))
            mycollection_mongodb.insert_many(rows) # myresult comes from mysql cursor
                

    except:
        print(f"NoOk!")

###############################################################



###############################################################

# MySQL connection
prettyprint("Conexión al servidor MySQL...", MsgType.HEADER)
###
try:
    mysqldb = mysql.connector.connect(  host="localhost",
                                        database="project_star_model",
                                        user="root",
                                        password="superman"
                                    )
    #mycursor = mysqldb.cursor(dictionary=True)
    prettyprint("La conexión al servidor MySQL fue exitosa.", MsgType.OKGREEN)

except:
    prettyprint("Error en la conexión al servidor MySQL.\n\n", MsgType.WARNING)
######################


#################################################################################
# MongoDB connection
prettyprint("Conexión al servidor MongoDB...\n", MsgType.HEADER)
###
    
mongodb_host            = 'mongodb://localhost:27017'
mongodb_dbname          = 'migrate_bda'
n_collection            = 'publicaciones'
#
mymongodb               = pymongo.MongoClient(mongodb_host)
mydb_mongodb            = mymongodb[mongodb_dbname]
mycollection_mongodb    = mydb_mongodb[n_collection]
#print(mymongodb, mydb_mongodb, mycollection_mongodb)
#########################    
prettyprint("La conexión al servidor MongoDB fue exitosa.", MsgType.OKGREEN)
#########################

master_table            = ['publicacion']
slave_table             = ['institucion', 'revista', 'publicacion', 'sede_universidad']
master_table            = ['registro_publicaciones']
#########################

mycursor = mysqldb.cursor(dictionary=True)

for i in master_table:
    mycursor.execute("SELECT * FROM "+ i +";")
    row = mycursor.fetchall()        
    #print(row)
    
    for idj, j in enumerate(row):

        #print(idj) ### Corresponde al ID
        #print(j) ### Corresponde al Arreglo
        #print(j["revista_id"]) ### Corresponde al Valor del arreglo

        #print ( str(row["revista_id"]) )
        #print ( str(row[idj]["revista_id"]) )
        #print ("SELECT * FROM revista WHERE institucion_id = " + str(row[idj]["revista_id"]) )
        
        if j["egresado_id"] is not None:
            a = ["AMAZONIA", "CARIBE", "BOGOTÁ", "MANIZALES", "MEDELLÍN", "ORINOQUIA", "PALMIRA", "TUMACO Y DE LA PAZ"]
            row[idj]["egresado_id"] = {"egresado_id": j["egresado_id"], "sede_nombre": random.choice(a)}
        
        for h in slave_table:
            #print(h)
            if h == 'institucion':
                query = "SELECT * FROM " + h + " WHERE institucion_id = %s ;"
                if j["institucion_id"] is not None:
                    v_query = (j["institucion_id"],)
                    mycursor.execute(query, v_query)
                    row_ji = mycursor.fetchall()
                    row[idj]["institucion_id"] = row_ji[0]
                else:
                    row[idj]["institucion_id"] = None

            if h == 'revista':
                query = "SELECT * FROM " + h + " WHERE revista_id = %s ;"
                if j["revista_id"] is not None:
                    v_query = (j["revista_id"],)
                    mycursor.execute(query, v_query)
                    row_jr = mycursor.fetchall()
                    row[idj]["revista_id"] = row_jr[0]
                else:
                    row[idj]["revista_id"] = None

            if h == 'publicacion':
                query = "SELECT * FROM " + h + " WHERE publicacion_id = %s ;"

                if j["publicacion_id"] is not None:
                    v_query = (j["publicacion_id"],)
                    mycursor.execute(query, v_query)
                    row_jp = mycursor.fetchall()
                    row[idj]["publicacion_id"] = row_jp[0]
                else:
                    row[idj]["publicacion_id"] = None

            ####if h == 'sede_universidad':
                #SELECT DISTINCT `rp`.`egresado_id`, `su`.`sede_nombre` FROM `sede_universidad` `su` INNER JOIN `graduaciones` `g` ON `su`.`sede_id` = `g`.`sede_id` INNER JOIN `egresado` `e` ON `e`.`egresado_id` = `g`.`egresado_id` INNER JOIN `registro_publicaciones` `rp` ON `e`.`egresado_id` = `rp`.`egresado_id` WHERE `rp`.`egresado_id` = 
                ####query = "SELECT DISTINCT `rp`.`egresado_id`, `su`.`sede_nombre` FROM `" + h + "` `su` INNER JOIN `graduaciones` `g` ON `su`.`sede_id` = `g`.`sede_id` INNER JOIN `egresado` `e` ON `e`.`egresado_id` = `g`.`egresado_id` INNER JOIN `registro_publicaciones` `rp` ON `e`.`egresado_id` = `rp`.`egresado_id` WHERE `rp`.`egresado_id` = %s LIMIT 1 ;"
                ##print(query)
                ####if j["egresado_id"] is not None:
                    ####v_query = (j["egresado_id"],)
                    ####mycursor.execute(query, v_query)
                    ####row_jee = mycursor.fetchall()
                    ####print(row_jee)
                    ####row[idj]["egresado_id"] = row_jee
                ####else:
                    ####row[idj]["egresado_id"] = None


#mycollection_mongodb.insert_many(row)

# 
#print(row)
#print(row)
#mycollection_mongodb.insert_many(row_jp)
################################################################
################################################################
#mongodb_host            = 'mongodb://localhost:27017'
#mongodb_dbname          = 'migrate_bda'
#n_collection            = 'publicaciones'
#
#mymongodb               = pymongo.MongoClient(mongodb_host)
#mydb_mongodb            = mymongodb[mongodb_dbname]
#mycollection_mongodb    = mydb_mongodb[n_collection]
#########################    
#####mycollection_mongodb.insert_many(row)

#########################    
prettyprint("La conexión al servidor MongoDB # 1 fue exitosa y se insertaron los datos.", MsgType.OKGREEN)



#################################################################################

#print ( row[0] )
#print(row)

if len(row) > 0:
    print("Detalle: ", len(row))
    mycollection_mongodb.insert_many(row) # myresult comes from mysql cursor

###############################################################
