from fastapi import FastAPI
from neo4j import GraphDatabase
import os

from app.api.endpoints import router

app = FastAPI()
app.include_router(router)

# === Neo4j Driver Setup ===
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "password")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

# Udostępniamy driver jako zależność
@app.on_event("shutdown")
def shutdown():
    driver.close()

# getter dla serwisów
def get_driver():
    return driver
