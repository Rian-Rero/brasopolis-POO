import sqlite3

databasePath = 'db/brasopolis.db'

def connect():
    conn = sqlite3.connect(databasePath)
    return conn

def initializeDatabase():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Player (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance REAL DEFAULT 0,  
            position INTEGER DEFAULT 0,  
            properties TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Property (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,            
            rent REAL NOT NULL,             
            ownerId INTEGER,               
            FOREIGN KEY (ownerId) REFERENCES Player(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Board (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spaces TEXT,                    
            cards TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Card (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,     
            action TEXT                    
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll INTEGER                    
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Game (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currentPlayer INTEGER,         
            turns INTEGER DEFAULT 0,        
            isGameOver BOOLEAN DEFAULT 0,   
            winnerId INTEGER,              
            boardId INTEGER,               
            FOREIGN KEY (currentPlayer) REFERENCES Player(id),
            FOREIGN KEY (winnerId) REFERENCES Player(id),
            FOREIGN KEY (boardId) REFERENCES Board(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized and tables created successfully.")

def addPlayer(name, initialBalance=1500):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Player (name, balance) VALUES (?, ?)", (name, initialBalance))
    conn.commit()
    conn.close()

def addProperty(name, price, rent):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Property (name, price, rent) VALUES (?, ?, ?)", (name, price, rent))
    conn.commit()
    conn.close()

def registerMove(playerId, move, turn):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO historicoMovimentos (jogadorId, movimento, turno) VALUES (?, ?, ?)", 
                   (playerId, move, turn))
    conn.commit()
    conn.close()

def rollDice():
    import random
    result = random.randint(1, 6)
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Dice (roll) VALUES (?)", (result,))
    conn.commit()
    conn.close()
    return result

def startGame():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Game (currentPlayer, turns, isGameOver) VALUES (?, ?, ?)", (None, 0, False))
    conn.commit()
    conn.close()

