from fastapi import Depends ,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session , engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware  (
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hello"

products = [
    Product (id=1,name="phone",description="budget phone",price=99,quantity=10),
    Product (id=2,name="laptop",description="gaming laptop",price=999,quantity=6),
    Product (id=3,name="ps5" ,description="playstation",price=9999,quantity=40),
    Product (id=4,name="xbox" ,description="microsoft xbox",price=9999,quantity=90),
]
def get_db():
    db=session() #update
    try:
         yield db   #waiting for others to use it   #yield is a special keyword in Python that turns a function into a generator.
    finally:
        db.close()


def init_db():
    db = session()

    count= db.query(database_models.Product).count

    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump())) #model_dump will give you dictionary
                                                                    # star will give you unpacking            
        db.commit()
init_db()        


@app.get("/products/")
def get_all_products(db : Session = Depends(get_db)):                 #fastapi inject
    
    db_products=db.query(database_models.Product).all()

    return db_products

@app.get("/products/{id}")  #get=take data
def get_product_by_id(id:int,db : Session = Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product     
    return "product not found"


@app.post("/products/")   #post=send data
def add_product(product:Product,db : Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product 



@app.put("/products/{id}")
def update_product(id:int, product: Product,db : Session = Depends(get_db)):
   db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
   if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price
        db_product.quantity=product.quantity
        db.commit()
        return "Product updated"
   else:
        return "No product found"

@app.delete("/products/{id}")
def delete_product(id:int,db : Session = Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        return "product not found"

