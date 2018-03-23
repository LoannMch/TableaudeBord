SELECT count(id_attack) as Nb_attack,lib_country
FROM attack, city ,country
WHERE attack.id_city = city.id_city
AND  city.id_country =country.id_country
GROUP BY lib_country
ORDER BY count(id_attack) DESC;

SELECT count(id_attack) as Nb_attack,lib_type_attack
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
