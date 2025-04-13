-- Insertar configuraciones predeterminadas para usuarios existentes
INSERT INTO user_configs (user_id, notification_email, notification_sms, language, theme, currency)
SELECT id, TRUE, FALSE, 'es', 'light', 'EUR'
FROM users
WHERE id NOT IN (SELECT user_id FROM user_configs);
