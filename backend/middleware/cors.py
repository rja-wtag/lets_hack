from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Frontend URLs
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
