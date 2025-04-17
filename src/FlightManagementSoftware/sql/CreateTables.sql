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


CREATE TABLE Airline (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Name" NVARCHAR(100) NOT NULL,
    CreatedDate DateTime2 NOT NULL,
    DeletedDate DateTime2
);


CREATE TABLE Destination (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    CountryId INTEGER NOT NULL,
    "Name" NVARCHAR(100) NOT NULL,
    AirportCode NVARCHAR(3) UNIQUE, -- unique ignores nulls, could be null for private airfield for example
    Active BIT NOT NULL,
    CreatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2,

    FOREIGN KEY (CountryId) REFERENCES Country
);



-- This table defines the Destinations valid flight paths, when flights are to be created
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


CREATE Table Airplane (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    ModelNumber NVARCHAR(200) NOT NULL, 
    ManufacturedDate DATETIME2 NOT NULL, 
    LastServiceDate DATETIME2 NOT NULL, -- For newly added planes this will match CreatedDate
    PassengerCapacity INTEGER NOT NULL,
    CurrentDestinationId INTEGER,
    CreatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2,

    FOREIGN KEY (CurrentDestinationId) REFERENCES Destination
);


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


CREATE TABLE Flight (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    FlightPathId INTEGER NOT NULL,
    AirplaneId INTEGER NOT NULL,
    DepartureTimeUTC DATETIME2,
    ArrivalTimeUTC DATETIME2,
    CreatedDate DATETIME2 NOT NULL,
    DeletedDate DATETIME2,

    FOREIGN KEY (FlightPathId) REFERENCES FlightPath,
    FOREIGN KEY (AirPlaneId) REFERENCES Airplane
);


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