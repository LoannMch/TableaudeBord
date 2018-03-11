/* 
	Procedure qui prend un type d'attaque en parametre d'entrée
	retourne l'id_type_attack associé en sortie
	si le type d'attaque n'est pas dans la bd, il est inséré 
*/

CREATE OR ALTER PROCEDURE F_Id_type_attack
	@type_attack varchar(50)
AS
DECLARE @id_type_attack int
BEGIN
	SELECT @id_type_attack = id_type_attack
	FROM type_attack
	WHERE lib_type_attack = @type_attack;

	IF(@id_type_attack is null)
		Insert Into type_attack(lib_type_attack) values(@type_attack);
	IF(@id_type_attack is null)
		Select @id_type_attack = @@identity;
	RETURN(@id_type_attack); 
END
GO
-- test de la fonction F_Id_type_attack 
declare @ret int
exec @ret = F_Id_type_attack @type_attack='ddos'
print @ret
GO

SELECT *
from type_attack
where lib_type_attack='ddos';
GO

/*
	Procedure qui prend un pays en parametre d'entrée
	retourne l'id du pays associé en sortie
	si le pays n'est pas dans la bd, il est inséré 
*/
CREATE OR ALTER PROCEDURE F_Id_country
	@name_country varchar(50)
AS
DECLARE @id_country int
BEGIN
	SELECT @id_country = id_country
	FROM country
	WHERE name_country = @name_country;

	IF(@id_country is null)
		Insert Into country(name_country) values(@name_country);
	IF(@id_country is null)
		Select @id_country = @@identity;
	RETURN(@id_country); 
END
GO

-- test de la fonction F_Id_country 
declare @ret int
exec @ret = F_Id_country @name_country='France'
print @ret
GO

SELECT *
from country;
GO

/*
	Procedure qui prend une ville et un Id de pays en parametres d'entrée
	retourne l'id de la ville associé en sortie
	si la ville n'est pas dans la bd, elle est insérée
*/
CREATE OR ALTER PROCEDURE F_Id_city
	@name_city varchar(50),
	@id_country int
AS
DECLARE @id_city int
BEGIN
	SELECT @id_city = id_city
	FROM city
	WHERE name_city = @name_city;

	IF(@id_city is null)
		Insert Into city(name_city, id_country) values(@name_city, @id_country);
	IF(@id_city is null)
		Select @id_city = @@identity;
	RETURN(@id_city); 
END

-- test de la fonction F_Id_city 
declare @ret int
exec @ret = F_Id_city @name_city='Toulouse',@id_country=1
print @ret
GO

SELECT *
from city;
GO

-- A compléter pour les données de Zone-H
CREATE OR ALTER PROCEDURE F_Id_attacker
	@name_attacker varchar(200),
	@IP_attacker varchar(50),
	@id_city int
AS
DECLARE @id_attacker int
BEGIN
	SELECT @id_attacker = id_hacker
	FROM attacker
	WHERE name_attacker = @name_attacker;

	IF(@id_attacker is null)
		IF(@id_city is null)
			Insert Into attacker(name_attacker, IP_attacker, id_city) values(@name_attacker, @IP_attacker, null);
		ELSE
			Insert Into attacker(name_attacker, IP_attacker, id_city) values(@name_attacker, @IP_attacker, @id_city);
	IF(@id_attacker is null)
		Select @id_attacker = @@identity;
	RETURN(@id_attacker); 
END

-- test de la fonction F_Id_city 
declare @ret int
exec @ret = F_Id_attacker @name_attacker='lolo-bucheron', @IP_attacker='100.93.3.26', @id_city='2'
print @ret
GO

SELECT *
from attack;
GO