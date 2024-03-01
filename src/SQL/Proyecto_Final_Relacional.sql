Create database project;

USE project;

-- Entidades

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


Create table Sede_universidad(
       sede_nombre VARCHAR(10),
       sede_id int primary key
)


Create table Empresa(
       empresa_nombre VARCHAR(10),
       empresa_origen VARCHAR(20),
       empresa_id int primary key
)



Create table Cargos(
       cargo_nombre VARCHAR(10),
       cargo_id int primary key
)



Create table programa(
       programa_nombre VARCHAR(10),
       programa_nivelacademico VARCHAR(10),
       CONSTRAINT programa_nivelacademico CHECK (programa_nivelacademico IN ('Pregrado', 'Posgrado')),
       programa_id int primary key
)



Create table facultad(
       facultad_nombre VARCHAR(10),
       facultad_id int primary key
)



Create table departamento(
       departamento_nombre VARCHAR(10),
       departamento_id int primary key
)



Create table publicacion(
       tipo_publicacion VARCHAR(10),
	   ano_publiacion date,
       descripcion VARCHAR (1000),
       publicacion_id int primary key
)
    


Create table institucion(
       institucion_nombre VARCHAR(10),
       institucion_id int primary key
)



Create table revista(
       revista_nombre VARCHAR(10),
       revista_id int primary key
)



-- Relaciones

Create table egresado_programa (
       egresado_id int,
       programa_id int,
       registration_id int primary key,
       FOREIGN Key (egresado_id) References egresado(egresado_id),
       FOREIGN Key (programa_id) References programa(programa_id)
)



Create table programa_facultad (
       programa_id int,
       facultad_id int,
       registration_id int primary key,
       FOREIGN Key (programa_id) References programa(programa_id),
       FOREIGN Key (facultad_id) References facultad(facultad_id)
)



Create table facultad_departamento (
	   facultad_id int,
       departamento_id int,
	   FOREIGN Key (facultad_id) References facultad(facultad_id),
       FOREIGN Key (departamento_id) References departamento(departamento_id)
)



Create table publicaciones_egresado (
	   publicacion_id int,
       egresado_id int,
       registration_id int primary key,
	   FOREIGN Key (publicacion_id) References publicacion(publicacion_id),
       FOREIGN Key (egresado_id) References egresado(egresado_id)
)



Create table cargos_egresado (
	   cargo_id int,
       egresado_id int,
       fecha_ingreso date,
       salario int,
       registration_id int primary key,
	   FOREIGN Key (cargo_id) References cargos(cargo_id),
       FOREIGN Key (egresado_id) References egresado(egresado_id)
)

Create table cargos_empresa (
	   cargo_id int,
       empresa_id int,
       registration_id int primary key,
	   FOREIGN Key (cargo_id) References cargos(cargo_id),
       FOREIGN Key (empresa_id) References empresa(empresa_id)
)

Create table egresado_sede (
       egresado_id int,
       sede_id int,
       registration_id int primary key,
       FOREIGN Key (egresado_id) References egresado(egresado_id),
	   FOREIGN Key (sede_id) References sede_universidad(sede_id)       
)



Create table publicacion_institucion (
       publicacion_id int,
       institucion_id int,
       registration_id int primary key,
       FOREIGN Key (publicacion_id) References publicacion(publicacion_id),
	   FOREIGN Key (institucion_id) References institucion(institucion_id)       
)



Create table publicacion_revista (
       publicacion_id int,
       revista_id int,
       registration_id int primary key,
       FOREIGN Key (publicacion_id) References publicacion(publicacion_id),
	   FOREIGN Key (revista_id) References revista(revista_id)       
)

