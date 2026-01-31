from marshmallow import Schema, fields

class HeritageWordPuzzleSchema(Schema):
    id = fields.Int(required=True)
    question = fields.Str(required=True)
    answer = fields.Str(required=True)

class HeritageMazeSchema(Schema):
    id = fields.Int(required=True)
    maze_data = fields.Str(required=True)

class HeritageQuizSchema(Schema):
    id = fields.Int(required=True)
    question = fields.Str(required=True)
    options = fields.List(fields.Str(), required=True)
    correct_answer = fields.Str(required=True)

class HeritageCardsSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)