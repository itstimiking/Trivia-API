import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql:///{}".format( self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {'question':"new question","answer":"new answer","category":'4',"difficulty":2}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        questions = Question.query.filter(Question.question == self.new_question['question'])
        for q in questions:
            q.delete()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    """Get pagninated questions test--------------------------------------- """
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(len(data["categories"]))

    def test_get_paginated_questions_out_of_range(self):
        res = self.client().get("/questions?page=100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    """ Get questions by category test ------------------------------------- """
    def test_get_questions_for_a_given_category_id(self):
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["current_category"]))
    
    def test_get_questions_for_a_given_category_id_out_of_range(self):
        res = self.client().get("/categories/1000/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    """ Delete question test ------------------------------------- """
    def test_delete_question_for_a_given_question_id(self):
        res = self.client().delete("/questions/4")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 9).one_or_none()
        self.assertEqual(question, None)
    
    def test_delete_questions_for_a_given_question_id_out_of_range(self):
        res = self.client().delete("/questions/2000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False) 


    """ Add a new question test ------------------------------------- """
    def test_add_question(self):
        res = self.client().post("/questions",json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
    
    def test_add_question_error(self):
        res = self.client().post("/questions",json={'question':None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)  
        self.assertEqual(data['message'],'unprocessable')  


    """ Search questions test ------------------------------------- """
    def test_search_questions(self):
        res = self.client().post("/questions",json={'searchTerm':'title'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])  
        self.assertTrue(data['current_category'])  
        self.assertTrue(data['total_questions'])
    
    def test_search_questions_empty_serchTerm(self):
        res = self.client().post("/questions",json={'searchTerm':''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)  
        self.assertEqual(data['total_questions'],0)


    """ Play quize endpoint test -----------------------------------"""
    def test_play_quizzes(self):
        res = self.client().post("/quizzes",json={"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])

    def test_play_quizzes_no_valid_category(self):
        res = self.client().post("/quizzes",json={"previous_questions":[],"quiz_category":{"type":"Science","id":"1000"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

    