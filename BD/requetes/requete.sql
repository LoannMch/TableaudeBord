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