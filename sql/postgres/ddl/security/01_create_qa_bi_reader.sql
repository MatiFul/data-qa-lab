DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_roles
        WHERE rolname = 'qa_bi_reader'
    ) THEN
        CREATE ROLE qa_bi_reader
            LOGIN
            PASSWORD 'qa_bi_pass';
    END IF;
END
$$;

ALTER ROLE qa_bi_reader LOGIN PASSWORD 'qa_bi_pass';
ALTER ROLE qa_bi_reader SET default_transaction_read_only = on;

GRANT CONNECT ON DATABASE qa_lab TO qa_bi_reader;
CREATE SCHEMA IF NOT EXISTS dbt_marts AUTHORIZATION qa_user;
GRANT USAGE ON SCHEMA dbt_marts TO qa_bi_reader;
