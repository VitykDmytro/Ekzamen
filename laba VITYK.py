from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Імпровізована база даних - словник у пам'яті
posts_db = {}

# Клас моделі для постів
class Post(BaseModel):
    title: str
    content: str

# Додати кілька початкових постів
posts_db = {
    1: Post(title="Перший пост", content="Це контент першого поста"),
    2: Post(title="Другий пост", content="Це контент другого поста")
}

# Створення кінцевої точки /version
@app.get("/version")
async def version():
    return {"version": "1.0"}

# Створення кінцевої точки /posts
@app.post("/posts/")
async def create_post(post: Post):
    post_id = len(posts_db) + 1
    posts_db[post_id] = post
    return {"message": "Пост успішно створений", "post_id": post_id}

# Створення кінцевої точки /posts/{post_id}
@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Пост не знайдений")
    posts_db[post_id] = post
    return {"message": "Пост успішно оновлений"}

# Створення кінцевої точки /posts/{post_id}
@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Пост не знайдений")
    del posts_db[post_id]
    return {"message": "Пост успішно видалений"}

# Створення кінцевої точки /stats
@app.get("/stats")
async def stats():
    stats_data = {}
    for path, route in app.routes:
        path_count = route.call_count if hasattr(route, "call_count") else 0
        stats_data[path] = path_count
    return stats_data

# Тестові сценарії
# - version
# - posts (POST)
# - posts (PUT)
# - posts (DELETE)
# - stats

# Тестовий сценарій для кінцевої точки /version
def test_version():
    response = app.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "1.0"}

# Тестовий сценарій для кінцевої точки /posts (POST)
def test_create_post():
    new_post = {"title": "Третій пост", "content": "Це контент третього поста"}
    response = app.post("/posts/", json=new_post)
    assert response.status_code == 200
    assert response.json().get("message") == "Пост успішно створений"

# Тестовий сценарій для кінцевої точки /posts (PUT)
def test_update_post():
    updated_post = {"title": "Оновлений другий пост", "content": "Це оновлений контент другого поста"}
    response = app.put("/posts/2", json=updated_post)
    assert response.status_code == 200
    assert response.json().get("message") == "Пост успішно оновлений"

# Тестовий сценарій для кінцевої точки /posts (DELETE)
def test_delete_post():
    response = app.delete("/posts/1")
    assert response.status_code == 200
    assert response.json().get("message") == "Пост успішно видалений"

# Тестовий сценарій для кінцевої точки /stats
def test_stats():
    response = app.get("/stats")
    assert response.status_code == 200
    assert response.json().get("/version") == 1
    assert response.json().get("/posts/") == 2
    assert response.json().get("/posts/{post_id}") == 0

