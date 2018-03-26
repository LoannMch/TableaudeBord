SELECT count(id_attack) as Nb_attack,lib_country
FROM attack, city ,country
WHERE attack.id_city = city.id_city
AND  city.id_country =country.id_country
GROUP BY lib_country
ORDER BY count(id_attack) DESC;

SELECT TOP(20) count(id_attack) as Nb_attack,lib_type_attack
FROM attack, type_attack
WHERE attack.id_type_attack = type_attack.id_type_attack
GROUP BY lib_type_attack
ORDER BY count(id_attack) DESC;

SELECT count(id_attack) as Nb_attack,co1.lib_country as 'Attaqué',co2.lib_country as 'Attaquant'
FROM attack, attacker, city ci1, country co1, city ci2, country co2
WHERE attack.id_city = ci1.id_city
AND  ci1.id_country =co1.id_country
AND attack.id_attacker = attacker.id_attacker
AND  attacker.id_city = ci2.id_city
AND  ci2.id_country =co2.id_country
GROUP BY co1.lib_country, co2.lib_country
ORDER BY count(id_attack) DESC;

SELECT count(id_attack) as Nb_attack,lib_type_attack,lib_country
FROM attack, type_attack, city ,country
WHERE attack.id_type_attack = type_attack.id_type_attack
AND attack.id_city = city.id_city
AND  city.id_country =country.id_country
GROUP BY lib_type_attack,lib_country
ORDER BY count(id_attack) DESC;

SELECT count(id_attack) as Nb_attack,co1.lib_country as 'Pays'
FROM attack, attacker, city ci1, country co1, city ci2, country co2
WHERE attack.id_city = ci1.id_city
AND  ci1.id_country =co1.id_country
AND attack.id_attacker = attacker.id_attacker
AND  attacker.id_city = ci2.id_city
AND  ci2.id_country = co2.id_country
AND co1.id_country = co2.id_country
GROUP BY co1.lib_country, co2.lib_country
ORDER BY count(id_attack) DESC;

SELECT c.lib_country,
(SELECT count(id_attack) as Nb_attack_subie
FROM attack, city ,country
WHERE attack.id_city = city.id_city
AND city.id_country = country.id_country
AND country.lib_country = c.lib_country
GROUP BY lib_country) as Nb_attack_subie,
(SELECT count(id_attack) as Nb_attack_emmise
FROM attack, city ,country, attacker
WHERE attack.id_attacker = attacker.id_attacker
AND attacker.id_city = city.id_city
AND city.id_country = country.id_country
AND country.lib_country = c.lib_country
GROUP BY lib_country) as Nb_attack_emmise
FROM country c

SELECT count(id_attack) as Nb_attack_subie
FROM attack, city ,country
WHERE attack.id_city = city.id_city
AND city.id_country = country.id_country
AND country.lib_country = 'france'
GROUP BY lib_country;

SELECT count(id_attack) as Nb_attack_emmise,lib_country
FROM attack, city ,country, attacker
WHERE attack.id_attacker = attacker.id_attacker
AND attacker.id_city = city.id_city
AND city.id_country = country.id_country
AND country.lib_country = 'france'
GROUP BY lib_country;

/* ZoneH */
SELECT TOP(10) COUNT(id_attack) AS Nb_attack, lib_organisation
FROM attack, organisation
WHERE attack.id_organisation = organisation.id_organisation
GROUP BY lib_organisation
ORDER BY COUNT(id_attack) DESC;

SELECT TOP(10) COUNT(id_attack) AS Nb_attack, lib_organisation
FROM attack, organisation
WHERE attack.id_organisation = organisation.id_organisation
AND  organisation.famous = 1
GROUP BY lib_organisation
ORDER BY COUNT(id_attack) DESC;

SELECT TOP(10) COUNT(id_attack) AS Nb_attack, lib_type_organisation
FROM attack, organisation, type_organisation
WHERE attack.id_organisation = organisation.id_organisation
AND organisation.id_type_organisation = type_organisation.id_type_organisation
GROUP BY lib_type_organisation
ORDER BY COUNT(id_attack) DESC;

SELECT TOP(10) COUNT(id_attack) AS Nb_attack, lib_type_server
FROM attack, organisation, type_server
WHERE attack.id_organisation = organisation.id_organisation
AND organisation.id_type_server = type_server.id_type_server
GROUP BY lib_type_server
ORDER BY COUNT(id_attack) DESC;

SELECT TOP(10) COUNT(id_attack) AS Nb_attack, lib_OS_property
FROM attack, organisation, OS_property
WHERE attack.id_organisation = organisation.id_organisation
AND organisation.id_OS_property = OS_property.id_OS_property
GROUP BY lib_OS_property
ORDER BY COUNT(id_attack) DESC;


SELECT x.month_date as mois, AVG(x.nb_attack) as nb_attack
FROM (SELECT YEAR(attack.date_attack) AS year_date, MONTH(date_attack) AS month_date, count(id_attack) AS nb_attack
		FROM attack 
		WHERE id_city is null
		GROUP BY YEAR(date_attack), MONTH(date_attack)) x
GROUP BY x.month_date;

SELECT lib_country, COUNT(id_attack) AS Nb_attack
FROM attack, organisation, country
WHERE attack.id_organisation = organisation.id_organisation
AND organisation.id_country = country.id_country
GROUP BY lib_country
ORDER BY COUNT(id_attack) DESC;