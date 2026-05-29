class SaldoInsuficiente(Exception):
    pass

class SinStock(Exception): #primero pongo mis excepciones para evitar problemas adelante o que se rompa
    pass

class AccesoDenegado(Exception):
    pass

class CaracterInvalido(Exception):
    pass

class Persona:
    def __init__(self, nombre, apellido, mail, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.telefono = telefono

class Usuario(Persona): #hago esto para que se hereden los datos de la clase persona y el 0 en saldo como valor predeterminado sino no ingreso otro 
    def __init__(self, nombre, apellido, mail, telefono, username, password, rol, saldo = 0):
         super().__init__(nombre, apellido, mail, telefono)
         self.username = username
         self.password = password
         self.saldo = saldo
         self.rol = rol
         
class Cliente(Usuario):
    def __init__(self, nombre, apellido, mail, telefono, username, password, saldo = 0):
        super().__init__(nombre, apellido, mail, telefono, username, password, "Comprador", saldo)
        self.historial_compras = []
        self.carrito = []
            
class Producto: 
    def __init__(self, nombre, precio, stock, descripcion):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.descripcion = descripcion
        
    def reducir_stock(self, cantidad):
        if cantidad > self.stock:
            raise SinStock(f"No hay más stock de {self.nombre}")
        
        self.stock -= cantidad
        
    def ingresar_stock(self, cantidad):
        if cantidad <=0:
            raise CaracterInvalido("La cantidad debe ser mayor a 0")
        
        self.stock += cantidad
    

class Venta: 
    def __init__(self, cliente, vendedor = None):
        self.cliente = cliente
        self.vendedor = vendedor
        self.producto = []
        self.total= 0
        
    def operacion_venta(self, producto, cantidad):
            if cantidad > producto.stock:
                raise SinStock(f"No hay más stock de {producto.nombre}")
            
            producto.reducir_stock(cantidad)
            self.cliente.carrito.append((producto, cantidad))
            
            compra_estimada = producto.precio * cantidad
            self.total += compra_estimada
            
            print(f"Se ha añadido al carrito de compra")
            
    def pagar_compra(self):
        if self.cliente.saldo < self.total:
            for prod, cant in self.cliente.carrito:
                prod.ingresar_stock(cant)
            self.cliente.carrito = []
            raise SaldoInsuficiente(f"Error, no tiene saldo suficiente")
        
        self.cliente.saldo -= self.total
        self.cliente.historial_compras.append(self)
        self.cliente.carrito = []
        print("Compra exitosa, vuelva pronto")
        
            
class Datos: #para organizarme y tener un lugar donde se guarden mis datos y usuarios, listas donde se van a colocar los datos
    def __init__(self): 
        self.usuarios = []
        self.clientes = []
        self.productos = []
        self.ventas = []
        self.usuario_activo = None #variable con este nombre que va a tener nombre o valor despues
        
        self.datos_iniciales() #llamo para ejecutar
     #ALGUNOS datos puestos para verificar si funhciojna o no
    
    def datos_iniciales(self):
        admin = Usuario("Admin", "General", "adminpymarket@tienda.com", "11800000", "administrador", "1234","Administrador", saldo=0)
        vendedor = Usuario("Juan", "Pepito", "juanpe@tienda.com", "11695677", "vendedor", "2222", "Vendedor", saldo=0)
        self.usuarios.append(admin)
        self.usuarios.append(vendedor)
        
        c1 = Cliente("Milagros", "Chavez", "milagros@mail.com", "11334455", "agr0s", "2345", 150000.0)
        self.usuarios.append(c1)
        
        p1 = Producto("Monster blanca", 3500, 10, "Bebida energética de 473 ml")
        p2 = Producto("Monster amarilla", 3200, 4, "Bebida energética de 473 ml")
        self.productos.append(p1)
        self.productos.append(p2)        

def loggin(sistema):
    intentos = 0
    while intentos < 3:
        print("\n--- Inicie sesión ---")
        u = input("Username: ")
        p = input("Password: ")
        
        for usuario in sistema.usuarios:
            if usuario.username == u and usuario.password == p:
              print(f"Bienvenido/a {usuario.username}")
              sistema.usuario_activo = usuario
              return True
        
        intentos += 1
        print(f"Error, usuario o contraseña incorrectos")

    return False

def menu(sistema):
    if not sistema.usuario_activo:
        print("Inicie sesión primero")
        return
    
    compra_actual = Venta(cliente=sistema.usuario_activo)
    
    while True:
        print("\n-------- Bienvenido a la tienda Pymarket --------")
        print("\n-------- Menu principal --------")
        
        print("1. Módulos")
        print("2. Reportes")
        print("3. Salida")
        
        opcion_principal = input("Seleccione una opción: ")
        
        if opcion_principal == "1":
            
            if sistema.usuario_activo.rol == "Comprador":
                
                while True:
                    print("\n-------- Menu Pymarket --------")
                    print("1. Productos")
                    print("2. Carrito")
                    print("3. Pagos")
                    print("4. Información personal")
                    print("5. Salir")
                    
                    opcion_compra = input("Seleccione una opción: ")
                    
                    if opcion_compra == "1":
                        print("\n--- Productos ---")
                    
                        for prod in sistema.productos:
                            print(f"{prod.nombre} / Precio: ${prod.precio} / Stock: {prod.stock}")
                        
                        #agregar una variable de busqueda para expandir despues, basicamente el sistema de compras del los super
                        
                    elif opcion_compra == "2":
                        print("\n--- Carrito ---")
                            
                        if len(sistema.usuario_activo.carrito) == 0:
                            
                            print("El carrito está vacío")      
                                              
                        else:
                            for prod, cant in sistema.usuario_activo.carrito:
                                subtotal = prod.precio * cant
                                print(f"{prod.nombre} x {cant} u / Subtotal: ${subtotal}")
                        
                        print(f"\nTotal a pagar: ${compra_actual.total}")
                        
                        nombre_carrito = input("Ingrese el nombre del producto que desea llevar: ")
                        
                        producto_elegido = None
                            
                        for prod in sistema.productos:
                            if prod.nombre.lower() == nombre_carrito.lower():
                                producto_elegido = prod
                                break
                        
                        if producto_elegido is None:
                            print(f"No se encontró ningún producto llamado {nombre_carrito}")
                            
                            continue
                        
                        try:
                            cantidad = int(input("Ingrese la cantidad del producto que desea llevar: "))
                            if cantidad <= 0:
                                print("Error, debe ser mayor a 0")
                                continue
                                
                            compra_actual.operacion_venta(producto_elegido, cantidad)         
                                
                        except SinStock as e:
                            print(e)
                                
                    elif opcion_compra == "3":
                        print("\n--- Pagos ---")
                        if len(sistema.usuario_activo.carrito) == 0:
                            print("Todavía no se ha agregado nada al carrito, ingrese un productopara continuar")
                            continue
                        
                        print(f"Total acumulado a pagar: ${compra_actual.total}")
                        try:
                            compra_actual.pagar_compra()
                            sistema.ventas.append(compra_actual) #basicamente se guarda en el sitema la compra
                            compra_actual = Venta(cliente=sistema.usuario_activo)
                            
                        except SaldoInsuficiente as e:
                            print(e)
                            compra_actual = Venta(cliente=sistema.usuario_activo) #es como un ticket, la venta le coresponde a usuario tal (usuario activo en mi sisteja)
                    
                    elif opcion_compra == "4":
                        print("\n--- Información Personal ---")
                        print(f"Nombre Completo: {sistema.usuario_activo.nombre} {sistema.usuario_activo.apellido}")
                        print(f"Mail: {sistema.usuario_activo.mail}")
                        print(f"Telefono: {sistema.usuario_activo.telefono}")
                        print(f"Usuario: {sistema.usuario_activo.username}")
                        print(f"Contraseña: {sistema.usuario_activo.password}")
                        
                    elif opcion_compra == "5":
                        break
                        
                    
            else:
                while True:
                    print("\n-------- Administración  --------")
                    print("1. Administrar Productos")
                    print("2. Administrar Clientes")
                    print("3. Registrar Ventas")
                    print("4. Menu principal")
                            
                    opcion_admin = input("Seleccione una gestión: ")
                    
                    if opcion_admin == "1":
                        print("\n--- Administrar Stock ---")
                        for prod in sistema.productos:
                            print(f"{prod.nombre} / Stock actual: {prod.stock} / Descripción {prod.descripcion}")
                            
                        seleccion = input("Ingrese el nombre del producto que desea reponer: ")
                        
                        producto_buscado = None
                        
                        for prod in sistema.productos:
                            if prod.nombre.lower() == seleccion.lower():
                                producto_buscado = prod
                                break
                            
                        if producto_buscado is None:
                            print(f"No se encontró el producto {seleccion}")
                            
                            continue

                        try:
                            cantidad = int(input("Cantidad de stock a ingresar: "))
                            
                            producto_buscado.ingresar_stock(cantidad)
                            print("Stock actualizado correctamente.")
                            
                        except (ValueError):
                            print("Error en los datos ingresados.")
                            
                        except CaracterInvalido as e:
                            print(e)
                            
                    elif opcion_admin == "2":
                        print("\n--- Usuarios registrados ---")
                        for user in sistema.usuarios:
                            print(f"{user.username} / Rol: {user.rol} / Mail: {user.mail}")
                            
                    elif opcion_admin == "3":
                        print("\n--- Registro de ventas ---")
                        print(f"Se han registrado {len(sistema.ventas)} ventas.")
                        
                    elif opcion_admin == "4":
                        break 
                    
        elif opcion_principal == "2":
            if sistema.usuario_activo.rol == "Comprador":
                print("Los reportes comerciales solo los puede ver el personal autorizado.")
                        
            else:
                print("\n--- Reportes comerciaes ---")
                total_caja = 0
                for factura in sistema.ventas:
                    total_caja += factura.total
                
                print(f"Recaudación total de la caja: ${total_caja}")
                print(f"Cantidad total de transacciones: {len(sistema.ventas)}")
                    
        elif opcion_principal == "3":
            break
        
        else:
            print("Opción invalida")

                        
                                
if __name__ == "__main__":
    base_sistema = Datos()
    
    if loggin(base_sistema):
        menu(base_sistema)
        
        
# agregar
# una opcion para atras y no ir al menu de una
#cambiar lo de la compra
# ver el tema de guardar