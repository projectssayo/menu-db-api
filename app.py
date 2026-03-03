from fastapi import FastAPI
from pymongo import MongoClient

url = r'mongodb+srv://projectssayo_db_user:1234@test.mdv08ad.mongodb.net/?retryWrites=true&w=majority&appName=test'

client = MongoClient(
    url,
    serverSelectionTimeoutMS=3000,
    connectTimeoutMS=3000,
    socketTimeoutMS=3000
)

db = client["menu_db"]
menu_collection = db["menu_items"]
signature_collection = db["signature_items"]

app = FastAPI()


@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {
        "Get all menu items": "/get_all",
        "Get signature food": "/get_signature_food",
        "Insert new item": "/insert (POST)",
        "Insert signature item": "/insert_signature (POST)",
        "Update full item": "/update_full (PUT)",
        "Delete menu item": "/delete (DELETE)",
        "Delete signature item": "/delete_signature_food (DELETE)"
    }


# GET ALL MENU
@app.get("/get_all")
def get_all():
    try:
        items = []
        for item in menu_collection.find():
            item.pop("_id", None)
            items.append(item)
        return {"success": True, "menu": items}
    except Exception as e:
        return {"success": False, "message": str(e)}


# GET SIGNATURE FOOD
@app.get("/get_signature_food")
def get_signature_food():
    try:
        items = []
        for item in signature_collection.find():
            item.pop("_id", None)
            items.append(item)
        return {"success": True, "signature_food": items}
    except Exception as e:
        return {"success": False, "message": str(e)}


# INSERT MENU ITEM
@app.post("/insert")
def insert(
    name: str,
    description: str,
    price: int = 0,
    category: str = "",
    image_url: str = None,
    available: bool = True
):
    try:
        item = {
            "name": name,
            "description": description,
            "price": price,   # Stored as NUMBER now
            "category": category,
            "image_url": image_url,
            "available": available
        }

        menu_collection.insert_one(item)
        return {"success": True}

    except Exception as e:
        return {"success": False, "message": str(e)}


# INSERT SIGNATURE ITEM
@app.post("/insert_signature")
def insert_signature(
    name: str,
    description: str,
    price: int = 0,
    category: str = "",
    image_url: str = None,
    available: bool = True
):
    try:
        item = {
            "name": name,
            "description": description,
            "price": price,
            "category": category,
            "image_url": image_url,
            "available": available
        }

        signature_collection.insert_one(item)
        return {"success": True}

    except Exception as e:
        return {"success": False, "message": str(e)}


# UPDATE FULL ITEM
@app.put("/update_full")
def update_full(
    name: str,
    new_name: str = None,
    description: str = None,
    price: int = None,
    category: str = None,
    image_url: str = None,
    available: bool = None
):
    try:
        update_data = {}

        if new_name is not None:
            update_data["name"] = new_name
        if description is not None:
            update_data["description"] = description
        if price is not None:
            update_data["price"] = price
        if category is not None:
            update_data["category"] = category
        if image_url is not None:
            update_data["image_url"] = image_url
        if available is not None:
            update_data["available"] = available

        if not update_data:
            return {"success": False, "message": "No fields provided"}

        result = menu_collection.update_many(
            {"name": {"$regex": name, "$options": "i"}},
            {"$set": update_data}
        )

        return {"success": True, "updated_count": result.modified_count}

    except Exception as e:
        return {"success": False, "message": str(e)}


# DELETE MENU ITEM
@app.delete("/delete")
def delete(name: str):
    try:
        result = menu_collection.delete_many(
            {"name": {"$regex": name, "$options": "i"}}
        )
        return {"success": True, "deleted_count": result.deleted_count}
    except Exception as e:
        return {"success": False, "message": str(e)}


# DELETE SIGNATURE ITEM
@app.delete("/delete_signature_food")
def delete_signature_food(name: str):
    try:
        result = signature_collection.delete_many(
            {"name": {"$regex": name, "$options": "i"}}
        )
        return {"success": True, "deleted_count": result.deleted_count}
    except Exception as e:
        return {"success": False, "message": str(e)}
