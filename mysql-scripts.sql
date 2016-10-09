USE oily-palm; 

DELIMITER //

DROP PROCEDURE IF EXISTS getPhonesByDate;

CREATE PROCEDURE getPhonesByDate(IN date_IN DATE)
BEGIN
    SELECT phone
    FROM (
        SELECT village
        FROM village JOIN events
        WHERE ABS(village.lat - events.lat) < 0.0667
            AND ABS(village.lon - events.lon) < 0.0667
            AND events.date = date_IN 
        ) AS filt
        JOIN users
        ON filt.village = users.village;
END //


DROP PROCEDURE IF EXISTS getEventsByPhone;

CREATE PROCEDURE getEventsByPhone(IN phone_IN TEXT)
BEGIN
    SELECT nearby.phone, events.event 
    FROM (
        SELECT users.village, village.lat, village.lon, users.phone
        FROM users
        JOIN village
        ON village.village = users.village
        WHERE users.phone = phone_IN
        ) AS nearby 
    JOIN events
    WHERE ABS(nearby.lat - events.lat) < 0.0667
        AND ABS(nearby.lon - events.lon) < 0.0667
        AND events.date = CURDATE();
END //



DROP PROCEDURE IF EXISTS dummy;

CREATE PROCEDURE dummy()
BEGIN
    SELECT * FROM events;
END //


DROP PROCEDURE IF EXISTS insertFormaEvent;

CREATE PROCEDURE insertFormaEvent(IN date_IN DATE, IN lat_IN DOUBLE, IN lon_IN DOUBLE)
BEGIN
    INSERT INTO events (date, source, lat, lon)
    VALUES (date_IN, "forma", lat_IN, lon_IN );
END //
