# Backend - Trivia API
- [Install Dependencies](#dependencies)
- [Setup the server](#setup)
- [Run the server](#run)
- [Api Reference](#api)

## Setting up the Backend

The code adheres to the PEP 8 style guide and follows common best practices.

### Install Dependencies {#dependencies}

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database 

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server {#run}

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


### API Reference {#api}

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'total_questions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'current_category': 'History'
}
```


`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string

```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'total_questions': 100,
    'current_category': 'History'
}
```


`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not return anything .



`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
}
```
- Returns: a single new question object

```
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}
```


`POST '/questions'`

- For adding question to the questions database or to search for questions using a search term in the question

- Request Body to add a new question 

```
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
```
- No response body

#### Search

- Request body order to search for a specific question by search term

```
{
    'searchTerm': 'this is the term the user is looking for'
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'total_questions': 100,
    'current_category': 'Entertainment'
}
```