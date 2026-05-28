.
├── app/
│   ├── api/                # API routes and versioning
│   │   └── v1/             # V1 endpoints (e.g., users.py, items.py)
│   ├── core/               # Global configs (auth, security, settings)
│   ├── db/                 # Database connection and session management
│   ├── models/             # Database ORM models (SQLAlchemy/SQLModel)
│   ├── schemas/            # Pydantic models for data validation
│   ├── services/           # Business logic (kept out of routes)
│   └── main.py             # App entry point & initialization
├── tests/                  # Pytest test cases
├── .env                    # Environment variables
├── alembic/                # Database migrations
├── docker-compose.yml      # Container orchestration
└── requirements.txt        # Project dependencies
