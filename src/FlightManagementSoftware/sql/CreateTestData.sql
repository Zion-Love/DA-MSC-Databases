-- Having Countries stored in a table like this means we can 
-- actively track which countries our Flight management software manages flights from / to
-- The idea being scalability of the software, if the flight management company expanded to a new country
-- we could add that in here , likewise should the need to scale down we can soft delete the corresponding country
-- in the unlikely event of a border lockdown an allowingflights bit is used
CREATE TABLE Country (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" NVARCHAR(100) NOT NULL,
    IsoCode NVARCHAR(3) NOT NULL UNIQUE,
    AllowingFlights BIT NOT NULL,
    CreatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2
);


INSERT INTO Country (Id, "Name", IsoCode , AllowingFlights, CreatedDate, DeletedDate) VALUES (1,'United Kingdom', 'GBR', 1, DATETIME('now'), NULL);
INSERT INTO Country (Id, "Name", IsoCode , AllowingFlights, CreatedDate, DeletedDate) VALUES (2,'France', 'FRA', 1, DATETIME('now'), NULL);
INSERT INTO Country (Id, "Name", IsoCode , AllowingFlights, CreatedDate, DeletedDate) VALUES (3,'Germany', 'DEU', 1, DATETIME('now'), NULL);
INSERT INTO Country (Id, "Name", IsoCode , AllowingFlights, CreatedDate, DeletedDate) VALUES (4,'North Korea', 'PRK', 0, DATETIME('now'), NULL);
INSERT INTO Country (Id, "Name", IsoCode , AllowingFlights, CreatedDate, DeletedDate) VALUES (5,'The Lost City of Atlantis', 'ATL', 0, DATETIME('1989-05-01'), DATETIME('2000-01-01'));
INSERT INTO Country (Id, "Name", IsoCode , AllowingFlights, CreatedDate, DeletedDate) VALUES (6,'Spain', 'SPA', 1, DATETIME('now'), NULL);


-- Airlines tend to be global companies for obvious reasons so 
CREATE TABLE Airline (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" NVARCHAR(100) NOT NULL,
    CreatedDate DateTime2 NOT NULL,
    DeletedDate DateTime2
);


INSERT INTO Airline (Id, "Name", CreatedDate, DeletedDate) VALUES (1,"AirTrainUK", DATETIME('now'), NULL);
INSERT INTO Airline (Id, "Name", CreatedDate, DeletedDate) VALUES (2,"FlyingLion", DATETIME('now'), NULL);
INSERT INTO Airline (Id, "Name", CreatedDate, DeletedDate) VALUES (3,"OurPlanesAlmostDontCrashCo", DATETIME('now'), NULL);
INSERT INTO Airline (Id, "Name", CreatedDate, DeletedDate) VALUES (4,"Tykes plastic planes", DATETIME('now'), NULL);
INSERT INTO Airline (Id, "Name", CreatedDate, DeletedDate) VALUES (5,"Flying Portaloo", DATETIME('now'), NULL);




CREATE TABLE Destination (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    CountryId INTEGER NOT NULL,
    "Name" NVARCHAR(100) NOT NULL,
    AirportCode NVARCHAR(3), -- can be null for things like private airfields
    Active BIT NOT NULL,
    CreatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2,

    FOREIGN KEY (CountryId) REFERENCES Country
);


-- UK Destinations
INSERT INTO Destination (Id, CountryId, "Name", AirportCode, Active, CreatedDate, DeletedDate) VALUES (1, 1, 'London Stansted', 'STN', 1, DATETIME('1943-08-07'), NULL);
INSERT INTO Destination (Id, CountryId, "Name", AirportCode, Active, CreatedDate, DeletedDate) VALUES (2, 1, 'London Heathrow', 'LHR', 1, DATETIME('1944-03-25'), NULL);
INSERT INTO Destination (Id, CountryId, "Name", AirportCode, Active, CreatedDate, DeletedDate) VALUES (3, 1, 'London Terminal Aerodrome', 'LCI', 0, DATETIME('1920-03-09'), DATETIME('1959-09-30'));



-- SPA Destinations
INSERT INTO Destination (Id, CountryId, "Name", AirportCode, Active, CreatedDate, DeletedDate) VALUES (4, 6, 'San Sebastian Flight School', NULL, 1, DATETIME('1987-01-09'), NULL);
INSERT INTO Destination (Id, CountryId, "Name", AirportCode, Active, CreatedDate, DeletedDate) VALUES (5, 6, 'Adolfo Suárez Madrid–Barajas Airport', 'MAD', 1, DATETIME('1987-01-09'), NULL);


