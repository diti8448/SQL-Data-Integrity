-- ============================================================
-- HrvatskaDB_data.sql
-- Unos podataka u HrvatskaDB
-- Pokreni NAKON HrvatskaDB_schema.sql
-- ============================================================

USE HrvatskaDB;
GO

-- Brisanje postojećih podataka (redoslijed: djeca prije roditelja)
DELETE FROM Znamenitost;
DELETE FROM Grad;
DELETE FROM Zupanija;

-- Resetiranje IDENTITY brojača (da ID-ovi kreću od 1)
DBCC CHECKIDENT ('Znamenitost', RESEED, 0);
DBCC CHECKIDENT ('Grad',        RESEED, 0);
DBCC CHECKIDENT ('Zupanija',    RESEED, 0);
GO

-- ============================================================
-- UNOS ŽUPANIJA
-- N prefiks je obavezan za ispravno spremanje hrvatskih znakova
-- ============================================================
INSERT INTO Zupanija (Naziv) VALUES
(N'Krapinsko-zagorska'),   -- Id = 1
(N'Grad Zagreb'),           -- Id = 2
(N'Zagrebačka'),            -- Id = 3
(N'Splitsko-dalmatinska'),  -- Id = 4
(N'Istarska');              -- Id = 5
GO

-- ============================================================
-- UNOS GRADOVA
-- ZupanijaId mora odgovarati ID-u iz tablice Zupanija
-- ============================================================
INSERT INTO Grad (Naziv, Stanovnistvo, ZupanijaId) VALUES
(N'Zabok',         8800,   1),  -- Id = 1, Krapinsko-zagorska
(N'Krapina',       12000,  1),  -- Id = 2, Krapinsko-zagorska
(N'Zagreb',        760000, 2),  -- Id = 3, Grad Zagreb
(N'Samobor',       37000,  3),  -- Id = 4, Zagrebačka
(N'Velika Gorica', 63000,  3),  -- Id = 5, Zagrebačka
(N'Split',         160000, 4),  -- Id = 6, Splitsko-dalmatinska
(N'Pula',          52000,  5);  -- Id = 7, Istarska
GO

-- ============================================================
-- UNOS ZNAMENITOSTI
-- GradId mora odgovarati ID-u iz tablice Grad
-- ============================================================
INSERT INTO Znamenitost (Naziv, Tip, GodinaIzgradnje, GradId) VALUES
(N'Dvorac Đalski',          N'Dvorac',     1750, 1),  -- Zabok
(N'Krapinski pračovjek',    N'Muzej',      1969, 2),  -- Krapina
(N'Zagrebačka katedrala',   N'Katedrala',  1217, 3),  -- Zagreb
(N'Stari grad Samobor',     N'Tvrđava',    1268, 4),  -- Samobor
(N'Dioklecijanova palača',  N'Palača',     305,  6),  -- Split
(N'Arena u Puli',           N'Amfiteatar', 27,   7);  -- Pula
GO
