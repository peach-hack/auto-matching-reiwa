SELECT
    table_schema, sum(data_length+index_length) /1024 /1024/1024 as GB
FROM
    information_schema.tables
GROUP BY
    table_schema
ORDER BY
    sum(data_length+index_length) DESC;