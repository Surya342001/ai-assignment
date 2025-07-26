# 🎥 IMDb Movie Finder (LLM + LangChain + FastAPI)

## 🚀 Features:
- Query movies using **natural language**.
- Supports **year, genre, and actor filters**.
- Uses **LangChain + ChromaDB** for semantic search.
- Conversational memory to handle follow-up questions.

## 🛠️ Setup:
```bash
pip install -r requirements.txt
uvicorn main:app --reload
npm start # for frontend





# {"message": "Show me a drama starring Morgan Freeman"}
# {"message": "Movies with Leonardo DiCaprio"}
# {"message": "Show me all Sci-Fi movies"}
# {"message": "List romantic comedy films"}
# {"message": "Movies released in 1994"}
# {"message": "Popular movies from 2000 to 2010"}
# {"message": "Movies with IMDb rating above 8.5"}
# {"message": "Best rated action movies"}
# {"message": "Movies directed by Steven Spielberg"}
# {"message": "Movie about dream sharing"}
# {"message": "Films with prison escape story"}
# {"message": "Comedy movies starring Jim Carrey from the 1990s"}
# {"message": "Action Sci-Fi movies starring Keanu Reeves with IMDb rating above 8"}