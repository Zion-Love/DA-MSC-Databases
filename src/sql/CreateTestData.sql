CREATE TABLE Pilot (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" VARCHAR(100) NOT NULL,
    CreatedDate DateTime2 NOT NULL,
    DeletedDate DateTime2
);

INSERT INTO Pilot (Id, "Name", CreatedDate, DeletedDate) VALUES (1, 'Steve Buscemi', DATETIME('now'),NULL);
INSERT INTO Pilot (Id, "Name", CreatedDate, DeletedDate) VALUES (2, 'Daniel Radcliffe', DATETIME('now'),NULL);
INSERT INTO Pilot (Id, "Name", CreatedDate, DeletedDate) VALUES (3, 'Dr. Strange Love', DATETIME('2020-01-01') ,NULL);
INSERT INTO Pilot (Id, "Name", CreatedDate, DeletedDate) VALUES (4, 'The forces of evil', DATETIME('2022-10-25'), DATETIME('2023-05-02'));
INSERT INTO Pilot (Id, "Name", CreatedDate, DeletedDate) VALUES (5, 'Snakes in human clothing', DATETIME('2020-02-14'), NULL);


CREATE TABLE Country (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" NVARCHAR(100) NOT NULL,
    IsoCode NVARCHAR(3) NOT NULL UNIQUE,
    AllowingFlights BIT NOT NULL,
    CreatedDate DATETIME2,
    DeletedDate DATETIME2
);

INSERT INTO Country (Id, "Name", IsoCode , AllowingFlights, CreatedDate, DeletedDate) VALUES (1,'United Kingdom', 'GBR', 1, DATETIME('now'), NULL);
INSERT INTO Country (Id, "Name", IsoCode , AllowingFlights, CreatedDate, DeletedDate) VALUES (2,'France', 'FRA', 1, DATETIME('now'), NULL);
INSERT INTO Country (Id, "Name", IsoCode , AllowingFlights, CreatedDate, DeletedDate) VALUES (3,'Germany', 'DEU', 1, DATETIME('now'), NULL);
INSERT INTO Country (Id, "Name", IsoCode , AllowingFlights, CreatedDate, DeletedDate) VALUES (4,'North Korea', 'PRK', 0, DATETIME('now'), NULL);
INSERT INTO Country (Id, "Name", IsoCode , AllowingFlights, CreatedDate, DeletedDate) VALUES (5,'The Lost City of Atlantis', 'ATL', 1, DATETIME('1989-05-01'), DATETIME('2000-01-01'));


CREATE TABLE Airport (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    CountryId INTEGER NOT NULL,
    "Name" NVARCHAR(100) NOT NULL,
    AirportCode NVARCHAR(3) NOT NULL,
    Active BIT NOT NULL,
    CreatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2,

    FOREIGN KEY (CountryId) REFERENCES Country
);

-- UK Airports
INSERT INTO Airport (Id, CountryId, "Name", AirportCode, Active, CreatedDate, DeletedDate) VALUES (1, 1, 'London Stansted', 'STN', 1, DATETIME('1943-08-07'), NULL);
INSERT INTO Airport (Id, CountryId, "Name", AirportCode, Active, CreatedDate, DeletedDate) VALUES (2, 1, 'London Heathrow', 'LHR', 1, DATETIME('1944-03-25'), NULL);
INSERT INTO Airport (Id, CountryId, "Name", AirportCode, Active, CreatedDate, DeletedDate) VALUES (3, 1, 'London Terminal Aerodrome', 'LCI', 0, DATETIME('1920-03-09'), DATETIME('1959-09-30'));


CREATE Table Airplane (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    ModelNumber INTEGER NOT NULL,
    Airline NVARCHAR(100) NOT NULL, -- really could be another table for airline info...
    LastServiceDate DATETIME2 NOT NULL, -- For newly added planes this will match CreatedDate
    PassengerCapacity INTEGER NOT NULL,
    CurrentAirportId INTEGER, -- NULL for deleted airplanes / in service...
    CeatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2,

    FOREIGN KEY (CurrentAirportId) REFERENCES Airport
);


CREATE TABLE Flight (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    DepartureAirportId INTEGER NOT NULL,
    ArrivalAirportId INTEGER NOT NULL,
    AirPlaneId INTEGER NOT NULL,
    AirMiles INTEGER NOT NULL,
    DepartureTimeUTC DATETIME2,
    ArrivalTimeUTC DATETIME2
    CreatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2,

    FOREIGN KEY (DepartureAirportId) REFERENCES Airport,
    FOREIGN KEY (ArrivalAirportId) REFERENCES Airport,
    FOREIGN KEY (AirPlaneId) REFERENCES Airplane
);


CREATE TABLE FlightHistory (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    FlightId INTEGER NOT NULL,
    DepartureTime DATETIME2 NOT NULL,
    ArrivalTime DATETIME2, -- This can be null when a flight gets cancelled
    CreatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2,

    FOREIGN KEY (FlightId) REFERENCES Flight
);


-- This table details a many to many for pilot assignment to flights
-- I am aware most flights have 2-3 pilots but doing it this way allows us to 
-- have more if need be , for example if a junior is joining to 'shadow' their peers
CREATE TABLE PilotFlight (
    PilotId INTEGER NOT NULL,
    FlightId INTEGER NOT NULL,


    PRIMARY KEY (PilotId, FlightId),
    FOREIGN KEY (PilotId) REFERENCES Pilot ON DELETE CASCADE,
    FOREIGN KEY (FlightId) REFERENCES Flight ON DELETE CASCADE
);