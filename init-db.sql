-- Create tables if not handled by FastAPI (optional, as FastAPI creates them)
-- But can be used for initial data seeding

CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR,
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert admin user if not exists
INSERT INTO public.users (email, hashed_password) 
VALUES ('admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW') 
ON CONFLICT (email) DO NOTHING;