-- FRA Destinations



-- This table defines the Airports valid flight paths, when flights are to be created
-- it must first check that it is a valid active flight path.
-- We could have certain flight paths blocked for various reasons 
-- such as airspace being shut down en route, or a specific airport
-- not accepting fligts at this time, this is marked here but Fligts to be scheduled should also respect 
-- both the To and From Airports Activeflag as well as the Airports countries AllowingFlights flag
CREATE TABLE FlightPath (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    FromDestinationId INTEGER NOT NULL,
    ToDestinationId INTEGER NOT NULL,
    DistanceKm INTEGER NOT NULL,
    Active BIT NOT NULL,
    CreatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2,

    FOREIGN KEY (FromDestinationId) REFERENCES Destination,
    FOREIGN KEY (ToDestinationId) REFERENCES Destination,
    CONSTRAINT Columns_Cannot_Be_Equal CHECK (FromDestinationId <> ToDestinationId)
);


-- London Stansted -> san sebastian
INSERT INTO FlightPath (Id, FromDestinationId, ToDestinationId, DistanceKm, Active, CreatedDate, DeletedDate) VALUES 
    (1, 1, 4, 930, 1, DATETIME('2001-03-21'), NULL);
-- San Sebastian -> London Stansted
INSERT INTO FlightPath (Id, FromDestinationId, ToDestinationId, DistanceKm, Active, CreatedDate, DeletedDate) VALUES 
    (2, 4, 1, 930, 1, DATETIME('1956-02-12'), NULL);
-- Madrid -> Heathrow
INSERT INTO FlightPath (Id, FromDestinationId, ToDestinationId, DistanceKm, Active, CreatedDate, DeletedDate) VALUES 
    (3, 5, 2, 1000, 1, DATETIME('2001-03-22'), NULL);
-- Heathrow -> Madrid
INSERT INTO FlightPath (Id, FromDestinationId, ToDestinationId, DistanceKm, Active, CreatedDate, DeletedDate) VALUES 
    (4, 2, 5, 1000, 1, DATETIME('2001-03-21'), NULL);
-- Madrid -> San Sebastian
INSERT INTO FlightPath (Id, FromDestinationId, ToDestinationId, DistanceKm, Active, CreatedDate, DeletedDate) VALUES 
    (5, 5, 4, 452, 1, DATETIME('2000-07-08'), NULL);


CREATE Table Airplane (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    ModelNumber NVARCHAR(200) NOT NULL, 
    ManufacturedDate DATETIME2 NOT NULL, 
    LastServiceDate DATETIME2 NOT NULL, -- For newly added planes this will match CreatedDate
    PassengerCapacity INTEGER NOT NULL,
    CurrentAirportId INTEGER,
    CreatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2,

    FOREIGN KEY (CurrentAirportId) REFERENCES Airport
);

INSERT INTO Airplane (Id, ModelNumber, ManufacturedDate, LastServiceDate, PassengerCapacity, CurrentAirportId, CreatedDate, DeletedDate) 
    VALUES (1, '1to87987ijh982', DATETIME('2001-01-01'), date('now'), 160, null, date('now'), null);
INSERT INTO Airplane (Id, ModelNumber, ManufacturedDate, LastServiceDate, PassengerCapacity, CurrentAirportId, CreatedDate, DeletedDate) 
    VALUES (2, 'aksnf92930g31', DATETIME('1987-01-01'), date('now'), 180, null, date('now'), null);
INSERT INTO Airplane (Id, ModelNumber, ManufacturedDate, LastServiceDate, PassengerCapacity, CurrentAirportId, CreatedDate, DeletedDate) 
    VALUES (3, 'klsmv92g02b009', DATETIME('1999-12-25'), date('now'), 200, null, date('now'), null);
INSERT INTO Airplane (Id, ModelNumber, ManufacturedDate, LastServiceDate, PassengerCapacity, CurrentAirportId, CreatedDate, DeletedDate) 
    VALUES (4, 'qgm29mg0393', DATETIME('2020-08-30'), date('now'), 80, null, date('now'), null);
INSERT INTO Airplane (Id, ModelNumber, ManufacturedDate, LastServiceDate, PassengerCapacity, CurrentAirportId, CreatedDate, DeletedDate) 
    VALUES (5, '08meb08nb404', DATETIME('2010-07-02'), date('now'), 4, 5, date('now'), null);


