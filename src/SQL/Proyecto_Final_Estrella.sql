create database project_star_model;

USE project_star_model;

-- Tablas de dimensiones


Create table egresado(
       egresado_names VARCHAR(10),
       egresado_firstlastname VARCHAR(10),
	   egresado_secondlastname VARCHAR(10),
       egresado_gender VARCHAR(10),
       egresado_etnicgroup VARCHAR(10),
	   egresado_cellphone int,
       egresado_address VARCHAR(20),
	   egresado_emailaddress VARCHAR(20),
       egresado_edad int,
       CONSTRAINT egresado_etnicgroup CHECK (egresado_etnicgroup IN ('Activo', 'Inactivo')),
       egresado_id int primary key
)

Insert egresado(egresado_names, egresado_firstlastname,
	   egresado_secondlastname, egresado_gender,
       egresado_etnicgroup,egresado_cellphone, egresado_address,
	   egresado_address, egresado_edad) Values 
("Demetrio","male",'2002-01-21',001)


Create table sede_universidad(
       sede_nombre VARCHAR(10),
       CONSTRAINT sede_nombre CHECK (sede_nombre IN ('Bogota', 'Medellin','La Paz', 'Orinoquia')),
       sede_id int primary key
)

Insert sede_universidad(sede_nombre,sede_id) Values 
("Demetrio",001),
("Maria",002)

Create table Cargos(
       cargo_nombre VARCHAR(10),
       cargo_sectorlaboral VARCHAR(20),
       cargo_id int primary key
)

Insert cargo(cargo_nombre,cargo_sectorlaboral,cargo_id) Values 
("Demetrio","nanana",001),
("Maria","nanana",002)

Create table Empresa(
       empresa_nombre VARCHAR(10),
       empresa_origen VARCHAR(20),
       empresa_id int primary key
)

Insert Empresa(empresa_nombre,empresa_origen,empresa_id) Values 
("Demetrio","nanana",001),
("Maria","nanana",002)

Create table programa(
       programa_nombre VARCHAR(10),
       programa_nivelacademico VARCHAR(10),
       CONSTRAINT programa_nivelacademico CHECK (programa_nivelacademico IN ('Pregrado', 'Posgrado')),
       programa_id int primary key
)

Insert programa(programa_nombre, programa_nivelacademico, programa_id) Values 
("Demetrio",001),
("Maria",002)

Create table facultad(
       facultad_nombre VARCHAR(10),
       facultad_id int primary key
)

Insert facultad(facultad_nombre, facultad_id) Values 
("Demetrio",001),
("Maria",002)

Create table departamento(
       departamento_nombre VARCHAR(10),
       departamento_id int primary key
)

Insert departamento(departamento_nombre, departamento_id) Values 
("Demetrio",001),
("Maria",002)

Create table publicacion(
       tipo_publicacion VARCHAR(10),
	   ano_publiacion date,
       descripcion VARCHAR (1000),
       publicacion_id int primary key
)
    
Insert publicacion( tipo_publicacion, ano_publiacion, descripcion, publicacion_id) Values 
("Demetrio","male",'2002-01-21',001),
("Maria","female",'2002-01-21',002),

Create table institucion(
       institucion_nombre VARCHAR(10),
       institucion_id int primary key
)

Insert institucion(institucion_nombre, institucion_id) Values 
("Demetrio",001),
("Maria",002)

Create table revista(
       revista_nombre VARCHAR(10),
       revista_id int primary key
)

Insert revista(revista_nombre, revista_id) Values 
("Demetrio",001),
("Maria",002)


Create table time_(
       year_ int,
       month_ int,
       day_ int,
       date_id date
)

Insert time_(year_, month_, day_, date_id) Values 
("Demetrio",001),
("Maria",002)

CREATE INDEX idx_date_id ON time_ (date_id);

-- Tablas de Hechos

Create table graduaciones(
       sede_id int,
       departamento_id int,
	   programa_id int,
       egresado_id int,
       date_id date,
       registration_id int primary key,
       FOREIGN Key (sede_id) References sede_universidad(sede_id),
       FOREIGN Key (departamento_id) References departamento(departamento_id),
	   FOREIGN Key (programa_id) References programa(programa_id),
	   FOREIGN Key (egresado_id) References egresado(egresado_id),
       FOREIGN Key (date_id) References time_(date_id)
)

Insert student(egresado_id, programa_id, registration_id) Values 
(001,001,001),
(001,001,001)

Create table registro_publicaciones (
       publicacion_id int,
       revista_id int,
	   institucion_id int,
       egresado_id int,
       date_id date,
       registration_id int primary key,
       FOREIGN Key (publicacion_id) References publicacion(publicacion_id),
       FOREIGN Key (revista_id) References revista(revista_id),
	   FOREIGN Key (institucion_id) References institucion(institucion_id),
	   FOREIGN Key (egresado_id) References egresado(egresado_id),
       FOREIGN Key (date_id) References time_(date_id)
)

Insert programa_facultad(facultad_id,programa_id) Values 
(001,001),
(001,001)

Create table contrataciones (
       cargo_id int,
       empresa_id int,
       egresado_id int,
       date_id date,
       salario decimal,
       contratacion_id int primary key,
       FOREIGN Key (cargo_id) References cargos(cargo_id),
       FOREIGN Key (empresa_id) References empresa(empresa_id),
	   FOREIGN Key (egresado_id) References egresado(egresado_id),
       FOREIGN Key (date_id) References time_(date_id)
)

Insert facultad_departamento(facultad_id,departamento_id) Values 
(001,001),
(001,001)

