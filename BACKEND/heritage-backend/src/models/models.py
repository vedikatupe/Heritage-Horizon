from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class HeritageWordPuzzle(Base):
    __tablename__ = 'heritage_word_puzzle'
    
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)

class HeritageMaze(Base):
    __tablename__ = 'heritage_maze'
    
    id = Column(Integer, primary_key=True)
    maze_data = Column(String, nullable=False)

class HeritageQuiz(Base):
    __tablename__ = 'heritage_quiz'
    
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    options = Column(String, nullable=False)  # Store options as a comma-separated string
    correct_answer = Column(String, nullable=False)

class HeritageCard(Base):
    __tablename__ = 'heritage_cards'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)