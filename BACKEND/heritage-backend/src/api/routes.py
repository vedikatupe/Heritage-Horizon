from flask import Blueprint, jsonify, request
from models.db import db
from models.models import HeritageWordPuzzle, HeritageMaze, HeritageQuiz, HeritageCards

api = Blueprint('api', __name__)

@api.route('/heritage/wordpuzzle', methods=['GET'])
def get_wordpuzzle():
    puzzles = HeritageWordPuzzle.query.all()
    return jsonify([puzzle.to_dict() for puzzle in puzzles])

@api.route('/heritage/maze', methods=['GET'])
def get_maze():
    mazes = HeritageMaze.query.all()
    return jsonify([maze.to_dict() for maze in mazes])

@api.route('/heritage/quiz', methods=['GET'])
def get_quiz():
    quizzes = HeritageQuiz.query.all()
    return jsonify([quiz.to_dict() for quiz in quizzes])

@api.route('/heritage/cards', methods=['GET'])
def get_cards():
    cards = HeritageCards.query.all()
    return jsonify([card.to_dict() for card in cards])

@api.route('/heritage/wordpuzzle', methods=['POST'])
def create_wordpuzzle():
    data = request.json
    new_puzzle = HeritageWordPuzzle(**data)
    db.session.add(new_puzzle)
    db.session.commit()
    return jsonify(new_puzzle.to_dict()), 201

@api.route('/heritage/maze', methods=['POST'])
def create_maze():
    data = request.json
    new_maze = HeritageMaze(**data)
    db.session.add(new_maze)
    db.session.commit()
    return jsonify(new_maze.to_dict()), 201

@api.route('/heritage/quiz', methods=['POST'])
def create_quiz():
    data = request.json
    new_quiz = HeritageQuiz(**data)
    db.session.add(new_quiz)
    db.session.commit()
    return jsonify(new_quiz.to_dict()), 201

@api.route('/heritage/cards', methods=['POST'])
def create_cards():
    data = request.json
    new_card = HeritageCards(**data)
    db.session.add(new_card)
    db.session.commit()
    return jsonify(new_card.to_dict()), 201