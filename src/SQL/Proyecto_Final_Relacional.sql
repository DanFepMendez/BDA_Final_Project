Create database project;

USE project;

-- Entidades

Create table egresado(
       egresado_name VARCHAR(10),
       egresado_gender VARCHAR(10),
       egresado_edad int,
       fecha_egreso date,
       egresado_estado VARCHAR(10),
       CONSTRAINT egresado_estados CHECK (egresado_estado IN ('Activo', 'Inactivo')),
       egresado_id int primary key
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),
("Marcos","male",'2004-01-21',003)

Create table Sede_universidad(
       sede_nombre VARCHAR(10),
       sede_id int primary key
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

Create table Cargos(
       cargo_nombre VARCHAR(10),
       cargo_id int primary key
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

Create table facultad(
       facultad_nombre VARCHAR(10),
       facultad_id int primary key
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

Create table departamento(
       departamento_nombre VARCHAR(10),
       departamento_id int primary key
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

Create table publicacion(
       tipo_publicacion VARCHAR(10),
	   ano_publiacion date,
       descripcion VARCHAR (1000),
       publicacion_id int primary key
)
    
Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

Create table institucion(
       institucion_nombre VARCHAR(10),
       institucion_id int primary key
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

Create table revista(
       revista_nombre VARCHAR(10),
       revista_id int primary key
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

-- Relaciones

Create table egresado_facultad (
       egresado_id int,
       facultad_id int,
       registration_id int primary key,
       FOREIGN Key (egresado_id) References egresado(egresado_id),
       FOREIGN Key (facultad_id) References facultad(facultad_id)
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

Create table facultad_departamento (
	   facultad_id int,
       departamento_id int,
	   FOREIGN Key (facultad_id) References facultad(facultad_id),
       FOREIGN Key (departamento_id) References departamento(departamento_id)
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

Create table publicaciones_egresado (
	   publicacion_id int,
       egresado_id int,
       registration_id int primary key,
	   FOREIGN Key (publicacion_id) References publicacion(publicacion_id),
       FOREIGN Key (egresado_id) References egresado(egresado_id)
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

select * from publicacion

Create table cargos_egresado (
	   cargo_id int,
       egresado_id int,
       fecha_ingreso date,
       salario int,
       registration_id int primary key,
	   FOREIGN Key (cargo_id) References cargos(cargo_id),
       FOREIGN Key (egresado_id) References egresado(egresado_id)
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),


Create table egresado_sede (
       egresado_id int,
       sede_id int,
       registration_id int primary key,
       FOREIGN Key (egresado_id) References egresado(egresado_id),
	   FOREIGN Key (sede_id) References sede_universidad(sede_id)       
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

Create table publicacion_institucion (
       publicacion_id int,
       institucion_id int,
       registration_id int primary key,
       FOREIGN Key (publicacion_id) References publicacion(publicacion_id),
	   FOREIGN Key (institucion_id) References institucion(institucion_id)       
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

Create table publicacion_revista (
       publicacion_id int,
       revista_id int,
       registration_id int primary key,
       FOREIGN Key (publicacion_id) References publicacion(publicacion_id),
	   FOREIGN Key (revista_id) References revista(revista_id)       
)

Insert student(student_name,student_gender,student_DateBirth,student_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),