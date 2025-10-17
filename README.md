# 🌌 Star Wars API — Django + GraphQL

This project implements a **GraphQL API** using **Django** and **Graphene-Django**, with data from the Star Wars universe.  
It allows querying characters, movies, and relationships between them, as well as executing **mutations** to create or delete records.

---

## 🚀 1. Environment Setup

First, clone the repository and install the necessary dependencies.

```bash
git clone https://github.com/yourusername/django-starwars.git
cd django-starwars
```

Create your virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## 🧩 2. Database Creation

Run the initial migrations to build the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 📦 3. Load Initial Data

Run the command that consumes the public Star Wars API and loads the data:

```bash
python manage.py load_starwars_data
```

## 🔥 4. Start the API

Start the development server:

```bash
python manage.py runserver
```

Once started, you can access:

- **GraphQL Playground (GraphiQL)**: http://127.0.0.1:8000/graphql/

## 🧠 5. Basic Usage from GraphQL

Once inside GraphiQL, you can execute queries like:

### 🔍 Get Characters

```graphql
{
  allCharacters {
    edges {
      node {
        id
        name
        gender
        specie
      }
    }
  }
}
```

### 🎬 Create a Movie

```graphql
mutation {
  createMovie(
    input: {
      title: "A New Hope"
      releaseDate: "1977-05-25"
      openingCrawl: "It is a period of civil war..."
      directorId: "UGVyc29uTm9kZTox" # Example global ID
    }
  ) {
    movie {
      title
      director {
        name
      }
    }
  }
}
```

### 🗑️ Delete a Movie

```graphql
mutation {
  deleteMovie(input: { id: "TW92aWVOb2RlOjE=" }) {
    ok
    message
  }
}
```

## 🧪 6. Run Tests

Execute unit and integration tests with:

```bash
python manage.py test
```

This will automatically execute all files located inside the folder:

```
movies/tests/
├── test_unit_models.py
├── test_unit_utils.py
├── test_integration_queries.py
└── test_integration_mutations.py
```

The tests validate both internal model functions and GraphQL operations (queries and mutations).

## 📚 7. Main Project Structure

```
django-starwars/
│
├── core/
│   ├── schema.py
│   ├── settings.py
│   └── urls.py
│
├── movies/
│   ├── models.py
│   ├── admin.py
│   ├── views.py
│   ├── management/
│   │   └── commands/
│   │       └── load_starwars_data.py
│   ├── fixtures/
│   │   └── starwars_data.json
│   ├── tests/
│   │   ├── test_unit_models.py
│   │   ├── test_unit_utils.py
│   │   ├── test_integration_queries.py
│   │   └── test_integration_mutations.py
│   └── migrations/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
└── .env
```

## 🛠️ 8. Technologies Used

- **Python 3.12+**
- **Django 5+**
- **Graphene-Django**
- **PostgreSQL** / **SQLite**
- **django-test**
- **python-dotenv**
- **requests**

## ✨ 9. Credits

Project developed using Django and GraphQL  
**Developer**: Juan David Torres
**Contact**: judatoba02@gmail.com

--
