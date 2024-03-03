import time, re, os
from datetime import timedelta, date
import mysql.connector
from mysql.connector import Error

# Funcion para ejecutar archivo sql desde python

def exec_sql_file(cursor, sql_file):
    sql_file = os.path.join(os.path.dirname(__file__), sql_file)
    print ("\n[INFO] Executing SQL script file: %s",sql_file)
    statement = ""

    for line in open(sql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r';$', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            #print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
            try:
                cursor.execute(statement)
            except (Error) as e:
                print("\n[WARN] MySQLError during execute statement \n\tArgs: '%s'", (str(e.args)))

            statement = ""

# Variables para conexión a mysql

db_host = "localhost"
s_db_name = "project_test"
d_db_name = "project_star_model"
db_user = "root"
db_pass = "Danipau2124"

scx = mysql.connector.connect(
    host=db_host, database=s_db_name, user=db_user, password=db_pass
  )

# Create star schema

scur = scx.cursor()

try:
    exec_sql_file(scur, "star-ini.sql")
    print("Star schema created")
except Exception as e:
    print("Error creating schema", e)

scx.commit()

# Se crea la conexión para la base de datos de estrella

dcx = mysql.connector.connect(
    host=db_host, database=d_db_name, user=db_user, password=db_pass
  )

dcur = dcx.cursor()

# x

scur.close()
scx.reconnect()
scur = scx.cursor()

# Funcion para llenar una tabla con el mismo nombre y misma info

def directETL (nCol, a, b = None):
    if b is None:
        b = a
    # a -> b
    query = "SELECT * FROM " + a + ";"
    scur.execute(query)
    a_rows = scur.fetchall()

    query = "INSERT INTO " + b + " VALUES ("

    for i in range(nCol):
        query += "%s,"
    
    query = query[:-1] + ");"

    # print("Insert query: ", query)
    
    for row in a_rows:
        dcur.execute(query, row)

# Se empiezan a realizar las operaciones ETL

# - cargos
# - egresado
# - empresa
# - facultad
# - institucion
# - publicacion
# - revista
# - sede_universidad
# - departamento
# - programa
# - time_
# - contrataciones
# - registro_publicaciones
# graduaciones

##############################################################################################################
        
# Se llenan las dimensiones primero         

directETL(2, "cargos")

directETL(10, "egresado")

directETL(3, "empresa")

directETL(2, "facultad")

directETL(2, "institucion")

directETL(4, "publicacion")

directETL(2, "revista")

directETL(2, "sede_universidad")


#### departamento

scur.execute("select departamento_nombre, departamento_id from project_test.departamento;")
departamento = scur.fetchall()

for row in departamento:
    dcur.execute("INSERT INTO departamento VALUES (%s,%s)", row)

#### programa

scur.execute("select programa_nombre, programa_nivelacademico, programa_id from programa;")
programa = scur.fetchall()

for row in programa:
    dcur.execute("INSERT INTO programa VALUES (%s,%s,%s);", row)

#### time_

# Se llena time desde start_date a end_date
    
start_year = 1970
end_year = 2024
    
start_date = date(start_year,1,1)
end_date = date(end_year,12,31)

delta = end_date - start_date

# weekdays = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    dcur.execute("INSERT INTO time_ (year_, month_, day_, date_id) VALUES (%s, %s, %s, %s);", [day.year, day.month, day.day, day])

##############################################################################################################

# Se llenan los hechos

#### contrataciones

scur.execute("select empresa_has_cargos.cargos_id, empresa_has_cargos.empresa_id, cargos_egresado.egresado_id, cargos_egresado.fecha_ingreso, cargos_egresado.salario from cargos_egresado JOIN empresa_has_cargos ON empresa_has_cargos.empresa_has_cargos_id = cargos_egresado.empresa_has_cargos_id;")
contrataciones = scur.fetchall()

for row in contrataciones:
    dcur.execute("INSERT INTO `contrataciones` (`cargo_id`, `empresa_id`, `egresado_id`, `date_id`, `salario`) VALUES (%s, %s, %s, %s, %s);", row)

#### registro_publicaciones

scur.execute("SELECT publicacion_revista.publicacion_id, revista_id, NULL, egresado_id, ano_publiacion FROM publicaciones_egresado JOIN publicacion_revista ON publicacion_revista.publicacion_id = publicaciones_egresado.publicacion_id JOIN publicacion ON publicacion_revista.publicacion_id = publicacion.publicacion_id;")
publicacion_revista = scur.fetchall()

# publicaciones egresado doble primary key?

for row in publicacion_revista:
    dcur.execute("INSERT INTO `registro_publicaciones` (`publicacion_id`, `revista_id`, `institucion_id`, `egresado_id`, `date_id`) VALUES (%s, %s, %s, %s, %s);", row)

# Publicaciones en institutos

scur.execute("SELECT publicacion_institucion.publicacion_id, NULL, institucion_id, egresado_id, ano_publiacion FROM publicaciones_egresado JOIN publicacion_institucion ON publicacion_institucion.publicacion_id = publicaciones_egresado.publicacion_id JOIN publicacion ON publicacion_institucion.publicacion_id = publicacion.publicacion_id;")
publicacion_institucion = scur.fetchall()

for row in publicacion_institucion:
    dcur.execute("INSERT INTO `registro_publicaciones` (`publicacion_id`, `revista_id`, `institucion_id`, `egresado_id`, `date_id`) VALUES (%s, %s, %s, %s, %s);", row)

#### graduaciones
        
scur.execute("select sede_universidad_sede_id, departamento.departamento_id, facultad_facultad_id, programa.programa_id, egresado_id, fecha from egresado_programa JOIN programa ON programa.programa_id = egresado_programa.programa_id JOIN departamento ON departamento.departamento_id = programa.departamento_id JOIN sede_universidad_has_facultad ON sede_universidad_has_facultad.sede_facultad_id = departamento.sede_facultad_id;")
graduaciones = scur.fetchall()

for row in graduaciones:
    dcur.execute("INSERT INTO `graduaciones` (`sede_id`, `departamento_id`, `facultad_id`, `programa_id`, `egresado_id`, `date_id`) VALUES (%s, %s, %s, %s, %s, %s);", row)

dcx.commit()
dcur.close()
dcx.close()
scur.close()
scx.close()