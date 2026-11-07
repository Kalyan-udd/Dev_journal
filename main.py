from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime
from fastapi.requests import Request
from schemas import Journal, Comments, TextGenerationModel, ContentUpdate
from databases import insert_values, show_complete_data, update_comment, prompt_query, update_content, delete_journal_post, delete_comment
from intent_check import IntentCheck
from prompt_generation import PromptGeneration

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
        "status":"200, ok", 
    }

@app.post("/api/entries")
def receiving_data(data: Journal):
    try:
        current_time = datetime.now().isoformat()
        result = insert_values(database_path="Database.db", data=dict(data), time=current_time)
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

@app.post("/api/prompt")
def prompt(data: TextGenerationModel):
    journal_name = data.journal_name
    user_prompt = data.user_prompt
    try:
        row = prompt_query(database_path="Database.db", journal_name=journal_name)
        intent_check = IntentCheck()
        intent = intent_check.compare(user_prompt)
        prompt_gen = PromptGeneration()
        message_payload = prompt_gen.build_messages(intent=intent, user_query=user_prompt, retrieved_logs=row, journal_title=journal_name)
        generated_text = prompt_gen.text_generation(message_payload=message_payload)
        return {
            "intent": intent,
            "journal_targeted": journal_name,
            "generated_response": generated_text,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception - {e}") 

@app.post("/api/{entryId}/update/title")
def update_title(entryId, data:ContentUpdate):
    content = data.content
    try:
        database_response = update_content(content_type='title', content=content, entry_Id=entryId)
        return f"successfully updated the response - {database_response}"
    except Exception as e:
        raise HTTPException(status_code= 500, detail=f"Exception - {e}")

@app.post("/api/{entryId}/update/content")
def update__content(entryId, data:ContentUpdate):
    content = data.content
    try:
        database_response = update_content(content_type="content", content=content, entry_Id=entryId)
        return f"successfully updated the response - {database_response}"
    except Exception as e:
        raise HTTPException(status_code= 500, detail=f"Exception - {e}")

@app.post("/api/{entryId}/update/tags")
def update_tags(entryId, data:ContentUpdate):
    content = data.content
    try:
        database_response = update_content(content_type="tags", content=content, entry_Id=entryId)
        return f"successfully updated the response - {database_response}"
    except Exception as e:
        raise HTTPException(status_code= 500, detail=f"Exception - {e}")

@app.delete("/api/entries/{entryId}")
def delete_post(entryId):
    response = delete_journal_post(entryId=entryId)
    return response

@app.delete("/entries/{entryId}/comments/{commentIndex}")
def delete_comments(entryId:int, commentIndex:int):
    response = delete_comment(entryId=entryId, comment_index= commentIndex)
    if response:
        return "Comment Deleted Successful"
    else:
        raise HTTPException(status_code=422, detail="Incorrect entryId or comment_index")



if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)