from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title = "E-commerce")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get('/health')
def health_check():
    return{'status':'ok'}
