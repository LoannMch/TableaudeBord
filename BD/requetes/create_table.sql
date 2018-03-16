/*------------------------------------------------------------
*        Script SQLSERVER 
------------------------------------------------------------*/


/*------------------------------------------------------------
-- Table: attack
------------------------------------------------------------*/
CREATE TABLE attack(
	id_attack       INT IDENTITY (1,1) NOT NULL ,
	date_attack     DATETIME  ,
	id_organisation INT   ,
	id_attacker     INT   ,
	id_city         INT   ,
	id_type_attack  INT   ,
	CONSTRAINT prk_constraint_attack PRIMARY KEY NONCLUSTERED (id_attack)
);


/*------------------------------------------------------------
-- Table: attacker
------------------------------------------------------------*/
CREATE TABLE attacker(
	id_attacker  INT IDENTITY (1,1) NOT NULL ,
	lib_attacker VARCHAR (200)  ,
	IP_attacker  VARCHAR (200)  ,
	id_city      INT   ,
	CONSTRAINT prk_constraint_attacker PRIMARY KEY NONCLUSTERED (id_attacker)
);


/*------------------------------------------------------------
-- Table: organisation
------------------------------------------------------------*/
CREATE TABLE organisation(
	id_organisation      INT IDENTITY (1,1) NOT NULL ,
	lib_organisation     VARCHAR (200)  ,
	url                  VARCHAR (200)  ,
	IP_address           VARCHAR (200)  ,
	famous               bit   ,
	id_country           INT   ,
	id_type_server       INT   ,
	id_OS_property       INT   ,
	id_type_organisation INT   ,
	CONSTRAINT prk_constraint_organisation PRIMARY KEY NONCLUSTERED (id_organisation)
);


/*------------------------------------------------------------
-- Table: country
------------------------------------------------------------*/
CREATE TABLE country(
	id_country  INT IDENTITY (1,1) NOT NULL ,
	lib_country VARCHAR (200)  ,
	CONSTRAINT prk_constraint_country PRIMARY KEY NONCLUSTERED (id_country)
);


/*------------------------------------------------------------
-- Table: type_server
------------------------------------------------------------*/
CREATE TABLE type_server(
	id_type_server  INT IDENTITY (1,1) NOT NULL ,
	lib_type_server VARCHAR (50)  ,
	CONSTRAINT prk_constraint_type_server PRIMARY KEY NONCLUSTERED (id_type_server)
);


/*------------------------------------------------------------
-- Table: OS_property
------------------------------------------------------------*/
CREATE TABLE OS_property(
	id_OS_property  INT IDENTITY (1,1) NOT NULL ,
	lib_OS_property VARCHAR (200)  ,
	CONSTRAINT prk_constraint_OS_property PRIMARY KEY NONCLUSTERED (id_OS_property)
);


/*------------------------------------------------------------
-- Table: city
------------------------------------------------------------*/
CREATE TABLE city(
	id_city    INT IDENTITY (1,1) NOT NULL ,
	lib_city   VARCHAR (200)  ,
	id_country INT   ,
	CONSTRAINT prk_constraint_city PRIMARY KEY NONCLUSTERED (id_city)
);


/*------------------------------------------------------------
-- Table: type_organisation
------------------------------------------------------------*/
CREATE TABLE type_organisation(
	id_type_organisation  INT IDENTITY (1,1) NOT NULL ,
	lib_type_organisation VARCHAR (200)  ,
	CONSTRAINT prk_constraint_type_organisation PRIMARY KEY NONCLUSTERED (id_type_organisation)
);


/*------------------------------------------------------------
-- Table: type_attack
------------------------------------------------------------*/
CREATE TABLE type_attack(
	id_type_attack  INT IDENTITY (1,1) NOT NULL ,
	lib_type_attack VARCHAR (200)  ,
	CONSTRAINT prk_constraint_type_attack PRIMARY KEY NONCLUSTERED (id_type_attack)
);



ALTER TABLE attack ADD CONSTRAINT FK_attack_id_organisation FOREIGN KEY (id_organisation) REFERENCES organisation(id_organisation);
ALTER TABLE attack ADD CONSTRAINT FK_attack_id_attacker FOREIGN KEY (id_attacker) REFERENCES attacker(id_attacker);
ALTER TABLE attack ADD CONSTRAINT FK_attack_id_city FOREIGN KEY (id_city) REFERENCES city(id_city);
ALTER TABLE attack ADD CONSTRAINT FK_attack_id_type_attack FOREIGN KEY (id_type_attack) REFERENCES type_attack(id_type_attack);
ALTER TABLE attacker ADD CONSTRAINT FK_attacker_id_city FOREIGN KEY (id_city) REFERENCES city(id_city);
ALTER TABLE organisation ADD CONSTRAINT FK_organisation_id_country FOREIGN KEY (id_country) REFERENCES country(id_country);
ALTER TABLE organisation ADD CONSTRAINT FK_organisation_id_type_server FOREIGN KEY (id_type_server) REFERENCES type_server(id_type_server);
ALTER TABLE organisation ADD CONSTRAINT FK_organisation_id_OS_property FOREIGN KEY (id_OS_property) REFERENCES OS_property(id_OS_property);
ALTER TABLE organisation ADD CONSTRAINT FK_organisation_id_type_organisation FOREIGN KEY (id_type_organisation) REFERENCES type_organisation(id_type_organisation);
ALTER TABLE city ADD CONSTRAINT FK_city_id_country FOREIGN KEY (id_country) REFERENCES country(id_country);
