CREATE PROCEDURE InsertDataFromNorse
    @attacker varchar,
	@target_country varchar,
	@attacker_town varchar,
	@ip varchar,
	@attacker_country varchar,
	@target_town varchar,
	@date datetime, -- verifier la compatibilité
	@attack_type varchar
AS
	SELECT @id_type_attack = id_type_attack
	FROM type_attack
	WHERE lib_type_attack = @attack_type;
GO