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
            print(rows)
            print("Total filas:  ", len(rows))

                #print(len(x.inserted_ids))

            
            #for j in table_slave:
                #print (j)
                #print("registration_id: ", rows[0])
                #print("sede_id: ", rows[1])
                #print("departamento_id: ", rows[2])
                #print("facultad_id: ", rows[3])
                #print("programa_id: ", rows[4])
                #print("egresado_id: ", rows[5])
                #print("date_id: ", rows[6])
                #print("\n\n")

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
    prettyprint("Error en la conexión al servidor MySQL.", MsgType.WARNING)
######################


#################################################################################
# MongoDB connection
prettyprint("Conexión al servidor MongoDB...\n", MsgType.HEADER)
###
try:
    import pymongo
    
    mongodb_host            = 'mongodb://localhost:27017'
    mongodb_dbname          = 'migrate_bda'
    n_collection            = 'graduaciones'
    #
    mymongodb               = pymongo.MongoClient(mongodb_host)
    mydb_mongodb            = mymongodb[mongodb_dbname]
    mycollection_mongodb    = mydb_mongodb[n_collection]
    #print(mymongodb, mydb_mongodb, mycollection_mongodb)
    #########################    
    prettyprint("La conexión al servidor MongoDB fue exitosa.", MsgType.OKGREEN)
    #########################
    master_table            = ['graduaciones']
    slave_table             = ['departamento', 'facultad', 'programa']
    #########################

    for i in master_table:
        mycursor = mysqldb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM "+ i +";")
        row = mycursor.fetchall()
        ##print(row)

        #for j in row: 
        for idj, j in enumerate(row):
            #print(idj)
            #print(j)
            
            for k in slave_table:
                #print(k, row[idj]["departamento_id"]) 
                #print("SELECT * FROM "+ k +" WHERE departamento_id = '"+ row[idj]["departamento_id"] +"'" )
                #print("SELECT * FROM "+ k +" ;")
                if k == 'departamento':
                    query = "SELECT * FROM " + k + " WHERE departamento_id = " + str(row[idj]["departamento_id"])
                    mycursor.execute(query)
                    row_jd = mycursor.fetchall()
                    row[idj]["departamento_id"] = row_jd

                if k == 'facultad':
                    query = "SELECT * FROM " + k + " WHERE facultad_id = " + str(row[idj]["facultad_id"])
                    mycursor.execute(query)
                    row_jf = mycursor.fetchall()
                    row[idj]["facultad_id"] = row_jf

                if k == 'programa':
                    query = "SELECT * FROM " + k + " WHERE programa_id = " + str(row[idj]["programa_id"])
                    mycursor.execute(query)
                    row_jp = mycursor.fetchall()
                    row[idj]["programa_id"] = row_jp

    ###print(row)
    mycollection_mongodb.insert_many(row)
    ################################################################
    n_collection            = 'publicaciones'
    mycollection_mongodb    = mydb_mongodb[n_collection]
    #########################    
    prettyprint("La conexión al servidor MongoDB # 2 fue exitosa.", MsgType.OKGREEN)
    #########################
    master_table            = ['publicacion']
    slave_table             = ['publicacion', 'revista']
    #########################

    for i in master_table:

        mycursor = mysqldb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM "+ i +";")
        row = mycursor.fetchall()

        #for j in row: 
        for idj, j in enumerate(row):

            mycursor.execute("SELECT * FROM registro_publicaciones rp WHERE rp.publicacion_id = " + str(row[idj]["publicacion_id"]) + ";")
            row_rp = mycursor.fetchall()
            
            if row_rp is None:
            
            else:
                for idx, x in enumerate(row_rp):
                
                    for k in slave_table:

                        if k == 'publicacion':
                            query = "SELECT * FROM " + k + " WHERE departamento_id = " + str(row_rp[idj]["departamento_id"])
                            mycursor.execute(query)
                            row_jd = mycursor.fetchall()
                            row[idj]["departamento_id"] = row_jd

                if k == 'revista':
                    query = "SELECT * FROM " + k + " WHERE facultad_id = " + str(row[idj]["facultad_id"])
                    mycursor.execute(query)
                    row_jf = mycursor.fetchall()
                    row[idj]["facultad_id"] = row_jf


    #####
    #
    #####

except:
    prettyprint("Error en la conexión al servidor MongoDB .", MsgType.WARNING)
#################################################################################


#mycursor = mysqldb.cursor(dictionary=True)
#mycursor.execute("SELECT * from warnings1")
#myresult = mycursor.fetchall()

####print(myresult)

###############################################################

##
###mongodb_host    = "mongodb://localhost:27017/"
###mongodb_dbname  = "migrate_dba"
###myclient        = pymongo.MongoClient(mongodb_host)
###mydb            = myclient[mongodb_dbname]
###mycol           = mydb["graduaciones"]
##
####if len(myresult) > 0:
    ####x = mycol.insert_many(myresult) #myresult comes from mysql cursor
    ####print(len(x.inserted_ids))


####get_value_table(mysqldb, mymongodb, table_master, table_slave, n_collection)