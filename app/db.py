from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL='postgresql://neondb_owner:npg_zsGZ0d7yeIaU@ep-bold-tree-aiptplva.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle= 300,
    connect_args={"sslmode":"require"}
)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)