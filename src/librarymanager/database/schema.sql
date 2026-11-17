DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS book_authors;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS reservation_statuses;
DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL UNIQUE
);

CREATE TABLE reservation_statuses (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name    TEXT NOT NULL,
    last_name     TEXT NOT NULL,
    middle_name   TEXT,
    login         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id       INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles (role_id)
);

CREATE TABLE authors (
    author_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    middle_name TEXT
);

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title   TEXT NOT NULL,
    isbn    TEXT NOT NULL UNIQUE
);

CREATE TABLE book_authors (
    book_author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id      INTEGER NOT NULL,
    book_id        INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors (author_id),
    FOREIGN KEY (book_id)   REFERENCES books (book_id)
);

CREATE TABLE reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    librarian_id   INTEGER,
    reader_id      INTEGER NOT NULL,
    book_id        INTEGER NOT NULL,
    reserved_at    TEXT NOT NULL,
    status_id      INTEGER NOT NULL,
    FOREIGN KEY (librarian_id) REFERENCES users (user_id),
    FOREIGN KEY (reader_id)    REFERENCES users (user_id),
    FOREIGN KEY (book_id)      REFERENCES books (book_id),
    FOREIGN KEY (status_id)    REFERENCES reservation_statuses (status_id)
);

INSERT INTO roles (name)
VALUES
    ('Reader'),
    ('Librarian');

INSERT INTO reservation_statuses (name)
VALUES
    ('Active'),
    ('Returned'),
    ('Canceled');

INSERT INTO users (first_name, last_name, middle_name, login, password_hash, role_id)
VALUES
    ('Главный', 'Администратор', NULL, 'admin',
     '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 2),
    ('Иван', 'Петров', 'Сергеевич', 'reader',
     '3d0941964aa3ebdcb00ccef58b1bb399f9f898465e9886d5aec7f31090a0fb30', 1);

INSERT INTO authors (first_name, last_name, middle_name)
VALUES
    ('Лев',       'Толстой',     'Николаевич'),
    ('Фёдор',     'Достоевский', 'Михайлович'),
    ('Александр', 'Пушкин',      'Сергеевич'),
    ('Антон',     'Чехов',       'Павлович'),
    ('Михаил',    'Булгаков',    'Афанасьевич'),
    ('Николай',   'Гоголь',      'Васильевич');

INSERT INTO books (title, isbn)
VALUES
    ('Война и мир',             '978-5-17-000001-1'),
    ('Анна Каренина',           '978-5-17-000002-8'),
    ('Преступление и наказание','978-5-17-000003-5'),
    ('Идиот',                   '978-5-17-000004-2'),
    ('Евгений Онегин',          '978-5-17-000005-9'),
    ('Капитанская дочка',       '978-5-17-000006-6'),
    ('Вишнёвый сад',            '978-5-17-000007-3'),
    ('Мастер и Маргарита',      '978-5-17-000008-0'),
    ('Мёртвые души',            '978-5-17-000009-7'),
    ('Ревизор',                 '978-5-17-000010-3');

INSERT INTO book_authors (author_id, book_id)
VALUES
    (1, 1),   -- Толстой     - Война и мир
    (1, 2),   -- Толстой     - Анна Каренина
    (2, 3),   -- Достоевский - Преступление и наказание
    (2, 4),   -- Достоевский - Идиот
    (3, 5),   -- Пушкин      - Евгений Онегин
    (3, 6),   -- Пушкин      - Капитанская дочка
    (4, 7),   -- Чехов       - Вишнёвый сад
    (5, 8),   -- Булгаков    - Мастер и Маргарита
    (6, 9),   -- Гоголь      - Мёртвые души
    (6, 10);  -- Гоголь      - Ревизор

INSERT INTO reservations (librarian_id, reader_id, book_id, reserved_at, status_id)
VALUES
    (NULL, 2, 3, '2026-11-10 12:30:00', 1),
    (1,    2, 1, '2026-10-20 09:15:00', 2),
    (NULL, 2, 8, '2026-10-25 16:40:00', 3);
