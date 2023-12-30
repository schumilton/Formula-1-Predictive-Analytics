-- Table structure for table "circuits"
DROP TABLE IF EXISTS circuits;
CREATE TABLE circuits (
  circuitId SERIAL PRIMARY KEY,
 -- circuitRef VARCHAR(255) NOT NULL DEFAULT '',
  name VARCHAR(255) NOT NULL DEFAULT '',
  location VARCHAR(255),
  country VARCHAR(255),
  lat FLOAT,
  lng FLOAT,
  alt INT,
  url VARCHAR(255) NOT NULL DEFAULT '',
    UNIQUE (url)
);

-- Table structure for table "status"
DROP TABLE IF EXISTS status;
CREATE TABLE status (
  statusId SERIAL PRIMARY KEY,
  status VARCHAR(255) NOT NULL DEFAULT '',
    UNIQUE (status)

);

-- Table structure for table "constructors"
DROP TABLE IF EXISTS constructors;
CREATE TABLE constructors (
  constructorId SERIAL PRIMARY KEY,
 -- constructorRef VARCHAR(255) NOT NULL DEFAULT '',
  name VARCHAR(255) NOT NULL DEFAULT '',
  nationality VARCHAR(255),
  url VARCHAR(255) NOT NULL DEFAULT '',
    UNIQUE (url,name)

);

-- Table structure for table "drivers"
DROP TABLE IF EXISTS drivers;
CREATE TABLE drivers (
  driverId SERIAL PRIMARY KEY,
  driverRef VARCHAR(255) NOT NULL DEFAULT '',
--  number INT,
  --code VARCHAR(3),
  forename VARCHAR(255) NOT NULL DEFAULT '',
  surname VARCHAR(255) NOT NULL DEFAULT '',
  dob DATE,
  nationality VARCHAR(255),
  url VARCHAR(255) NOT NULL DEFAULT '',
    UNIQUE (url,forename,surname)
);

-- Table structure for table "seasons"
DROP TABLE IF EXISTS seasons;
CREATE TABLE seasons (
  year INT PRIMARY KEY,
  url VARCHAR(255) NOT NULL DEFAULT '',
    UNIQUE (url)

);


-- Table structure for table "races"
DROP TABLE IF EXISTS races;
CREATE TABLE races (
  raceId SERIAL PRIMARY KEY,
  year INT NOT NULL DEFAULT '0',
  round INT NOT NULL DEFAULT '0',
  circuitId INT NOT NULL DEFAULT '0',
  name VARCHAR(255) NOT NULL DEFAULT '',
  date DATE NOT NULL DEFAULT '1970-01-01', -- Updated default date
  url VARCHAR(255),
  FOREIGN KEY (circuitId) REFERENCES circuits(circuitId),
Foreign KEY (year) REFERENCES seasons(year),
    UNIQUE (url, name)
);

-- Table structure for table "qualifying"
DROP TABLE IF EXISTS qualifying;
CREATE TABLE qualifying (
  qualifyId SERIAL PRIMARY KEY,
  raceId INT NOT NULL DEFAULT '0',
  driverId INT NOT NULL DEFAULT '0',
  constructorId INT NOT NULL DEFAULT '0',
  number INT NOT NULL DEFAULT '0',
  position INT,
  q1 TIME(3),
  q2 TIME(3),
  q3 TIME(3),
    UNIQUE (raceId,driverId,constructorId),
 FOREIGN KEY (constructorId)  REFERENCES constructors(constructorId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId),
    FOREIGN KEY (raceId) references races(raceId),
                        UNIQUE(qualifyId,raceId,driverId)
);


-- Table structure for table "results"
DROP TABLE IF EXISTS results;
CREATE TABLE results (
  resultId SERIAL PRIMARY KEY,
  raceId INT NOT NULL DEFAULT '0',
  driverId INT NOT NULL DEFAULT '0',
  constructorId INT NOT NULL DEFAULT '0',
  number INT,
  grid INT NOT NULL DEFAULT '0',
  position INT,
  positionText VARCHAR(255) NOT NULL DEFAULT '',
 -- positionOrder INT NOT NULL DEFAULT '0',
  points FLOAT NOT NULL DEFAULT '0',
  laps INT NOT NULL DEFAULT '0',
  time varchar(250),
 -- milliseconds INT,
  fastestLap INT,
  rank INT DEFAULT '0',
  fastestLapTime TIME(3),
  fastestLapSpeed VARCHAR(255),
  statusId INT NOT NULL DEFAULT '0',
    foreign key (statusId) REFERENCES status(statusId),
    FOREIGN KEY (raceId) references races(raceId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId),
    FOREIGN KEY (constructorId) REFERENCES constructors(constructorId),
    UNIQUE (raceId,driverId)

);

