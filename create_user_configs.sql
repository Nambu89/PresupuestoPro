-- Crear tabla de configuraciones de usuario
CREATE TABLE IF NOT EXISTS user_configs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    notification_email BOOLEAN DEFAULT TRUE,
    notification_sms BOOLEAN DEFAULT FALSE,
    language VARCHAR DEFAULT 'es',
    theme VARCHAR DEFAULT 'light',
    currency VARCHAR DEFAULT 'EUR'
);
