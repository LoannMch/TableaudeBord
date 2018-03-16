ALTER TABLE attack DROP CONSTRAINT FK_attack_id_attacker;
ALTER TABLE attack DROP CONSTRAINT FK_attack_id_city;
ALTER TABLE attack DROP CONSTRAINT FK_attack_id_organisation;
ALTER TABLE attack DROP CONSTRAINT FK_attack_id_type_attack;

ALTER TABLE attacker DROP CONSTRAINT FK_attacker_id_city;

ALTER TABLE city DROP CONSTRAINT FK_city_id_country;

ALTER TABLE organisation DROP CONSTRAINT FK_organisation_id_country;
ALTER TABLE organisation DROP CONSTRAINT FK_organisation_id_OS_property;
ALTER TABLE organisation DROP CONSTRAINT FK_organisation_id_type_organisation;
ALTER TABLE organisation DROP CONSTRAINT FK_organisation_id_type_server;

DROP TABLE attack;
DROP TABLE attacker;
DROP TABLE city;
DROP TABLE country;
DROP TABLE organisation;
DROP TABLE OS_property;
DROP TABLE type_attack;
DROP TABLE type_organisation;
DROP TABLE type_server;