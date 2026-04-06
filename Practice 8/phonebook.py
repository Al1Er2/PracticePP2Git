CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, name TEXT, surname TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, surname, phone
    FROM phonebook
    WHERE name ILIKE '%' || pattern || '%'
       OR surname ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE upsert_user(p_name TEXT, p_surname TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name AND surname = p_surname) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO phonebook(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_users(users JSON)
LANGUAGE plpgsql AS $$
DECLARE
    rec JSON;
    u_name TEXT;
    u_surname TEXT;
    u_phone TEXT;
    invalid_data JSON := '[]'::JSON;
BEGIN
    FOR rec IN SELECT * FROM json_array_elements(users)
    LOOP
        u_name := rec->>'name';
        u_surname := rec->>'surname';
        u_phone := rec->>'phone';

        IF u_phone ~ '^[0-9]+$' AND length(u_phone) >= 5 THEN
            CALL upsert_user(u_name, u_surname, u_phone);
        ELSE
            invalid_data := invalid_data || json_build_array(rec);
        END IF;
    END LOOP;

    RAISE NOTICE 'Некорректные данные: %', invalid_data;
END;
$$;


CREATE OR REPLACE FUNCTION get_phonebook_page(limit_rows INT, offset_rows INT)
RETURNS TABLE(id INT, name TEXT, surname TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, surname, phone
    FROM phonebook
    ORDER BY id
    LIMIT limit_rows OFFSET offset_rows;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_user(p_name TEXT DEFAULT NULL, p_phone TEXT DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_name IS NOT NULL THEN
        DELETE FROM phonebook WHERE name = p_name;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
    ELSE
        RAISE NOTICE 'Name, phone number';
    END IF;
END;
$$;
