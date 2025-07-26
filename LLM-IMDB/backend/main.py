from fastapi import FastAPI
from pydantic import BaseModel
import re

from fastapi.middleware.cors import CORSMiddleware
from vector_store import load_vector_store

app = FastAPI()

# ✅ Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load Chroma vector store once
store = load_vector_store()
print(store,"the store")

class QueryRequest(BaseModel):
    message: str

@app.post("/predict")
def predict(req: QueryRequest):
    query = req.message

    # ✅ Extract 4-digit year from query
    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", query)
    search_year = year_match.group(0) if year_match else None

    results = store.similarity_search(query, k=10)

    seen_titles = set()
    movies = []

    for r in results:
        meta = r.metadata
        title = meta.get("Series_Title", "Unknown")
        year = str(meta.get("Released_Year", "N/A"))

        if search_year and year != search_year:
            continue

        if title in seen_titles:
            continue
        seen_titles.add(title)

        movies.append({
            "title": title,
            "year": year,
            "poster": meta.get("Poster_Link", ""),
            "summary": meta.get("Overview", ""),
            "genre": meta.get("Genre", "").split(",") if meta.get("Genre") else [],
            "actors": [meta.get("Star1", ""), meta.get("Star2", "")]
        })

    return {"movies": movies}




# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from chat_chain import qa_chain, chat_history
# import re

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class QueryRequest(BaseModel):
#     message: str

# # ✅ Utility: Generate a natural language summary
# def generate_summary(meta):
#     title = meta.get("Series_Title", "Unknown")
#     year = meta.get("Released_Year", "N/A")
#     genre = meta.get("Genre", "")
#     overview = meta.get("Overview", "")
#     return f"{title} ({year}) is a {genre.lower()} movie. {overview}"

# @app.post("/predict")
# def predict(req: QueryRequest):
#     query = req.message

#     # ✅ Extract year if present in query
#     year_match = re.search(r"\b(19\d{2}|20\d{2})\b", query)
#     search_year = year_match.group(0) if year_match else None

#     # ✅ Genre & Actor keyword extraction (simple version)
#     genre_keywords = ["action", "drama", "comedy", "sci-fi", "thriller", "romance"]
#     found_genre = next((g for g in genre_keywords if g in query.lower()), None)

#     actor_match = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", query)
#     found_actor = actor_match[0] if actor_match else None

#     # ✅ Run conversational chain
#     response = qa_chain({"question": query, "chat_history": chat_history})
#     chat_history.append((query, response["answer"]))

#     # ✅ Collect movie metadata from source docs
#     seen_titles = set()
#     movies = []

#     for doc in response["source_documents"]:
#         meta = doc.metadata
#         title = meta.get("Series_Title", "Unknown")
#         year = str(meta.get("Released_Year", "N/A"))
#         genre = meta.get("Genre", "").lower()
#         actors = [meta.get("Star1", ""), meta.get("Star2", ""), meta.get("Star3", ""), meta.get("Star4", "")]

#         # ✅ Apply year filter
#         if search_year and year != search_year:
#             continue

#         # ✅ Apply genre filter
#         if found_genre and found_genre not in genre:
#             continue

#         # ✅ Apply actor filter
#         if found_actor and all(found_actor not in a for a in actors):
#             continue

#         if title in seen_titles:
#             continue
#         seen_titles.add(title)

#         movies.append({
#             "title": title,
#             "year": year,
#             "poster": meta.get("Poster_Link", ""),
#             "summary": generate_summary(meta),
#             "genre": meta.get("Genre", "").split(",") if meta.get("Genre") else [],
#             "actors": actors
#         })

#     return {"movies": movies, "answer": response["answer"]}
