from models import *
from fastapi import FastAPI,Depends
from database import session,engine
import database_models
from sqlalchemy.orm import Session


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




def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()



@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    db_products=db.query(database_models.Product).all()
    return db_products



@app.get("/product/{id}")
def get_product_by_id(id:int,db:Session=Depends(get_db)):
    db_products=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_products:
        return db_products
    return "product not found"

@app.post("/product")
def add_product(product: Product,db:Session=Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit( )
    return product

@app.put("/product")
def update_product(id: int,product: Product,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "Product updated"
    else:
        return "product not found"
            
    
   

@app.delete("/product")
def delete_product(id :int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
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