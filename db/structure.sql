-- Création de la table des chaînes
CREATE TABLE IF NOT EXISTS chains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Création de la table des éléments de chaîne
CREATE TABLE IF NOT EXISTS chain_elements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chain_id INTEGER NOT NULL,
    order_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    type TEXT CHECK(type IN ('drawing', 'text')) NOT NULL,
    player_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chain_id) REFERENCES chains(id),
    UNIQUE(chain_id, order_number)
);
