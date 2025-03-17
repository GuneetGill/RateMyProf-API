from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from database import database

router = APIRouter()


@router.get("/search_professor_name/{name}")
def search_professor_name(name: str):
    """Searches for a professor by name in the database and returns their details."""
    
    #ensure all lowercase 
    name = name.lower().replace('+', ' ')  # Replacing '+' with space
    
    conn = database.get_connection()  # Get connection from the pool
    if not conn:
        print("1")
        raise HTTPException(status_code=500, detail="Database connection not available.")

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT prof_id, prof_name, department, rating, number_of_ratings, 
            top_tags, difficulty, would_take_again 
            FROM prof_info WHERE prof_name = %s
            """, (name,))  # Safe, efficient, and readable! no sql injection 

        result = cursor.fetchone()

        if not result:
            print("2")
            raise HTTPException(status_code=404, detail=f"Professor '{name}' not found.")

         # Construct JSON response
        professor_data = {
            "prof_id": result[0],
            "prof_name": result[1],
            "department": result[2],
            "rating": result[3],
            "number_of_ratings": result[4],
            "top_tags": result[5],
            "difficulty": result[6],
            "would_take_again": result[7]
        }
        
        return professor_data

    except Exception as e:
        print("3")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            database.release_connection(conn)  # Release connection back to the pool



@router.get("/search_professor_id/{id}")
def search_professor_id(id: int): 
    """Searches for a professor by id in the database and returns their details."""
    
    conn = database.get_connection()  # Get connection from the pool
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection not available.")

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT prof_id, prof_name, department, rating, number_of_ratings, 
            top_tags, difficulty, would_take_again 
            FROM prof_info WHERE prof_id = %s
            """, (id,))  # Safe, efficient, and readable! no sql injection 

        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail=f"Professor with ID {id} not found.")

         # Construct JSON response
        professor_data = {
            "prof_id": result[0],
            "prof_name": result[1],
            "department": result[2],
            "rating": result[3],
            "number_of_ratings": result[4],
            "top_tags": result[5],
            "difficulty": result[6],
            "would_take_again": result[7]
        }
        
        return professor_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            database.release_connection(conn)  # Release connection back to the pool
