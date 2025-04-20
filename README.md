# Intelligent Book Management System

## Overview

The Intelligent Book Management System is a comprehensive solution designed to help users manage books, generate AI-powered summaries, and receive personalized book recommendations. This system leverages Python, FastAPI, PostgreSQL, and a locally running LLaMA3 generative AI model to deliver an intelligent and responsive user experience.

## Architecture

The system follows a modern, modular architecture with clearly separated concerns:

![Architecture Diagram](https://via.placeholder.com/800x500)

### Key Components

1. **API Layer**: FastAPI-based RESTful endpoints with authentication
2. **Domain Layer**: Services handling business logic
3. **Data Access Layer**: Database models and repository pattern implementation
4. **AI Service Layer**: Integration with LLaMA3 for summaries and recommendations
5. **PostgreSQL Database**: Stores book and user data
6. **Utility Layer**: Configuration, logging, and error handling

## Features

- **Book Management**: Add, retrieve, update, and delete book information
- **Review System**: Allow users to add reviews and ratings for books
- **AI-Powered Summaries**: Generate book summaries using LLaMA3
- **Personalized Recommendations**: Get book recommendations based on user preferences
- **Authentication**: Secure API access with JWT-based authentication
- **Asynchronous Operations**: Optimized performance using asyncio and asyncpg

## Technology Stack

- **Backend**: Python 3.10+ with FastAPI
- **Database**: PostgreSQL with asyncpg and SQLAlchemy
- **AI Model**: Locally running LLaMA3
- **Authentication**: JWT-based auth with OAuth 2.0
- **Deployment**: Docker containers with docker-compose
- **Testing**: Pytest for unit and integration tests

## Installation and Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- PostgreSQL
- LLaMA3 model

### Environment Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:shivamtaneja31/GenerativeAI_Based_Book_Management.git
   ```

2. Create a `.env` file with the following variables:
   ```
   POSTGRES_USER=bookuser
   POSTGRES_PASSWORD=bookpassword
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=bookdb
   SECRET_KEY=yoursecretkey
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   LLAMA_MODEL_PATH=/path/to/llama/model
   LLAMA_MODEL_HOST=localhost
   LLAMA_MODEL_PORT=8080
   ```

### Running with Docker

1. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

2. The API will be available at `http://localhost:8000`

### Manual Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

API documentation is available at `http://localhost:8000/docs` when the server is running.

### Key Endpoints

- **Authentication**: 
  - `POST /api/v1/auth/token` - Get authentication token

- **Books**: 
  - `GET /api/v1/books` - List all books
  - `POST /api/v1/books` - Create a new book
  - `GET /api/v1/books/{id}` - Get book details
  - `PUT /api/v1/books/{id}` - Update book
  - `DELETE /api/v1/books/{id}` - Delete book

- **Reviews**:
  - `POST /api/v1/books/{id}/reviews` - Add a review
  - `GET /api/v1/books/{id}/reviews` - Get book reviews

- **AI Features**:
  - `GET /api/v1/books/{id}/summary` - Get AI-generated summary
  - `GET /api/v1/recommendations` - Get personalized recommendations
  - `POST /api/v1/generate-summary` - Generate summary for content

## Project Structure

```
book_management_system/
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration management
│   ├── api/                     # API Layer
│   │   ├── auth.py              # Authentication middleware
│   │   ├── routes/              # API endpoints
│   ├── domain/                  # Domain Layer
│   │   ├── services/            # Business logic services
│   │   ├── models/              # Domain models
│   ├── data/                    # Data Access Layer
│   │   ├── database.py          # Database connection
│   │   ├── models/              # SQLAlchemy models
│   │   ├── repositories/        # Repository pattern
│   ├── ai/                      # AI Service Layer
│   │   ├── ai_manager.py        # AI operations manager
│   │   ├── llama_interface.py   # LLaMA3 interface
│   ├── utils/                   # Utility modules
├── tests/                       # Testing
├── alembic/                     # Database migrations
├── requirements.txt             # Dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose
└── README.md                    # Documentation
```

## Testing

Run tests with pytest:

```bash
pytest
```

## Deployment

The system is designed to be deployed on AWS infrastructure:

1. **Application**: AWS EC2 or ECS with containerized deployment
2. **Database**: AWS RDS PostgreSQL
3. **AI Model**: EC2 instance or container with LLaMA3

## Security Considerations

- JWT-based authentication
- Password hashing with bcrypt
- HTTPS for production deployment
- Environment variable management for secrets

## Future Enhancements

- Implement caching with AWS ElastiCache
- Deploy AI model on AWS SageMaker
- Add user profiles and preferences management
- Implement recommendation caching and batch processing
- Add support for book cover images and content storage

## Contributors

- [Your Name/Team]

## License

[Specify License]
