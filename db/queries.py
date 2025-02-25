from typing import List, Dict, Any, Optional
from databases import Database

from db.models import Chain, ChainElement, AvailableChainInfo, ChainHistoryEntry, ChainInfoSummary

async def get_chain_by_id(database: Database, chain_id: int) -> Optional[Chain]:
    query = """
    SELECT * FROM chains WHERE id = :chain_id
    """
    row = await database.fetch_one(query, {"chain_id": chain_id})
    return Chain(**row) if row else None

async def get_chain_element_by_id(database: Database, element_id: int) -> Optional[ChainElement]:
    query = """
    SELECT * FROM chain_elements WHERE id = :element_id
    """
    row = await database.fetch_one(query, {"element_id": element_id})
    return ChainElement(**row) if row else None

async def get_active_chains(database: Database) -> List[Dict[str, Any]]:
    """
    Récupère toutes les chaînes actives avec leur dernier élément, le nombre de joueurs
    et le nombre de tours.
    
    Args:
        database: L'instance de la base de données
        
    Returns:
        Une liste de dictionnaires contenant les informations de chaque chaîne active
    """
    query = """
    SELECT 
        c.id,
        ce_last.type as last_type,
        ce_last.content as last_content,
        COUNT(DISTINCT ce.player_name) as players_count,
        COUNT(ce.id) as turns_count
    FROM chains c
    JOIN chain_elements ce ON ce.chain_id = c.id
    JOIN chain_elements ce_last ON ce_last.chain_id = c.id
    -- WHERE c.is_active = TRUE
    AND ce_last.order_number = (
        SELECT MAX(order_number)
        FROM chain_elements
        WHERE chain_id = c.id
    )
    AND ce_last.type = 'drawing'
    GROUP BY c.id
    ORDER BY c.id DESC
    """
    rows = await database.fetch_all(query)
    return [ChainInfoSummary(**row) for row in rows]

async def get_available_chain(database: Database) -> Optional[Dict[str, Any]]:
    """
    Récupère une chaîne inactive au hasard et la marque comme active.
    """
    async with database.transaction():
        # On récupère une chaîne inactive au hasard
        query = """
        SELECT 
            c.id,
            ce.type as last_type,
            ce.content as last_content,
            ce.order_number as last_order
        FROM chains c
        JOIN chain_elements ce ON ce.chain_id = c.id
        WHERE c.is_active = FALSE
        AND ce.order_number = (
            SELECT MAX(order_number)
            FROM chain_elements
            WHERE chain_id = c.id
        )
        ORDER BY RANDOM()
        LIMIT 1
        """
        chain = await database.fetch_one(query)
        
        if chain:
            # On marque la chaîne comme active
            await database.execute(
                "UPDATE chains SET is_active = TRUE WHERE id = :id",
                {"id": chain["id"]}
            )
            
        return AvailableChainInfo(**chain)

async def create_new_chain(database: Database, player_name: str, initial_text: str) -> int:
    """
    Crée une nouvelle chaîne avec un texte initial.
    """
    async with database.transaction():
        # Création de la chaîne
        chain_id = await database.execute(
            "INSERT INTO chains (is_active) VALUES (FALSE)"
        )
        
        # Ajout du premier élément
        chain_element = await database.execute("""
            INSERT INTO chain_elements (chain_id, order_number, content, type, player_name)
            VALUES (:chain_id, 1, :content, 'text', :player_name)
            RETURNING *
        """, {
            "chain_id": chain_id,
            "content": initial_text,
            "player_name": player_name
        })

        return ChainElement(**chain_element)

async def add_chain_element(
    database: Database,
    chain_id: int,
    player_name: str,
    content: str,
    element_type: str
) -> None:
    """
    Ajoute un nouvel élément à une chaîne existante.
    """
    async with database.transaction():
        # On récupère le dernier numéro d'ordre
        last_order = await database.fetch_val("""
            SELECT MAX(order_number)
            FROM chain_elements
            WHERE chain_id = :chain_id
        """, {"chain_id": chain_id})
        
        # On ajoute le nouvel élément
        chain_element = await database.execute("""
            INSERT INTO chain_elements (chain_id, order_number, content, type, player_name)
            VALUES (:chain_id, :order_number, :content, :type, :player_name)
            RETURNING *
        """, {
            "chain_id": chain_id,
            "order_number": last_order + 1,
            "content": content,
            "type": element_type,
            "player_name": player_name
        }) 
    
        return ChainElement(**chain_element)

async def set_chain_active(database: Database, chain_id: int, is_active: bool) -> None:
        # On marque la chaîne comme inactive
        await database.execute(
            "UPDATE chains SET is_active = :is_active WHERE id = :id",
            {"id": chain_id, "is_active": is_active}
        )

async def get_chain_history(database: Database, chain_id: int) -> List[Dict[str, Any]]:
    """
    Récupère tous les éléments d'une chaîne dans l'ordre.
    """
    query = """
    SELECT 
        ce.order_number,
        ce.type,
        ce.content,
        ce.player_name,
        ce.created_at as created_at
    FROM chain_elements ce
    WHERE ce.chain_id = :chain_id
    ORDER BY ce.order_number ASC
    """
    rows = await database.fetch_all(query, {"chain_id": chain_id})
    return [ChainHistoryEntry(**row) for row in rows]