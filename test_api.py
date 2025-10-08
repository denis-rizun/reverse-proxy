from fastapi import FastAPI

app = FastAPI(root_path="/api")


@app.get("/test")
async def get_id_without_body(id: int) -> dict:
    return {"id": id, "status": "ok"}


@app.post("/test")
async def get_id_with_body(body: dict) -> dict:
    return body
