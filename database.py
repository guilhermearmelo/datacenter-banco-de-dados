#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3

DATABASE = 'database.db'
DATABASE_URI = 'sqlite:///'+DATABASE

DBSession = None

def session():
	if DBSession:
		return DBSession
	else:
		DBSession = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

def sql(command, params=None):
	if sqlite3.complete_statement(command) or params:
		#connection = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		connection = sqlite3.connect(DATABASE)
		cursor = connection.cursor()
		if params:
			cursor.execute(command, params)
		else:
			cursor.execute(command)
		connection.commit()
		return cursor.fetchall()
	else:
		print command + ' is not a valid sql command'
		return None

def init_database():
	connection = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
	cursor = connection.cursor()
	sql_createdb=\
	"""CREATE TABLE Staff(
		    Staff_ID        INTEGER PRIMARY KEY AUTOINCREMENT,
		    SSN             VARCHAR(16)        NOT NULL,
		    Name            VARCHAR(30)     NOT NULL,
		    Email           VARCHAR(30),
		    Role            VARCHAR(30),
		    JoinDate        DATE,
		    Remuneration    DECIMAL(10,2)
		);

		CREATE TABLE Staff_Phones(
		    Staff_ID        VARCHAR(16) 		NOT NULL,
		    Phone           VARCHAR(12)        PRIMARY KEY NOT NULL,
		    CONSTRAINT FK_SSN FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
		);

		CREATE TABLE Client(
		    Client_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
		    Name            VARCHAR(30)     NOT NULL,
		    Email           VARCHAR(30)     NOT NULL,
		    Country         VARCHAR(30),
		    State           VARCHAR(30),
		    City            VARCHAR(30),
		    ZipCode         VARCHAR(14),
		    Street          VARCHAR(30),
		    AdNumber        INT
		);

		CREATE TABLE Company(
		    Client_ID       INTEGER     NOT NULL,
		    CNPJ            VARCHAR(18)    NOT NULL,
		    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
		);

		CREATE TABLE Person(
		    Client_ID       INTEGER        NOT NULL,
		    CPF             VARCHAR(14)       NOT NULL,
		    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
		);

		CREATE TABLE Client_Phones(
		    Client_ID       INTEGER         NOT NULL,
		    Phone           VARCHAR(10) PRIMARY KEY NOT NULL,
		    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
		);

		CREATE TABLE ClientBillingInfo(
		    Client_ID       INTEGER         NOT NULL,
		    BillingInfo     VARCHAR(16)        PRIMARY KEY,
		    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
		);

		CREATE TABLE Ticket(
		    Ticket_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
		    Description     VARCHAR(140)    NOT NULL,
		    Category        VARCHAR(10)     NOT NULL,
		    OpeningDate     DATE            NOT NULL,
		    ClosingDate     DATE,
		    Staff_ID        VARCHAR(16),
		    Client_ID       VARCHAR(8)         NOT NULL,
		    CONSTRAINT FK_Staff_ID FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID),
		    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
		);

		CREATE TABLE Ticket_Comments(
		    Comment_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
		    Ticket_ID       INTEGER         NOT NULL,
		    Commentary      VARCHAR(140)    NOT NULL,
		    CONSTRAINT FK_Ticket_ID FOREIGN KEY (Ticket_ID) REFERENCES Ticket(Ticket_ID)
		);

		CREATE TABLE Datacenter(
		    Datacenter_ID   INTEGER PRIMARY KEY AUTOINCREMENT,
		    Country         VARCHAR(30)     NOT NULL,
		    State           VARCHAR(30)     NOT NULL,
		    City            VARCHAR(30)     NOT NULL,
		    Tier            INT             NOT NULL,
		    CONSTRAINT Tier CHECK (Tier >= 1 or Tier <= 5)
		);

		CREATE TABLE Server(
		    Server_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
		    IP              VARCHAR(15),
		    MACAddress      VARCHAR(17),
		    OperationalSystem   VARCHAR(20),
		    MonthlyCost     DECIMAL(10,2),
		    HourlyCost      DECIMAL(5,2)
		);

		CREATE TABLE Component(
		    Component_ID    INTEGER PRIMARY KEY AUTOINCREMENT
		);

		CREATE TABLE Model(
		    Model_ID        INTEGER PRIMARY KEY AUTOINCREMENT
		);

		CREATE TABLE CPUModel(
		    Model_ID        INTEGER,
		    Type            VARCHAR(8),
		    Size            VARCHAR(8),
		    CoreSpeed       VARCHAR(8),
		    Cores           VARCHAR(10),
		    Cache           VARCHAR(8),
		    CONSTRAINT FK_Model_ID FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID)
		);

		CREATE TABLE GPUModel(
		    Model_ID        INTEGER,
		    Type            VARCHAR(8),
		    Size            VARCHAR(8),
		    CoreClock       VARCHAR(8),
		    MemoryClock     VARCHAR(8),
		    CONSTRAINT FK_Model_ID FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID)
		);

		CREATE TABLE RAMModel(
		    Model_ID        INTEGER,
		    Type            VARCHAR(8),
		    Size            VARCHAR(8),
		    Speed           VARCHAR(8),
		    CONSTRAINT FK_Model_ID FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID)
		);

		CREATE TABLE DiskModel(
		    Model_ID        INTEGER,
		    Type            VARCHAR(8),
		    Size            VARCHAR(8),
		    WritingSpeed    VARCHAR(8),
		    ReadingSpeed    VARCHAR(8),
		    CONSTRAINT FK_Model_ID FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID)
		);

		CREATE TABLE Refers_To(
		    Ticket_ID       INTEGER         NOT NULL,
		    Server_ID       INTEGER,
		    CONSTRAINT FK_Server_ID FOREIGN KEY (Server_ID) REFERENCES Server(Server_ID),
		    CONSTRAINT FK_Ticket_ID FOREIGN KEY (Ticket_ID) REFERENCES Ticket(Ticket_ID)
		);

		CREATE TABLE Rents(
		    Client_ID       INTEGER         NOT NULL,
		    Server_ID       INTEGER         NOT NULL,
		    CONSTRAINT FK_Server_ID FOREIGN KEY (Server_ID) REFERENCES Server(Server_ID),
		    CONSTRAINT FK_Client_ID FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
		);

		CREATE TABLE allocated_to(
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
		);"""
	#connection.execute('CREATE TABLE {tn} ({nf} {ft})'\
    #    .format(tn=table_name1, nf=new_field, ft=field_type))
   	connection.executescript(sql_createdb)
	connection.commit()
	connection.close()
	print 'Database created'
	populate_database()

