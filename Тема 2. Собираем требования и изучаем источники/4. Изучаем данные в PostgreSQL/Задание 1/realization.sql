-- Напишите запрос, который вернёт строки с информацией об атрибутах колонок всех таблиц из схемы public. Список таблиц из схемы public нужно получить в рамках этого же запроса. В результате вы должны получить следующую информацию:
--table_name — название таблицы;
--column_name — название колонки;
--data_type — тип данных в колонке;
--character_maximum_length — для строковых типов — максимальная длина значения в колонке;
--column_default — значение по умолчанию для колонки;
--is_nullable — может ли в колонке быть значение NULL.
--Строки в результате запроса должны быть отсортированы в алфавитном порядке по названию таблицы.

SELECT
    t.table_name,
    c.column_name,
    c.data_type,
    c.character_maximum_length,
    c.column_default,
    c.is_nullable
FROM information_schema.tables t
INNER JOIN information_schema.columns c
ON t.table_name = c.table_name
WHERE t.table_schema = 'public'
ORDER BY t.table_name, c.ordinal_position;

