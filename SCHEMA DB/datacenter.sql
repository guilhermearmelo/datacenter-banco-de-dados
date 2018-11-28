--CREATE SCHEMA Datacenter;
CREATE TABLE Staff
(
    Staff_ID        INTEGER PRIMARY KEY AUTOINCREMENT,
    SSN             CHAR(16)        NOT NULL,
    Name            VARCHAR(30)     NOT NULL,
    EMail           VARCHAR(30),
    Role            VARCHAR(30),
    JoinDate        DATE,
    Remuneration    DECIMAL(10,2)
);

CREATE TABLE Staff_Phones
(
    Staff_ID        CHAR(16) PRIMARY KEY NOT NULL,
    Phone           CHAR(12)        NOT NULL,
    CONSTRAINT FK_SSN FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);

CREATE TABLE Client
(
    Client_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
    Name            VARCHAR(30)     NOT NULL,
    EMail           VARCHAR(30)     NOT NULL,
    Country         VARCHAR(30),
    State           VARCHAR(30),
    City            VARCHAR(30),
    ZipCode         CHAR(14),
    Street          VARCHAR(30),
    AdNumber        INT
);

CREATE TABLE Company
(
    Client_ID       INTEGER     NOT NULL,
    CNPJ            CHAR(18)    NOT NULL,
    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
);

CREATE TABLE Person
(
    Client_ID       INTEGER        NOT NULL,
    CPF             CHAR(14)       NOT NULL,
    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
);

CREATE TABLE Client_Phones
(
    Phone           CHAR(10) PRIMARY KEY NOT NULL,
    Client_ID       INTEGER         NOT NULL,
    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
);

CREATE TABLE ClientBillingInfo
(
    Client_ID       INTEGER         NOT NULL,
    BillingInfo     CHAR(16)        PRIMARY KEY,
    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
);

CREATE TABLE Ticket
(
    Ticket_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
    Description     VARCHAR(140)    NOT NULL,
    Category        VARCHAR(10)     NOT NULL,
    OpeningDate     DATE            NOT NULL,
    ClosingDate     DATE,
    Staff_ID        CHAR(16),
    Client_ID       CHAR(8)         NOT NULL,
    CONSTRAINT FK_Staff_ID FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID),
    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
);

CREATE TABLE Ticket_Comments
(
    Comment_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
    Ticket_ID       INTEGER         NOT NULL,
    Commentary      VARCHAR(140)    NOT NULL,
    CONSTRAINT FK_Ticket_ID FOREIGN KEY (Ticket_ID) REFERENCES Ticket(Ticket_ID)
);

CREATE TABLE Datacenter
(
    Datacenter_ID   INTEGER PRIMARY KEY AUTOINCREMENT,
    Country         VARCHAR(30)     NOT NULL,
    State           VARCHAR(30)     NOT NULL,
    City            VARCHAR(30)     NOT NULL,
    Tier            INT             NOT NULL,
    CONSTRAINT Tier CHECK (Tier >= 1 or Tier <= 5)
);

CREATE TABLE Server
(
    Server_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
    IP              CHAR(15),
    MACAddress      CHAR(17),
    OperationalSystem   CHAR(20),
    MonthlyCost     DECIMAL(10,2),
    HourlyCost      DECIMAL(5,2)
);

CREATE TABLE Component
(
    Component_ID    INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE Model
(
    Model_ID        INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE CPUModel
(
    Model_ID        INTEGER,
    Type            VARCHAR(8),
    Size            VARCHAR(8),
    CoreSpeed       VARCHAR(8),
    Cores           VARCHAR(10),
    Cache           VARCHAR(8),
    CONSTRAINT FK_Model_ID FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID)
);

CREATE TABLE GPUModel
(
    Model_ID        INTEGER,
    Type            VARCHAR(8),
    Size            VARCHAR(8),
    CoreClock       VARCHAR(8),
    MemoryClock     VARCHAR(8),
    CONSTRAINT FK_Model_ID FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID)
);

CREATE TABLE RAMModel
(
    Model_ID        INTEGER,
    Type            VARCHAR(8),
    Size            VARCHAR(8),
    Speed           VARCHAR(8),
    CONSTRAINT FK_Model_ID FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID)
);

CREATE TABLE DiskModel
(
    Model_ID        INTEGER,
    Type            VARCHAR(8),
    Size            VARCHAR(8),
    WritingSpeed    VARCHAR(8),
    ReadingSpeed    VARCHAR(8),
    CONSTRAINT FK_Model_ID FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID)
);

CREATE TABLE Refers_To
(
    Ticket_ID       INTEGER         NOT NULL,
    Server_ID       INTEGER,
    CONSTRAINT FK_Server_ID FOREIGN KEY (Server_ID) REFERENCES Server(Server_ID),
    CONSTRAINT FK_Ticket_ID FOREIGN KEY (Ticket_ID) REFERENCES Ticket(Ticket_ID)
);

CREATE TABLE Rents
(
    Client_ID       INTEGER         NOT NULL,
    Server_ID       INTEGER         NOT NULL,
    CONSTRAINT FK_Server_ID FOREIGN KEY (Server_ID) REFERENCES Server(Server_ID),
    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
);

CREATE TABLE allocated_to
(
    Component_ID    INTEGER         NOT NULL,
    Server_ID       INTEGER         NOT NULL,
    CONSTRAINT FK_Server_ID FOREIGN KEY (Server_ID) REFERENCES Server(Server_ID),
    CONSTRAINT FK_Component_ID FOREIGN KEY (Component_ID) REFERENCES Component(Component_ID)
);

CREATE TABLE stored_at
(
    Component_ID    INTEGER         NOT NULL,
    Datacenter_ID   INTEGER         NOT NULL,
    CONSTRAINT FK_Component_ID FOREIGN KEY (Component_ID) REFERENCES Component(Component_ID),
    CONSTRAINT FK_Datacenter_ID FOREIGN KEY (Datacenter_ID) REFERENCES Datacenter(Datacenter_ID)
);

CREATE TABLE of_model
(
    Component_ID    INTEGER         NOT NULL,
    Model_ID        INTEGER         NOT NULL,
    CONSTRAINT FK_Component_ID FOREIGN KEY (Component_ID) REFERENCES Component(Component_ID),
    CONSTRAINT FK_Model_ID FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID)
);
