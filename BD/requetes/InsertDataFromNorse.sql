CREATE OR ALTER PROCEDURE InsertDataFromNorse

    @attacker varchar(200),
	@target_country varchar(50),
	@attacker_town varchar(50),
	@ip varchar(50),
	@attacker_country varchar(50),
	@target_town varchar(50),
	@date datetime, -- verifier la compatibilité
	@type_attack varchar(50)

AS
DECLARE 
	@id_type_attack int,
	@id_target_country int,
	@id_target_city int,
	@id_attacker_country int,
	@id_attacker_city int,
	@id_attacker int
BEGIN

	exec @id_type_attack = F_Id_type_attack @type_attack=@type_attack
	print @id_type_attack
	
	exec @id_target_country = F_Id_country @name_country=@target_country
	print @id_target_country

	exec @id_target_city = F_Id_city @name_city=@target_town,@id_country=@id_target_country
	print @id_target_city

	exec @id_attacker_country = F_Id_country @name_country=@attacker_country
	print @id_attacker_country

	exec @id_attacker_city = F_Id_city @name_city=@attacker_town,@id_country=@id_attacker_country
	print @id_attacker_city

	exec @id_attacker = F_Id_attacker @name_attacker=@attacker, @IP_attacker=@ip, @id_city=@id_attacker_city
	print @id_attacker

	INSERT INTO attack(date_attack,id_attacker,id_city,id_type_attack) values(@date,@id_attacker,@id_target_city,@id_type_attack)
END
GO

exec InsertDataFromNorse @type_attack='ddos',@target_country='France',@target_town='Carcassonne',@attacker_town='Toulouse',@attacker_country='France',@attacker='lolo-bucheron',@ip='100.93.3.26',@date='2018-03-11 08:48:10'
GO


