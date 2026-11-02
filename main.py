from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime
from fastapi.requests import Request
from schemas import Journal, Comments
from databases import insert_values, show_complete_data, update_comment


app = FastAPI()

@app.get("/", response_class=FileResponse)
def home():
    return FileResponse("templates/index.html")

@app.get("/entries")
def entries(request:Request):
    try:
        data = show_complete_data("Database.db")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"exception: {e}")

@app.get("/api/health")
def health_check():
    return {
        "status":"ok",
    }

@app.post("/api/entries")
def receiving_data(data: Journal):
    try:
        current_time = datetime.now().isoformat()
        result = insert_values("Database.db", data=dict(data), time=current_time)
        return {"status":"Success", "result":result, "Created_at": current_time}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@app.post("/entries/{entryId}/comments")
def comments(data:Comments, entryId:int):
    try:
        success = update_comment(database_path="Database.db", entryId=entryId, new_comment=data.content)
        if success:
            return {"status": "success", "result": "saved the comment successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"exception occured - {e}.")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)