CREATE OR ALTER PROCEDURE InsertDataFromZoneH

    @attacker varchar(200),
	@date datetime,
	-- @type_attack varchar(50)
	@lib_organisation varchar(200),
	@lib_type_server varchar(200),
	@country varchar(200),
	@lib_OS_property varchar(200),
	@type_organisation varchar(200)

AS
DECLARE 
	@id_organisation int,
	@id_attacker int,
	@id_type_server int,
	@id_country int,
	@id_OS_property int,
	@id_type_organisation int
BEGIN
	IF(@attacker is null)
		SET @id_attacker = null;
	ELSE
		exec @id_attacker = F_Id_attacker @name_attacker=@attacker, @id_city=null;
	print @id_attacker

	IF(@lib_type_server is null)
		SET @id_type_server = null
	ELSE 
		exec @id_type_server = F_Id_type_server @lib_type_server=@lib_type_server;
	print @id_type_server

	IF(@country is null)
		SET @id_country = null
	ELSE 
		exec @id_country = F_Id_country @name_country=@country
	print @id_country

	IF(@lib_OS_property is null)
		SET @id_OS_property = null
	ELSE 
		exec @id_OS_property =  F_Id_OS_property @lib_OS_property = @lib_OS_property
	print @id_OS_property

	IF(@type_organisation is null)
		SET @id_type_organisation = null
	ELSE 
		exec @id_type_organisation = F_Id_type_organisation @lib_type_organisation = @type_organisation
	print @id_type_organisation

	IF(@lib_organisation is null)
		SET @id_organisation = null
	ELSE 
		exec @id_organisation = F_Id_organisation @lib_organisation=@lib_organisation, @famous=1, @id_country=@id_country, @id_type_server=@id_type_server, @id_OS_property=1, @id_type_organisation=1
	print @id_organisation

	INSERT INTO attack(date_attack, id_attacker, id_organisation) values(@date, @id_attacker, @id_organisation)
END
GO

exec InsertDataFromZoneH  @attacker = null,	@date = '2017-05-11 08:48:10', @lib_organisation = 'Oracle', @lib_type_server = 'Apache', @country = 'France', @lib_OS_property = 'Linux', @type_organisation = 'Information'
GO

select count(id_attack) from attack where id_city is null;

select * from attack 
where id_city is null
AND id_organisation='175';

/* DELETE FROM attack WHERE id_city is null;
GO*/

SELECT count(*) from organisation
DELETE FROM organisation
GO

select * from attack, attacker 
where attack.id_city is null
AND attack.id_attacker = attacker.id_attacker;


select * from attacker where lib_attacker='team codezero';

select * 
from attacker,attack 
where attacker.id_attacker = attack.id_attack
and lib_attacker='team codezero';
