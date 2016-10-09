USE oily-palm; 

SELECT phone
FROM (
    SELECT village
    FROM village JOIN events
    WHERE ABS(village.lat - events.lat) < 100
        AND ABS(village.lon - events.lon) < 100
        AND events.date = CURDATE() 
    ) AS filt
    JOIN users
    ON filt.village = users.village;



SELECT nearby.phone, events.event 
FROM (
    SELECT users.village, village.lat, village.lon, users.phone
    FROM users
    JOIN village
    WHERE village.village = users.village
    ) AS nearby 
JOIN events
WHERE ABS(nearby.lat - events.lat) < 100
    AND ABS(nearby.lon - events.lon) < 100
    AND events.date = CURDATE();