-- Table structure for table "sprintResults"
DROP TABLE IF EXISTS sprintResults;
CREATE TABLE sprintResults (
  sprintResultId SERIAL PRIMARY KEY,
  raceId INT NOT NULL DEFAULT '0',
  driverId INT NOT NULL DEFAULT '0',
  constructorId INT NOT NULL DEFAULT '0',
  number INT NOT NULL DEFAULT '0',
  grid INT NOT NULL DEFAULT '0',
  position INT,
  positionText VARCHAR(255) NOT NULL DEFAULT '',
--  positionOrder INT NOT NULL DEFAULT '0',
  points FLOAT NOT NULL DEFAULT '0',
  laps INT NOT NULL DEFAULT '0',
  time VARCHAR(255),
--  milliseconds INT,
  fastestLap INT,
  fastestLapTime VARCHAR(255),
  statusId INT NOT NULL DEFAULT '0',
  FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId),
    FOREIGN KEY (constructorId) REFERENCES  constructors(constructorId),
    foreign key (statusId) references status(statusId),
    UNIQUE (driverId,sprintResultId)
);

 --Table structure for table "constructorResults"
--DROP TABLE IF EXISTS constructorResults;
--CREATE TABLE constructorResults (
  --constructorResultsId SERIAL PRIMARY KEY,
 -- raceId INT NOT NULL DEFAULT '0',
--  constructorId INT NOT NULL DEFAULT '0',
--  points FLOAT,
--  statusId INT NOT NULL DEFAULT '0',
 --   FOREIGN KEY (raceId) REFERENCES races(raceId),
 --  FOREIGN KEY (constructorId) REFERENCES constructors(constructorId),
  --  foreign key (statusId) references status(statusId),
   --                            UNIQUE (raceId,constructorResultsId)
--);

--Table structure for table "constructorStandings"
DROP TABLE IF EXISTS constructorStandings;
CREATE TABLE constructorStandings
(
    constructorStandingsId SERIAL PRIMARY KEY,
    raceId                 INT   NOT NULL DEFAULT '0',
    constructorId          INT   NOT NULL DEFAULT '0',
    points                 FLOAT NOT NULL DEFAULT '0',
    position               INT,
    positionText           VARCHAR(255),
    wins                   INT   NOT NULL DEFAULT '0',
    FOREIGN KEY (raceId) REFERENCES races (raceId),
    FOREIGN KEY (constructorId) REFERENCES constructors (constructorId),
    Unique(raceId,constructorId)
);



-- Table structure for table "driverStandings"
DROP TABLE IF EXISTS driverStandings;
CREATE TABLE driverStandings (
driverStandingsId SERIAL PRIMARY KEY,
 raceId INT NOT NULL DEFAULT '0',
 driverId INT NOT NULL DEFAULT '0',
 points FLOAT NOT NULL DEFAULT '0',
 position INT,
 positionText VARCHAR(255),
 wins INT NOT NULL DEFAULT '0',
   FOREIGN KEY (raceId) REFERENCES races(raceId),
   FOREIGN KEY (driverId) REFERENCES drivers(driverId),
    unique (raceId,driverId)
);






-- Table structure for table "lapTimes"
DROP TABLE IF EXISTS lapTimes;
CREATE TABLE lapTimes (
  raceId INT NOT NULL,
  driverId INT NOT NULL,
  lap INT NOT NULL,
  position INT,
  time VARCHAR(255),
  milliseconds INT,
  PRIMARY KEY (raceId, driverId, lap),
  FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId),
                      unique(raceId,driverId,lap)
);

-- Table structure for table "pitStops"
DROP TABLE IF EXISTS pitStops;
CREATE TABLE pitStops (
  raceId INT NOT NULL,
  driverId INT NOT NULL,
  stop INT NOT NULL,
  lap INT NOT NULL,
  time TIME NOT NULL,
  duration VARCHAR(255),
  milliseconds INT,
  PRIMARY KEY (raceId, driverId, stop),
  FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId),
    unique (raceId,driverId,stop)
);




--INSERT INTO circuits (name,location,country,lat, lng,alt, url)
           --                          VALUES ('test','germany','germany',23.0,3.0,2.0,'eewr')




