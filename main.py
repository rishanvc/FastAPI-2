from models import *
from fastapi import FastAPI
from database import session,engine
import database_models


app=FastAPI()

database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "welcome"

products=[
    Product(id=1,name="Phone",description="a good mobile",price=699.66,quantity=50),
    Product(id=2,name="laptop",description="a good laptop",price=999.66,quantity=20),
    Product(id=3,name="pen",description="a good pen",price=50.66,quantity=10),
    Product(id=4,name="car",description="a good car",price=99.66,quantity=80),
]


def init_db():
    db=session()
    count=db.query(database_models.Product).count()

    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()





@app.get("/products")
def get_all_products():
  # db=session()
 #  db.query()
    return products




@app.get("/product/{id}")
def get_product_by_id(id:int):
    for product in products:
        if product.id==id:
            return product
    return "product not found"

@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id: int,product: Product):
    for i in range(len(products)):
        if products[i].id==id:
            products[i]=product
            return "product added successfully"
    return "no products found"

@app.delete("/product")
def delete_product(id :int,product: Product):
    for i in range(len(products)):
        if products[i].id==id:
            del products[i]
            return "product deleted successfully"
    return "product not found"





#API STUDY WITHOUT CONNECTING PSQL
#---------------------------------------------

# @app.get("/")
# def greet():
#     return "welcome"

# products=[
#     Product(id=1,name="Phone",description="a good mobile",price=699.66,quantity=50),
#     Product(id=2,name="laptop",description="a good laptop",price=999.66,quantity=20),
#     Product(id=3,name="pen",description="a good pen",price=50.66,quantity=10),
#     Product(id=4,name="car",description="a good car",price=99.66,quantity=80),
# ]

# @app.get("/products")
# def get_all_products():
#     db=session()
#     db.query()
#     return products




# @app.get("/product/{id}")
# def get_product_by_id(id:int):
#     for product in products:
#         if product.id==id:
#             return product
#     return "product not found"

# @app.post("/product")
# def add_product(product: Product):
#     products.append(product)
#     return product

# @app.put("/product")
# def update_product(id: int,product: Product):
#     for i in range(len(products)):
#         if products[i].id==id:
#             products[i]=product
#             return "product added successfully"
#     return "no products found"

# @app.delete("/product")
# def delete_product(id :int,product: Product):
#     for i in range(len(products)):
#         if products[i].id==id:
#             del products[i]
#             return "product deleted successfully"
#     return "product not found"