def populate_database():
	connection = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
	cursor = connection.cursor()
	sql_createdb=\
	script = """
		INSERT INTO Staff ( SSN, Name,  Role, JoinDate, Remuneration )
		VALUES ( '941.167.345-78', 'Luis Filipe Vieira', 'Hardware Engineer', '04/02/2014', 10120.00 );
		INSERT INTO Staff ( SSN, Name,  Role, JoinDate, Remuneration )
		VALUES ( '283.512.515-93', 'Guilherme Melo', 'DB Administrator', '03/11/2013', 10120.01 );
		INSERT INTO Staff ( SSN, Name,  Role, JoinDate, Remuneration )
		VALUES ( '646.813.820-51', 'Danilo Machado', 'Hardware Engineer', '12/02/2013', 10120.00 );
		INSERT INTO Staff ( SSN, Name,  Role, JoinDate, Remuneration )
		VALUES ( '116.982.341-63', 'Alberto Oliveira', 'Software Engineer', '10/10/2010', 10120.00 );
		INSERT INTO Staff ( SSN, Name,  Role, JoinDate, Remuneration )
		VALUES ( '415.040.390-25', 'Matheus Andrade', 'DBA Intern', '24/04/2016', 1800.00 );
		INSERT INTO Staff ( SSN, Name,  Role, JoinDate, Remuneration )
		VALUES ( '825.911.329-50', 'Gabrielle Maito', 'Psychiatrist', '20/01/2000', 9000.00 );

		INSERT INTO Staff_Phones
		VALUES ( 1, '313536301066' );
		INSERT INTO Staff_Phones
		VALUES ( 2, '318293201066' );
		INSERT INTO Staff_Phones
		VALUES ( 2, '313741372466' );
		INSERT INTO Staff_Phones
		VALUES ( 4, '313742361066' );
		INSERT INTO Staff_Phones
		VALUES ( 3 , '313742148766' );
		INSERT INTO Staff_Phones
		VALUES ( 6 , '319320142266' );
		INSERT INTO Staff_Phones
		VALUES ( 5, '313435201066' );
		INSERT INTO Staff_Phones
		VALUES ( 1, '318804956866' );

		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'Joao das Neves', 'jneves@muralha.com', 'Westeros', 'The North', 'Winterfell', '35490-000', 'Rua dos Stark', 1 );
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'Tio Patinhas', 'patinhas@bancopatinhas.com', 'Estados Unidos', 'Patomar', 'Patopolis', '36420-000', 'Rua do Banco Caixa Forte', 123 );
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'Umbrella Corporation', 'umbrella@umbrellacorp.com', 'Estados Unidos', 'Wisconsin', 'Raccon City', '20201-020', 'Rua da Colmeia', 329 );
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'Empreendimentos S.A.',  'falecom@empreendimentossa.com', 'Brasil', 'Minas Gerais', 'Ouro Preto', '30310-000', 'Pca Tiradentes', 213 );
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'Andorinhas Linhas Aereas', 'contato@voeandorinhas.com', 'Brasil', 'Sao Paulo', 'Sao Paulo', '10210-900','Av Sumare', 3420 );
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'U. F. de Ouro Preto', 'ufop@ufop.br', 'Brasil', 'Minas Gerais', 'Ouro Preto', '35690-000', 'Campus Universitario', 1);
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'HUMBURGUERIA 2.0',  'contato@hamb20.com.br', 'Brasil', 'Minas Gerais', 'Ouro Preto', '35690-000', 'Rua Direita', 999 );
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'ELKay Mix Producoes',  'lucblaster@hotmail.com', 'Brasil', 'Minas Gerais', 'Ouro Branco', '36420-000', 'Rua Queiroz Junior', 6 );
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'Centro de Pesquisa KT8',  'KT8@search.gov.br', 'Brasil', 'Sao Paulo', 'Sao Paulo', '10210-900', 'Av Paulista', 5435 );
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'Eletronica COSMOS',  'eletrocosmos@gmail.com', 'Brasil', 'Minas Gerais', 'Ouro Branco', '36420-000', 'Rua da Lavoura', 333 );
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'Casa de Carnes Joao da Alcatra',  'CCJA@gmail.com', 'Brasil', 'Minas Gerais', 'Sao Joao Del Rey', '34789-230', 'Rua dos Velhos', 4353);
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'Etiquepress', 'etiquepress@etiquepress.com.br', 'Brasil', 'Sao Paulo', 'Sao Bernardo do Campo', '54323-902', 'Rua Rudge Ramos', 345);
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'Evolution Informatica', 'evo@info.com', 'Brasil', 'Minas Gerais', 'Belo Horizonte', '12335-111', 'Rua Horizonte Belo', 910);
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ( 'Meridional Interiores', 'meridionalinteriores@hotmail.com','Brasil','Minas Gerais','Varginha', '99920-000', 'Rua Dallas', 501);
		INSERT INTO Client (Name, Email, Country, State, City, ZipCode, Street, AdNumber)
		VALUES ('Joaquim Silverio dos Reis X9',  'joaquimsilverio@x9.com', 'Brasil', 'Minas Gerais', 'Tiradentes', '35715-372', 'Rua Quatro de Abril', 616);


		INSERT INTO Company
		VALUES ( '192300', '95.988.457/0001-62' );
		INSERT INTO Company
		VALUES ( '84012', '74.551.433/0001-71' );
		INSERT INTO Company
		VALUES ( '321901', '18.116.445/0001-05' );
		INSERT INTO Company
		VALUES ( '12392', '13.962.611/0001-62' );
		INSERT INTO Company
		VALUES ( '65382', '56.482.289/0001-87' );
		INSERT INTO Company
		VALUES (  '242424', '47.551.206/0001-73' );
		INSERT INTO Company
		VALUES (  '15839', '53.118.201/0001-54' );
		INSERT INTO Company
		VALUES (  '33331', '56.887.250/0001-40' );
		INSERT INTO Company
		VALUES (  '11753', '73.166.461/0001-02' );
		INSERT INTO Company
		VALUES (  '68782', '97.854.097/0001-31' );
		INSERT INTO Company
		VALUES (  '90909', '51.651.488/0001-58' );
		INSERT INTO Company
		VALUES (  '89033', '15.446.185/0001-30' );


		INSERT INTO Person
		VALUES (  '697538', '739.831.025-06' );
		INSERT INTO Person
		VALUES ( '192303', '814.450.401-15' );
		INSERT INTO Person
		VALUES ( '19212', '278.120.602-41' );

		INSERT INTO Client_Phones
		VALUES ( '192300', '3192341020' );
		INSERT INTO Client_Phones
		VALUES ( '84012', '3138429420' );
		INSERT INTO Client_Phones
		VALUES ( '321901', '3175291020' );
		INSERT INTO Client_Phones
		VALUES ( '12392', '3237422029' );
		INSERT INTO Client_Phones
		VALUES ( '192303', '1131110101' );
		INSERT INTO Client_Phones
		VALUES ( '19212', '2132310001' );
		INSERT INTO Client_Phones
		VALUES ( '12392', '3132322029' );
		INSERT INTO Client_Phones
		VALUES ( '192303', '1131111001' );
		INSERT INTO Client_Phones
		VALUES ( '19212', '2132310002' );
		INSERT INTO Client_Phones
		VALUES (  '242424', '4356748391' );
		INSERT INTO Client_Phones
		VALUES (  '15839', '6578961123' );
		INSERT INTO Client_Phones
		VALUES (  '33331', '8778698743' );
		INSERT INTO Client_Phones
		VALUES (  '11753', '9167483919' );
		INSERT INTO Client_Phones
		VALUES (  '68782', '9368794711' );
		INSERT INTO Client_Phones
		VALUES (  '90909', '5490831739' );
		INSERT INTO Client_Phones
		VALUES (  '89033', '3758691748' );
		INSERT INTO Client_Phones
		VALUES (  '697538', '1658395816' );


		INSERT INTO ClientBillingInfo
		VALUES ( '192300', '6011391370288000' );
		INSERT INTO ClientBillingInfo
		VALUES ( '84012', '352276105067862' );
		INSERT INTO ClientBillingInfo
		VALUES ( '321901', '5217886638454496' );
		INSERT INTO ClientBillingInfo
		VALUES ( '12392', '5515785612858145' );
		INSERT INTO ClientBillingInfo
		VALUES ( '192303', '6011968033194038' );
		INSERT INTO ClientBillingInfo
		VALUES ( '19212', '4672915937202263' );
		INSERT INTO ClientBillingInfo
		VALUES ( '192300', '5337179781388371' );
		INSERT INTO ClientBillingInfo
		VALUES ( '84012', '344665269679382' );
		INSERT INTO ClientBillingInfo
		VALUES ( '321901', '6011623436696010' );
		INSERT INTO ClientBillingInfo
		VALUES (  '242424', '4996533181058296' );
		INSERT INTO ClientBillingInfo
		VALUES (  '15839', '4889805216492835' );
		INSERT INTO ClientBillingInfo
		VALUES (  '33331', '5175828570552952' );
		INSERT INTO ClientBillingInfo
		VALUES (  '11753', '366837523124322' );
		INSERT INTO ClientBillingInfo
		VALUES (  '68782', '6011749371450509' );
		INSERT INTO ClientBillingInfo
		VALUES (  '90909', '4153647262264547' );
		INSERT INTO ClientBillingInfo
		VALUES (  '89033', '5137090067821344' );
		INSERT INTO ClientBillingInfo
		VALUES (  '697538', '5296849571386194' );
		INSERT INTO ClientBillingInfo
		VALUES (  '68782', '347380534184492' );
		INSERT INTO ClientBillingInfo
		VALUES (  '90909', '6011127313356284' );
		INSERT INTO ClientBillingInfo
		VALUES (  '89033', '5146567592540035' );
		INSERT INTO ClientBillingInfo
		VALUES (  '697538', '4025604809804836' );

		INSERT INTO Ticket
		VALUES ( '192303', 'Solicito o reparo dos meus servidores', 'Manutencao',
		    '20/7/2016', null, null, '84012' );
		INSERT INTO Ticket
		VALUES ( '192304', 'Preciso que seja instalado nos meus servidores GPUs Nvidia GTX1080',
		     'Upgrade', '22/7/2016', null, '116.982.341-63', '12392'  );
		INSERT INTO Ticket
		VALUES ( '192300', 'Solicito a segunda via do boleto', 'Pagamento', '10/2/2016',
		    '11/2/2016', '825.911.329-50', '192303' );
		INSERT INTO Ticket
		VALUES ( '19212', 'Necessito de mais memoria RAM nos meus servidores, de preferencia as Kingston HyperX 1333', 'Upgrade',
		    '30/8/2015', '2/9/2015', '283.512.515-93', '192300' );

		INSERT INTO Ticket_Comments
		VALUES(1, '192304', 'Gostaria de um orcamento de upgrade para 60TB de armazenamento.');
		INSERT INTO Ticket_Comments
		VALUES(2, '192304', 'Opcoes Upgrade com SATA com 12 HDs Seagate 4TB R$ 3600,00\n12 HDs Western Digital 4TB R$ 4200,00\n10 HDs Samsung 6TB R$ 5000,00');
		INSERT INTO Ticket_Comments
		VALUES(3, '192304', 'Opcoes Upgrade com SSD com 256 HDs Kingston 240GB R$ 74260,00\n256 HDs Sandisk 240GB R$ 72960,00\n60 HDs Samsung 1TB R$ 96940,00');
		INSERT INTO Ticket_Comments
		VALUES(4, '192304', 'Pode ser os HDS SSD Sandisk. Obrigado' );
		INSERT INTO Ticket_Comments
		VALUES(5, '192304', 'Sera disponibilizado em seu servidor em ate 2 dias uteis. Algo mais em que posso ajudar?');
		INSERT INTO Ticket_Comments
		VALUES (6, '19212', 'Prezado Cliente nao possuimos essa memoria em estoque no momento, faremos a solicitacao.' );
		INSERT INTO Ticket_Comments
		VALUES (7, '19212', 'Tenho pressa para o upgrade liste as memorias disponiveis. Obrigado' );
		INSERT INTO Ticket_Comments
		VALUES (8, '19212', 'Temos disponiveis: Kingston HyperX Cloud e Corsair Vengeance' );
		INSERT INTO Ticket_Comments
		VALUES (9, '19212', 'Prefiro a Corsair Vengeance, favor disponibilizar 24GB' );
		INSERT INTO Ticket_Comments
		VALUES (10, '19212', 'Sera disponibilizado em seu servidor em ate 2 dias uteis' );
		INSERT INTO Ticket_Comments
		VALUES (11, '19212', 'Ok no aguardo. Obrigado' );
		INSERT INTO Ticket_Comments
		VALUES (12, '19212', 'Tudo certo a memoria foi instalada em seu servidor. Caso tenha outra solicitacao abra outro ticket no sistema' );

		INSERT INTO Datacenter
		VALUES ( 1, 'Noruega', 'Kvaloya', 'Mjelde', 1 );
		INSERT INTO Datacenter
		VALUES ( 2, 'Suecia', 'Uppland', 'Uppsala', 5 );
		INSERT INTO Datacenter
		VALUES ( 3, 'Suecia', 'Escania', 'Malmo', 3 );
		INSERT INTO Datacenter
		VALUES ( 4, 'Irlanda', 'Munster', 'Cork', 4 );
		INSERT INTO Datacenter
		VALUES ( 5, 'Franca', 'Comuna Francesa', 'Nice', 2 );
		INSERT INTO Datacenter
		VALUES ( 6, 'Emirados Arabes Unidos', 'Emirado de Dubai', 'Dubai', 3 );
		INSERT INTO Datacenter
		VALUES ( 7, 'Nova Zelandia', 'Otago', 'Dunedin', 3 );
		INSERT INTO Datacenter
		VALUES ( 8, 'Japao', 'Hokkaido', 'Wakkanai', 2 );
		INSERT INTO Datacenter
		VALUES ( 9, 'Coreia do Sul', 'Hoseo', 'Daejeon', 4 );
		INSERT INTO Datacenter
		VALUES ( 10, 'Brasil', 'Parana', 'Cascavel', 5 );
		INSERT INTO Datacenter
		VALUES ( 11, 'Brasil', 'Rio de Janeiro', 'Petropolis', 2 );
		INSERT INTO Datacenter
		VALUES ( 12, 'Estados Unidos', 'California', 'Menlo Park', 1 );
		INSERT INTO Datacenter
		VALUES ( 13, 'Estados Unidos', 'Maine', 'Lewiston', 4 );
		INSERT INTO Datacenter
		VALUES ( 14, 'Canada', 'Columbia Britanica', 'Vancouver', 2 );
		INSERT INTO Datacenter
		VALUES ( 15, 'Canada', 'Ontario', 'Toronto', 5 );
		INSERT INTO Datacenter
		VALUES ( 16, 'Estados Unidos', 'Florida', 'Tampa', 3 );
		INSERT INTO Datacenter
		VALUES ( 17, 'Brasil', 'Minas Gerais', 'Ouro Branco', 4 );
		INSERT INTO Datacenter
		VALUES ( 18, 'Inglaterra', 'Lancashire', 'BlackBurn', 2 );
		INSERT INTO Datacenter
		VALUES ( 19, 'Inglaterra', 'Cornualha', 'Liskeard', 1 );
		INSERT INTO Datacenter
		VALUES ( 20, 'Mexico', 'San Luis Potosi', 'San Luis Potosi', 1 );


		INSERT INTO Server VALUES ( 1, '127.0.0.1', 'F4-3A-FD-9A-F2-17' , 'Linux', 10.5, 3.5);
		INSERT INTO Server VALUES (15, '76.158.46.120', '09-40-1B-50-5B-7C', 'Linux', 15, 15);
		INSERT INTO Server VALUES ( 13, '27.41.26.1', 'CE-5D-A9-CD-9D-1A', 'Linux', 13, 13);
		INSERT INTO Server VALUES ( 18, '31.147.47.135', 'C9-4A-91-92-61-E4', 'Linux', 18, 18);
		INSERT INTO Server VALUES ( 99, '136.76.209.29', 'DC-25-ED-3B-2C-83', 'Linux', 99, 99);
		INSERT INTO Server VALUES ( 46, '148.123.217.180', 'B1-B0-A4-15-C8-C4', 'Linux', 46, 46);
		INSERT INTO Server VALUES ( 90, '215.195.170.250', 'C9-D1-04-E5-22-60', 'Linux', 90, 90);
		INSERT INTO Server VALUES ( 21, '49.168.230.52', '61-F0-BD-0B-BE-5B', 'Linux', 21, 21);
		INSERT INTO Server VALUES ( 95, '39.144.96.168', '26-87-A5-B8-19-07', 'Linux', 95, 95);
		INSERT INTO Server VALUES ( 12, '171.75.194.33', '9D-F6-2D-8A-31-5A', 'Linux', 12, 12);
		INSERT INTO Server VALUES ( 77, '155.3.131.76', '0D-E2-0A-B2-F7-D2', 'Linux', 77, 77);
		INSERT INTO Server VALUES ( 97, '125.70.48.155', '76-C1-A3-7B-A6-C6', 'Linux', 97, 97);
		INSERT INTO Server VALUES ( 53, '147.236.71.221', 'DB-08-B7-99-14-75', 'Linux', 53, 53);
		INSERT INTO Server VALUES ( 32, '13.50.127.44', 'F4-3A-FD-9A-F2-17', 'Linux', 32, 32);
		INSERT INTO Server VALUES ( 35, '119.187.96.139', 'A1-90-0D-CE-1A-3F', 'Linux', 35, 35);
		INSERT INTO Server VALUES ( 91, '185.68.225.186', '28-28-21-32-DA-19', 'Linux', 91, 91);
		INSERT INTO Server VALUES ( 42, '34.171.64.223', '04-50-DB-A8-CB-81', 'Linux', 42, 42);
		INSERT INTO Server VALUES ( 54, '209.5.172.140', '6F-A6-8A-26-3F-9E', 'Linux', 54, 54);
		INSERT INTO Server VALUES (  5, '250.1.234.85', '9C-34-D9-9A-CE-CC', 'Linux', 5, 5);
		INSERT INTO Server VALUES ( 63, '47.55.46.244', 'B1-6F-5C-BF-3D-76', 'Linux', 63, 63);
		INSERT INTO Server VALUES ( 89, '28.233.252.253', 'FE-66-9F-20-98-79', 'Linux', 89, 89);
		INSERT INTO Server VALUES ( 61, '46.148.253.130', '39-9D-CA-14-46-96', 'Linux', 61, 61);
		INSERT INTO Server VALUES ( 68, '196.219.253.246', '96-B5-3D-21-DC-7C', 'Linux', 68, 68);
		INSERT INTO Server VALUES ( 37, '230.237.8.98', 'BF-79-B1-98-13-7F', 'Linux', 37, 37);
		INSERT INTO Server VALUES ( 65, '128.161.140.240', '65-C5-EF-C1-84-2D', 'Linux', 65, 65);
		INSERT INTO Server VALUES ( 86, '230.49.101.159', '37-83-93-D7-A3-2C', 'Linux', 86, 86);
		INSERT INTO Server VALUES ( 85, '168.160.246.250', '50-DC-C9-1B-F1-10', 'Linux', 85, 85);
		INSERT INTO Server VALUES ( 81, '112.115.61.131', 'B1-88-C6-EE-A9-A2', 'Linux', 81, 81);
		INSERT INTO Server VALUES ( 33, '159.113.178.216', '6B-68-1C-1C-01-30', 'Linux', 33, 33);
		INSERT INTO Server VALUES ( 66, '3.216.163.254', '9C-66-F5-8B-28-7A', 'Linux', 66, 66);
		INSERT INTO Server VALUES ( 84, '49.157.199.219', 'B8-5F-FD-4C-36-A1', 'Linux', 84, 84);
		INSERT INTO Server VALUES ( 74, '222.107.94.105', '42-8A-C1-1C-1E-2A', 'Linux', 74, 74);
		INSERT INTO Server VALUES ( 24, '168.241.182.217', '8F-8D-A8-14-39-35', 'Linux', 24, 24);
		INSERT INTO Server VALUES ( 30, '220.74.175.188', 'C8-BB-4E-F0-0F-89', 'Linux', 30, 30);
		INSERT INTO Server VALUES ( 40, '101.172.39.222', '89-14-28-55-08-2B', 'Linux', 40, 40);
		INSERT INTO Server VALUES ( 36, '177.102.34.82', '89-55-1B-18-FF-EA', 'Linux', 36, 36);
		INSERT INTO Server VALUES ( 14, '220.225.81.58', '27-42-74-E8-5E-92', 'Linux', 14, 14);
		INSERT INTO Server VALUES ( 22, '70.205.215.217', '13-EE-1F-BB-03-58', 'Linux', 22, 22);
		INSERT INTO Server VALUES ( 64, '66.127.24.235', 'F1-CC-14-3F-BC-24', 'Linux', 64, 64);
		INSERT INTO Server VALUES ( 72, '36.35.211.53', 'C9-45-38-F1-9B-41', 'Linux', 72, 72);
		INSERT INTO Server VALUES (  2, '45.52.155.67', '1C-24-96-38-3D-96', 'Linux', 2, 2);
		INSERT INTO Server VALUES ( 41, '241.171.138.173', '22-64-D8-96-4D-37', 'Linux', 41, 41);
		INSERT INTO Server VALUES ( 27, '15.246.73.187', '29-61-26-49-1D-29', 'Linux', 27, 27);
		INSERT INTO Server VALUES (  8, '150.61.249.211', 'A2-0E-F5-B6-4D-B2', 'Linux', 8, 8);
		INSERT INTO Server VALUES ( 83, '12.145.218.109', 'DA-16-F8-13-08-93', 'Linux', 83, 83);
		INSERT INTO Server VALUES ( 45, '150.11.224.135', '54-25-B8-EB-5D-F5', 'Linux', 45, 45);
		INSERT INTO Server VALUES ( 26, '160.207.190.195', '81-80-5A-5A-17-A8', 'Linux', 26, 26);
		INSERT INTO Server VALUES ( 96, '204.126.91.176', '92-40-09-B8-89-26', 'Linux', 96, 96);



		INSERT INTO Component VALUES (15);
		INSERT INTO Component VALUES (13);
		INSERT INTO Component VALUES (18);
		INSERT INTO Component VALUES (99);
		INSERT INTO Component VALUES (46);
		INSERT INTO Component VALUES (90);
		INSERT INTO Component VALUES (21);
		INSERT INTO Component VALUES (95);
		INSERT INTO Component VALUES (12);
		INSERT INTO Component VALUES (77);
		INSERT INTO Component VALUES (97);
		INSERT INTO Component VALUES (53);
		INSERT INTO Component VALUES (32);
		INSERT INTO Component VALUES (35);
		INSERT INTO Component VALUES (91);
		INSERT INTO Component VALUES (42);
		INSERT INTO Component VALUES (54);
		INSERT INTO Component VALUES ( 5);
		INSERT INTO Component VALUES (63);
		INSERT INTO Component VALUES (89);
		INSERT INTO Component VALUES (61);
		INSERT INTO Component VALUES (68);
		INSERT INTO Component VALUES (37);
		INSERT INTO Component VALUES (65);
		INSERT INTO Component VALUES (86);
		INSERT INTO Component VALUES (85);
		INSERT INTO Component VALUES (81);
		INSERT INTO Component VALUES (33);
		INSERT INTO Component VALUES (66);
		INSERT INTO Component VALUES (84);
		"""


	connection.executescript(script)
	connection.commit()
	connection.close()
	print 'Database created'