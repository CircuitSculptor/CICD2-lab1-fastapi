from fastapi import FastAPI,HTTPException

app = FastAPI(title="Product Service")

PRODUCTS = {
    1: {"id": 1, "name": "Laptop", "price": 899.0},
    2: {"id": 1, "name": "Mouse", "price": 25.0},
}

@app.get("/product/{prodcut_id}")
def get_product(product_id: int):
    product = PRODUCTS.get(product_id)
    if  product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product