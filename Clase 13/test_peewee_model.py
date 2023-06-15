from peewee_model import *

if __name__== "__main__" :
    #Creamos nuevas instancias de Category
    category1 = Category(name="shoes")
    category2 = Category(name="technology")

    #Creamos nuevas instancias de Product
    product1 = Product(name="NIKE Sneakers", price=35000.50, category=category1)
    product2 = Product(name="SAMSUNG Galaxy Watch5 Pro", price=275000, category=category2)

    #Guardamos los cambios con save() para insertar los registros
    try:
        category1.save()
        category2.save()
    except IntegrityError as e:
        print("Error al insertar en la tabla categories.", e)
    try:
        product1.save()
        product2.save()
    except IntegrityError as e:
        print("Error al insertar en la tabla products.", e)

    #También podemos insertar nuevos registros con create()
    try:
        product3 = Product.create(name="IPHONE 14 Pro", price=1220500, category=category2)
    except IntegrityError as e:
        print("Error al insertar en la tabla products.", e)
    try:
        category3 = Category.create(name="decoration")
        print("Id categoría:",category3.id)
        print(f"Nueva categoría de productos: Id={category3.id}, Name={category3.name}")
    except IntegrityError as e:
        print("Error al insertar en la tabla categories.", e)

    #Seleccionamos datos con get()
    category1 = Category.select().where(Category.name == 'shoes').get()
    #es equivalente a:
    category1 = Category.get(Category.name == 'shoes')
    # SELECT * FROM categories WHERE id = 1
    category_id = 1
    category1 = Category.get(category_id)

    #Seleccionamos datos con select()
    # SELECT * FROM categories WHERE id = 1 LIMIT 1;
    category1 = Category.select().where(Category.id == category_id).first()

    #Obtenemos el listado de todas la categorías:
    print("\nListado de todas la categorías y la cantidad de productos de cada una:")
    """ SELECT categories.name, COUNT(*) FROM categories 
        INNER JOIN products ON categories.id = products.category_id
        GROUP BY categories.name """
    for categ in Category.select():
        print(categ.name, categ.products.count(), "productos")
        #print(categ)

    #Obtenemos el listado de todos los productos y su categoría ordenados por nombre:
    print("\nListado de todos los productos ordenados por nombre:")
    """ SELECT products.*,categories.name FROM products 
        INNER JOIN categories ON products.category_id = categories.id
        ORDER BY products.name """
    query = Product.select().order_by(Product.name)
    for prod in query:
        print(prod.name, "- precio: $", prod.price, "- categoría:", prod.category.name)

    #Creamos nuevas instancias de Sale con save() y create()
    sale1 = Sale(product=product2, quantity=2)
    try:
        sale1.save()
        Sale.create(product=product1, quantity=3)
        Sale.create(product=product1, quantity=1)
        Sale.create(product=product3, quantity=1)
    except IntegrityError as e:
        print("Error al insertar en la tabla sales.", e)

    #Obtenemos el listado de todas la ventas:
    print("\nListado de todas la ventas realizadas:")
    """ SELECT sales.*, (products.price * sales.quantity) as amount_total
        FROM sales
        INNER JOIN products ON sales.product_id = products.id """
    for sale in Sale.select():
        #print(sale.date.strftime("%d/%m/%Y"), "-", sale.product.name, " - Cant:", sale.quantity, " - Total: $",sale.total)
        print(sale)

    #Monto total de ventas agrupado por producto
    print("\nMonto total de ventas agrupado por producto y ordenado por monto total descendente:")
    """ SELECT products.name, (products.price * sales.quantity) as amount_total
        FROM products
        INNER JOIN sales ON sales.product_id = products.id
        GROUP BY products.name ORDER BY amount_total DESC """
    amount_total = fn.SUM(Product.price * Sale.quantity).alias('amount_total')
    query = (Sale
            .select(Product.name, amount_total)
            .join(Product, on=(Sale.product == Product.id))
            .group_by(Product.name)
            .order_by(amount_total.desc()))
    for sale in query:
        print(f"{sale.product.name}, Monto total: $ {sale.amount_total}")

    #Monto total general de ventas
    """ SELECT sum(products.price * sales.quantity) as amount_total
        FROM products
        INNER JOIN sales ON sales.product_id = products.id """
    query = (Sale
            .select(amount_total)
            .join(Product, on=(Sale.product == Product.id)).get())
    print("\nMonto total general de ventas:\n$", query.amount_total,"\n")
    sqlite_db.close()