Reliable Posts API

Project Overview

This project is a RESTful Posts API built with Python, Django, and Django REST Framework.

It allows authenticated users to create posts, retrieve posts, update their own posts, and delete their own posts.

The API uses Django's built-in authentication system and a relational SQLite database to manage users and posts.

Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- Django ORM

Features

- Create posts with a title and content.
- Automatically associate posts with the authenticated user.
- Automatically record the creation timestamp.
- Retrieve all posts.
- Retrieve a single post.
- Allow users to update only their own posts.
- Allow users to delete only their own posts.
- Validate incoming data using serializers.
- Use appropriate HTTP response status codes.
- Implement an idempotency key for repeated post creation requests.

Project Structure

talkDev project/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── posts/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── manage.py
├── requirements.txt
└── README.md

Installation and Setup

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd talkDev-project

2. Create a virtual environment

python -m venv venv

3. Activate the virtual environment

Windows:

venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Apply database migrations

python manage.py migrate

6. Create a superuser

python manage.py createsuperuser

7. Start the development server

python manage.py runserver

The API will be available at:

"http://127.0.0.1:8000/api/posts/"

API Documentation

All endpoints are prefixed with "/api/".

Method| Endpoint| Description
GET| "/api/posts/"| Retrieve all posts
POST| "/api/posts/"| Create a post
GET| "/api/posts/<id>/"| Retrieve a single post
PATCH| "/api/posts/<id>/"| Update your own post
PUT| "/api/posts/<id>/"| Replace your own post
DELETE| "/api/posts/<id>/"| Delete your own post

Creating a Post

Method: POST

Endpoint: "/api/posts/"

Authentication is required.

Request header:

Idempotency-Key: unique-request-key

Example request body:

{
    "title": "My First Post",
    "content": "This is my first API post."
}

The authenticated user is automatically assigned as the author.

A successful request returns "201 Created".

Retrieving Posts

- "GET /api/posts/" retrieves the list of posts.
- "GET /api/posts/<id>/" retrieves an individual post.

Updating a Post

Method: PATCH

Endpoint: "/api/posts/<id>/"

Only the author of a post can update it.

Deleting a Post

Method: DELETE

Endpoint: "/api/posts/<id>/"

Only the author of a post can delete it.

HTTP Status Codes

Status Code| Meaning
200| Request successful
201| Resource created
204| Resource successfully deleted
400| Invalid request data or missing idempotency key
403| Permission denied or authentication required
404| Requested post not found
409| Idempotency key reused with different request data

Idempotency and Request Handling

The API implements idempotency for post creation using an "Idempotency-Key" request header.

When a client sends a post creation request, the API:

1. Checks whether an idempotency key was provided.
2. Generates a SHA-256 hash of the request data.
3. Checks whether the key has already been used.
4. If the same key and request data are received again, the previously stored response is returned instead of creating another post.
5. If the same key is reused with different request data, the API returns "409 Conflict".
6. If the key is new, the post is created and the response is stored.

Database transactions are used to group the creation and idempotency record operations.

This implementation addresses sequential retries of post creation. Simultaneous requests using the same key have not yet been verified for concurrency safety.

Permissions and Security

- Authentication is required to create posts.
- Post authors are assigned automatically from the authenticated user.
- Authors can update and delete their own posts.
- Other users cannot modify or delete posts they do not own.
- Author and creation timestamp fields are read-only through the serializer.

Running Automated Tests

Run the test suite with:

python manage.py test posts

The project includes automated tests for post creation, listing, retrieval, author updates, unauthorized updates, author deletion, unauthorized deletion, and missing posts.

Test result: 8 tests passed.

Design Decisions

The project uses Django REST Framework's generic views to handle standard API operations.

Serializers handle data validation and control which fields users can modify. A custom permission class enforces author-based access control.

An idempotency record model stores request hashes and previous responses to support safe retries of post creation.

Database transactions help keep post creation and its associated idempotency record together.