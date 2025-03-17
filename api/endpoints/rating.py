from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from database import database

router = APIRouter()

@router.get("/search_professor_rating/{rating}")
def search_professor_rating(rating: float): 
    """Find all prof's with a specfic rating"""
    
    conn = database.get_connection()  # Get connection from the pool
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection not available.")

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT prof_id, prof_name, department, rating, number_of_ratings, 
            top_tags, difficulty, would_take_again 
            FROM prof_info WHERE rating = %s
            """, (rating,))  # Safe, efficient, and readable! no sql injection 

        results = cursor.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail=f"'{rating}' not found.")

        # Convert results to a list of dictionaries
        professors = [
            {
                "prof_id": row[0],
                "prof_name": row[1],
                "department": row[2],
                "rating": row[3],
                "number_of_ratings": row[4],
                "top_tags": row[5],
                "difficulty": row[6],
                "would_take_again": row[7]
            }
            for row in results
        ]

        return professors  # Return as a list


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            database.release_connection(conn)  # Release connection back to the pool


