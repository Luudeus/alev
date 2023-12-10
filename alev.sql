CREATE DATABASE alev;
USE alev;

CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    RUT VARCHAR(12) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    permisos VARCHAR(20) NOT NULL,
    contrasenia VARCHAR(255) NOT NULL
);


INSERT INTO User (RUT, nombre, correo, telefono, direccion, permisos, contrasenia) VALUES 
('100122334', 'Juan Pérez', 'juanperez@mail.com', '12345678901', 'Calle 123', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('234567890', 'Ana Gómez', 'anagomez@mail.com', '12345678902', 'Avenida Principal', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('345678901', 'Carlos Ruiz', 'carlosruiz@mail.com', '12345678903', 'Calle Secundaria', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('456789012', 'María López', 'marialopez@mail.com', '12345678904', 'Calle 456', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('567890123', 'Lucía Hernández', 'luciahernandez@mail.com', '12345678905', 'Avenida Central', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('678901234', 'Miguel Ángel', 'miguelangel@mail.com', '12345678906', 'Calle 789', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('789012345', 'Sofía Martínez', 'sofiamartinez@mail.com', '12345678907', 'Avenida Norte', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('890123456', 'Diego Torres', 'diegotorres@mail.com', '12345678908', 'Calle 890', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('901234567', 'Andrea Jiménez', 'andreajimenez@mail.com', '12345678909', 'Avenida Sur', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('012345678', 'Roberto García', 'robertogarcia@mail.com', '12345678910', 'Calle 012', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('112233445', 'Sara Molina', 'saramolina@mail.com', '12345678911', 'Avenida Oeste', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('223344556', 'Luis Navarro', 'luisnavarro@mail.com', '12345678912', 'Calle 223', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('334455667', 'Marta Sánchez', 'martasanchez@mail.com', '12345678913', 'Avenida Este', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('445566778', 'Fernando Castro', 'fernandocastro@mail.com', '12345678914', 'Calle 445', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('556677889', 'Laura Ortiz', 'lauraortiz@mail.com', '12345678915', 'Avenida Final', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('667788990', 'Daniel Romero', 'danielromero@mail.com', '12345678916', 'Calle 667', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('778899001', 'Patricia Navarrete', 'patricianavarrete@mail.com', '12345678917', 'Avenida Inicial', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('889900112', 'Iván Morales', 'ivanmorales@mail.com', '12345678918', 'Calle 889', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('990011223', 'Carmen Díaz', 'carmendiaz@mail.com', '12345678919', 'Avenida Central', 'normal', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26'),
('123456789', 'Presidente', 'presidente@juntadevecinos.cl', '12345678920', 'Casa Central', 'admin', 'scrypt:32768:8:1$HzP950Lc5oxQ6Guw$b6ef14338b8db610ef345d05b18e268950380ae6c43e72f3c6a75d802ebd0a3b1c140fc0664a1cce270917f319abd80817bfc6b67d1f615c955c14801fb52e26');
