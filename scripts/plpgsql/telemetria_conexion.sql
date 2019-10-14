CREATE EXTENSION ogr_fdw;

CREATE SERVER emaaphidro_srv FOREIGN DATA WRAPPER ogr_fdw
  OPTIONS (datasource 'ODBC:AdministradorGAR/AdministradorGAR@EMAAPHIDRO', format 'ODBC');

CREATE schema emaaphidro;
IMPORT FOREIGN SCHEMA "dbo." FROM SERVER emaaphidro_srv INTO emaaphidro;

--SELECT * FROM emaaphidro.dbo_tbldatos;



CREATE SERVER dbclima_srv FOREIGN DATA WRAPPER ogr_fdw
  OPTIONS (datasource 'ODBC:hidrometrico/Hidro_epmaps_2017@DBCLIMA', format 'ODBC');

CREATE schema dbclima;
IMPORT FOREIGN SCHEMA "dbo." FROM SERVER dbclima_srv INTO dbclima;

--SELECT * FROM dbclima.dbo_measurements;