



productList = [
    Product(id=1, name="mobile", description="A high-end smartphone", price=85000, quantity=20),
    Product(id=2, name="laptop", description="A powerful gaming laptop", price=120000, quantity=15),
    Product(id=3, name="tablet", description="A versatile tablet for work and play", price=50000, quantity=25)
]

@app.get("/products", response_model=List[Product])
def get_all_products():
    # Placeholder for product retrieval logic
    return productList



@app.get("/product/{id}")
def get_one_product(id: int):
    return productList[id-1]