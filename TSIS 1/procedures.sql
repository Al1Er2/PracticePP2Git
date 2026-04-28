-- ==========================================
-- 1. ПРОЦЕДУРА: ДОБАВЛЕНИЕ ТЕЛЕФОНА
-- ==========================================
DROP PROCEDURE IF EXISTS add_phone(TEXT, TEXT, TEXT);
DROP PROCEDURE IF EXISTS add_phone(VARCHAR, VARCHAR, VARCHAR);

CREATE OR REPLACE PROCEDURE add_phone(p_contact_name TEXT, p_phone TEXT, p_type TEXT)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    -- Ищем ID контакта по имени
    SELECT id INTO v_contact_id FROM contacts WHERE first_name = p_contact_name LIMIT 1;
    
    IF v_contact_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_contact_id, p_phone, p_type);
    ELSE
        RAISE EXCEPTION 'Контакт % не найден', p_contact_name;
    END IF;
END;
$$;

-- ==========================================
-- 2. ПРОЦЕДУРА: ПЕРЕВОД В ГРУППУ
-- ==========================================
DROP PROCEDURE IF EXISTS move_to_group(TEXT, TEXT);
DROP PROCEDURE IF EXISTS move_to_group(VARCHAR, VARCHAR);

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name TEXT, p_group_name TEXT)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    -- Создаем группу, если её нет
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    
    -- Получаем ID группы
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    -- Обновляем группу у контакта
    UPDATE contacts SET group_id = v_group_id WHERE first_name = p_contact_name;
END;
$$;

-- ==========================================
-- 3. ФУНКЦИЯ: РАСШИРЕННЫЙ ПОИСК (TSIS 1)
-- ==========================================
-- Удаляем старые версии из Practice 8 и TSIS 1, чтобы не было конфликта возвращаемых колонок
DROP FUNCTION IF EXISTS search_contacts(TEXT);
DROP FUNCTION IF EXISTS search_contacts(VARCHAR);

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    first_name VARCHAR, 
    last_name VARCHAR, 
    email VARCHAR, 
    phone VARCHAR, 
    phone_type VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.first_name::VARCHAR, 
        c.last_name::VARCHAR, 
        c.email::VARCHAR, 
        p.phone::VARCHAR, 
        p.type::VARCHAR
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.last_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone LIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- 4. ФУНКЦИЯ: ПАГИНАЦИЯ (Адаптированная)
-- ==========================================
DROP FUNCTION IF EXISTS get_contacts_paginated(INT, INT);

CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE (id INT, first_name VARCHAR, last_name VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name::VARCHAR, c.last_name::VARCHAR, c.email::VARCHAR
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;