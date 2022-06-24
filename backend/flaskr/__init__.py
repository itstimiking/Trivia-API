import os
from unicodedata import category
from flask import Flask, request, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories',methods=['GET'])
    def home_route():
        categories = {}
        all_categories = [category.format() for category in Category.query.all()]
        for category in all_categories:
            categories[category["id"]] = category["type"]

        return jsonify({'categories':categories,"success":True})

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_paginated_questions():
        categories = {}
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        all_categories = [category.format() for category in Category.query.all()]
        for category in all_categories:
            categories[category["id"]] = category["type"]

        if len(current_questions) == 0: 
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "current_category":"All",
                "categories":categories,
            }
        )
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>",methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        else:
            question.delete()
            return jsonify({'success':True})

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions", methods=["POST"])
    def add_question():
        body = request.get_json()

        searchTerm = body.get('searchTerm',None) 

        if searchTerm is not None:
            if searchTerm == '':
                return jsonify({
                    'questions':[],
                    'total_questions':0,
                    'current_category':"Search:",
                    'success':False 
                })
            serch = Question.query.filter(Question.question.ilike("%{}%".format(searchTerm))).all()
            questions = [question.format() for question in serch]

            return jsonify({
                'questions':questions,
                'total_questions':len(questions),
                'current_category':"Includes: " + searchTerm
            })

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        question_category = body.get("category", None)
        question_difficulty = body.get("difficulty", None)

        if new_question is None or new_answer is None or question_category is None or question_difficulty is None:
            abort(422)

        try:
            question = Question(
                question=new_question, 
                answer=new_answer, 
                category=question_category,
                difficulty=question_difficulty
            )
            question.insert()

            return jsonify({"success": True})

        except:
            abort(422)

    

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_for_categoryId(category_id): 
        selection = Question.query.filter(Question.category == category_id).all()
        questions = [question.format() for question in selection]
        if len(selection) < 1:
            abort(404)
        return jsonify({
            'questions':questions,
            'total_questions': len(questions),
            'current_category':Category.query.get(category_id).format()['type'],
            'success':True
        })



    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        body = request.get_json()
        prev_questions = body["previous_questions"]
        category = body["quiz_category"]
        current_question = {}

        questions_in_category = []

        if category['id'] == 0:
            questions_in_category = Question.query.all()
        else:
            questions_in_category = Question.query.filter(Question.category == category["id"]).all()

        questions = [question.format() for question in questions_in_category]
        
        if len(questions) > 0:
            if len(prev_questions) < len(questions):
                if len(prev_questions) == 0:
                    current_question = questions[len(prev_questions)]
                else:
                    current_question = questions[len(prev_questions)]

                return jsonify({
                    'question':current_question
                })
            else: 
                return jsonify({
                    'question':''
                })
        else:
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    return app