-- Pilots in most cases are employed by specific airlines , except in the case of private flights
-- since it was not mentioned in the brief I have not included hanlding for private flights
-- especially since private flights flight paths can get more complicated , having to dart around closed airspace much more frequently
-- due to lower flying altitude etc, the pilots of those aircrafts tend to submit flight plans to their destination bases
CREATE TABLE Pilot (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" NVARCHAR(100) NOT NULL,
    AirlineId INTEGER,
    CreatedDate DateTime2 NOT NULL,
    DeletedDate DateTime2
);

INSERT INTO Pilot (Id, "Name", AirlineId, CreatedDate, DeletedDate) VALUES (1, 'Steve Buscemi', 1, DATETIME('now'), NULL);
INSERT INTO Pilot (Id, "Name", AirlineId, CreatedDate, DeletedDate) VALUES (2, 'Daniel Radcliffe', 2, DATETIME('now'), NULL);
INSERT INTO Pilot (Id, "Name", AirlineId, CreatedDate, DeletedDate) VALUES (3, 'Dr. Strange Love', 1, DATETIME('2020-01-01'), NULL);
INSERT INTO Pilot (Id, "Name", AirlineId, CreatedDate, DeletedDate) VALUES (4, 'The forces of evil', 3, DATETIME('2022-10-25'), DATETIME('2023-05-02'));
INSERT INTO Pilot (Id, "Name", AirlineId, CreatedDate, DeletedDate) VALUES (5, 'Snakes in human clothing', 3, DATETIME('2020-02-14'), NULL);


CREATE TABLE Flight (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    FlightPathId INTEGER NOT NULL,
    AirPlaneId INTEGER NOT NULL,
    DepartureTimeUTC DATETIME2,
    ArrivalTimeUTC DATETIME2,
    CreatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2,

    FOREIGN KEY (FlightPathId) REFERENCES FlightPath,
    FOREIGN KEY (AirPlaneId) REFERENCES Airplane
);

INSERT INTO Flight (Id, FlightPathId, AirPlaneId, DepartureTimeUTC, ArrivalTimeUTC, CreatedDate, DeletedDate) VALUES
    (1, 1, 1, DATETIME('2025-06-02 12:45:00'), null, date('now'), null);
INSERT INTO Flight (Id, FlightPathId, AirPlaneId, DepartureTimeUTC, ArrivalTimeUTC, CreatedDate, DeletedDate) VALUES
    (2, 2, 1, DATETIME('2025-10-02 12:00:00'), null, date('now'), null);
INSERT INTO Flight (Id, FlightPathId, AirPlaneId, DepartureTimeUTC, ArrivalTimeUTC, CreatedDate, DeletedDate) VALUES
    (3, 3, 2, DATETIME('2020-01-23 12:45:00'), DATETIME('2020-01-23 15:00:32'), DATETIME('2020-01-01'), null);
INSERT INTO Flight (Id, FlightPathId, AirPlaneId, DepartureTimeUTC, ArrivalTimeUTC, CreatedDate, DeletedDate) VALUES
    (4, 4, 2, DATETIME('2020-02-01 09:36:00'), DATETIME('2020-02-01 12:32:22'), date('now'), null);
INSERT INTO Flight (Id, FlightPathId, AirPlaneId, DepartureTimeUTC, ArrivalTimeUTC, CreatedDate, DeletedDate) VALUES
    (5, 5, 3, DATETIME('2026-02-01 10:28:12'), null, date('now'), null);


-- This table details a many to many for pilot assignment to flights
-- I am aware most flights have 2-3 pilots but doing it this way allows us to 
-- have more if need be , for example if a junior is joining to 'shadow' their peers
CREATE TABLE PilotFlight (
    PilotId INTEGER NOT NULL,
    FlightId INTEGER NOT NULL,

    PRIMARY KEY (PilotId, FlightId),
    FOREIGN KEY (PilotId) REFERENCES Pilot,
    FOREIGN KEY (FlightId) REFERENCES Flight
);


INSERT INTO PilotFlight (PilotId, FlightId) VALUES (1,1);
INSERT INTO PilotFlight (PilotId, FlightId) VALUES (2,1);
INSERT INTO PilotFlight (PilotId, FlightId) VALUES (1,2);
INSERT INTO PilotFlight (PilotId, FlightId) VALUES (2,2);
INSERT INTO PilotFlight (PilotId, FlightId) VALUES (3,3);
INSERT INTO PilotFlight (PilotId, FlightId) VALUES (4,3);
INSERT INTO PilotFlight (PilotId, FlightId) VALUES (3,4);
INSERT INTO PilotFlight (PilotId, FlightId) VALUES (4,4);
INSERT INTO PilotFlight (PilotId, FlightId) VALUES (5,5);