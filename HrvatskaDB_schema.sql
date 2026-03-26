-- ============================================================
-- HrvatskaDB_schema.sql
-- Kreiranje baze i tablica za HrvatskaDB projekt
-- Pokreni PRVO, prije HrvatskaDB_data.sql
-- ============================================================

CREATE DATABASE HrvatskaDB;
GO

USE HrvatskaDB;
GO

-- Tablica Zupanija
-- UNIQUE constraint sprječava duplikate naziva županija
CREATE TABLE Zupanija (
    Id    INT          IDENTITY(1,1) NOT NULL
          CONSTRAINT PK_Zupanija_Id    PRIMARY KEY,
    Naziv NVARCHAR(100) NOT NULL
          CONSTRAINT UQ_Zupanija_Naziv UNIQUE
);

-- Tablica Grad
-- CHECK constraint osigurava da stanovništvo ne može biti negativan broj
-- FOREIGN KEY veže svaki grad na županiju (referentni integritet)
CREATE TABLE Grad (
    Id           INT           IDENTITY(1,1) NOT NULL
                 CONSTRAINT PK_Grad_Id         PRIMARY KEY,
    Naziv        NVARCHAR(100) NOT NULL,
    Stanovnistvo INT           NOT NULL
                 CONSTRAINT CK_Grad_Stanovnistvo CHECK (Stanovnistvo >= 0),
    ZupanijaId   INT           NOT NULL
                 CONSTRAINT FK_Grad_Zupanija    FOREIGN KEY
                 REFERENCES Zupanija(Id)
);

-- Tablica Znamenitost
-- GodinaIzgradnje može biti NULL (nepoznata godina)
-- FOREIGN KEY veže svaku znamenitost na grad
CREATE TABLE Znamenitost (
    Id               INT           IDENTITY(1,1) NOT NULL
                     CONSTRAINT PK_Znamenitost_Id PRIMARY KEY,
    Naziv            NVARCHAR(200) NOT NULL,
    Tip              NVARCHAR(50),
    GodinaIzgradnje  INT,
    GradId           INT
                     CONSTRAINT FK_Znamenitost_Grad FOREIGN KEY
                     REFERENCES Grad(Id)
);
GO
