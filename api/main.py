import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, HTTPException, Query
from contextlib import asynccontextmanager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database 

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown events using a context manager."""
    database.initialize_connection_pool()
    yield  # Application runs while execution is suspended here
    database.close_connection_pool()

app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Welcome to the Rate my Professor API"}

@app.get("/search_professor_name/{name}")
def search_professor_name(name: str):
    """Searches for a professor by name in the database and returns their details."""
    
    #ensure all lowercase 
    name = name.lower()
    
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



@app.get("/search_professor_id/{id}")
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


@app.get("/search_department/{department}")
def search_professor_department(department: str): 
    """Find all prof's within a department"""
    
    department = department.lower() #ensure all lowercase
    
    conn = database.get_connection()  # Get connection from the pool
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection not available.")

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT prof_id, prof_name, department, rating, number_of_ratings, 
            top_tags, difficulty, would_take_again 
            FROM prof_info WHERE department = %s
            """, (department,))  # Safe, efficient, and readable! no sql injection 

        results = cursor.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail=f"'{department}' not found.")

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


@app.get("/search_rating/{rating}")
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


