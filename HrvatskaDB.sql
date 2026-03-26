CREATE DATABASE HrvatskaDB;
GO
USE HrvatskaDB;
GO

CREATE TABLE Zupanija (
    Id INT IDENTITY(1,1) NOT NULL 
	CONSTRAINT PK_Zupanija_Id PRIMARY KEY,
    Naziv NVARCHAR(100) NOT NULL 
	CONSTRAINT UQ_Zupanija_Naziv UNIQUE
);

CREATE TABLE Grad (
    Id INT IDENTITY(1,1) NOT NULL 
	CONSTRAINT PK_Grad_Id PRIMARY KEY,
    Naziv NVARCHAR(100) NOT NULL,
    Stanovnistvo INT NOT NULL 
	CONSTRAINT CK_Grad_Stanovnistvo CHECK (Stanovnistvo >= 0),
    ZupanijaId INT NOT NULL 
	CONSTRAINT FK_Grad_Zupanija FOREIGN KEY 
	REFERENCES Zupanija(Id)
);

INSERT INTO Zupanija (Naziv) VALUES ('Krapinsko-zagorska');
INSERT INTO Grad (Naziv, Stanovnistvo, ZupanijaId) 
VALUES ('Zabok', 8800, 1);
GO

USE HrvatskaDB;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Znamenitost')
BEGIN
    CREATE TABLE Znamenitost (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Naziv NVARCHAR(200) NOT NULL,
        Tip NVARCHAR(50), 
        GodinaIzgradnje INT,
        GradId INT FOREIGN KEY REFERENCES Grad(Id)
    );

    -- Ubacujemo testni podatak (1 je ID za Zabok koji smo ranije unijeli)
    INSERT INTO Znamenitost (Naziv, Tip, GodinaIzgradnje, GradId) 
    VALUES ('Dvorac Ðalski', 'Dvorac', 1750, 1);
END
GO