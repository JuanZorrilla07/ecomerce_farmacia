class Cart:

    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get("cart")
        montoTotal = self.session.get("cartMontoTotal")
        if not cart:
            cart = self.session['cart'] = {}
            montoTotal = self.session["cartMontoTotal"] = "0"
        
        self.cart = cart
        self.montoTotal = float(montoTotal)    

    def add(self,producuto,cantidad):
        if str(producuto.id) not in self.cart.keys():
            self.cart[producuto.id] = {
                "producuto_id":producuto.id,
                "nombre":producuto.nombre,
                "cantidad":cantidad,
                "precio":str(producuto.precio),
                "imagen":producuto.imagen.url,
                "categoria":producuto.Categoria.nombre,
                "subtotal":str(cantidad * producuto.precio)
            }
        else:
            for key,value in self.cart.items():
                if key == str(producuto.id):
                    value["cantidad"]=str(int(value["cantidad"]) + cantidad)
                    value["subtotal"]=str (float(value["cantidad"]) * float(value["precio"]))
                    break



        self.save()    
    
    def delete(self,producuto):
        producuto_id = str(producuto.id)
        if producuto_id in self.cart:
            del self.cart[producuto_id]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.session["cartMontoTotal"] = "0"

    def save(self):
        """guarda cambios en el carrito de compras"""
        montoTotal = 0

        for key,value in self.cart.items():
            montoTotal += float(value["subtotal"])
        
        self.session["cartMontoTotal"] = montoTotal
        self.session["cart"] = self.cart
        self.session.modified = True