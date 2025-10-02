productos = ["Café Americano", "Capuchino", "Té", "Sándwich", "Pastelito"]
precios = [5000, 6000, 4000, 8000, 7000]
stock = [10, 10, 10, 10, 10]
ventas_totales = 0
pedidos_totales = 0

def mostrar_menu():
    print("\n--- MENÚ ---")
    for i in range(len(productos)):
        print(i + 1, ".", productos[i], "- $", precios[i], "(Stock:", stock[i], ")")

def procesar_pedido():
    global ventas_totales, pedidos_totales
    
    nombre_cliente = input("\nNombre del cliente: ")
    pedido_productos = []
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione producto (número) o '0' para finalizar: ")
        if opcion == "0":
            break
        
        opcion = int(opcion) - 1
        if opcion < 0 or opcion >= len(productos):
            print("Opción no válida.")
            continue
        
        cantidad = input("Cantidad de " + productos[opcion] + ": ")
        if cantidad == "":
            print("Cantidad inválida.")
            continue
        cantidad = int(cantidad)
        
        if cantidad <= 0:
            print("Cantidad inválida.")
            continue
        if cantidad > stock[opcion]:
            print("Solo hay", stock[opcion], "disponibles. Se agregará el máximo posible.")
            cantidad = stock[opcion]
        
        pedido_productos.append([opcion, cantidad])

    if len(pedido_productos) == 0:
        print("Pedido vacío, cancelado.")
        return
    
    subtotal = 0
    for i in range(len(pedido_productos)):
        idx = pedido_productos[i][0]
        cantidad = pedido_productos[i][1]
        subtotal += precios[idx] * cantidad
    
    descuento = 0
    if subtotal > 30000:
        descuento = subtotal * 0.10
    
    for i in range(len(pedido_productos)):
        idx = pedido_productos[i][0]
        cantidad = pedido_productos[i][1]
        if productos[idx] == "Sándwich" or productos[idx] == "Pastelito":
            if cantidad >= 3:
                descuento += precios[idx] * cantidad * 0.05
    
    subtotal_desc = subtotal - descuento
    iva = subtotal_desc * 0.19
    total = subtotal_desc + iva
    
    print("\n--- FACTURA ---")
    print("Cliente:", nombre_cliente)
    for i in range(len(pedido_productos)):
        idx = pedido_productos[i][0]
        cantidad = pedido_productos[i][1]
        print("-", productos[idx], "x", cantidad, "=", "$", precios[idx] * cantidad)
    
    print("Subtotal:", "$", subtotal)
    print("Descuento:", "-$", int(descuento))
    print("Subtotal con descuento:", "$", int(subtotal_desc))
    print("IVA (19%):", "$", int(iva))
    print("TOTAL A PAGAR:", "$", int(total))
    
    for i in range(len(pedido_productos)):
        idx = pedido_productos[i][0]
        cantidad = pedido_productos[i][1]
        stock[idx] -= cantidad
    
    ventas_totales += total
    pedidos_totales += 1

def resumen_dia():
    print("\n=== RESUMEN DEL DÍA ===")
    print("Pedidos procesados:", pedidos_totales)
    print("Ingresos totales:", "$", int(ventas_totales))
    
    max_vendidos = max(stock)
    if max_vendidos > 0:
        for i in range(len(stock)):
            if stock[i] == max_vendidos:
                print("Producto más vendido:", productos[i])
    
    agotados = []
    for i in range(len(stock)):
        if stock[i] == 0:
            agotados.append(productos[i])
    
    if len(agotados) > 0:
        print("Productos agotados:", end=" ")
        for i in range(len(agotados)):
            if i == len(agotados) - 1:
                print(agotados[i])
            else:
                print(agotados[i], end=", ")
    else:
        print("No hubo productos agotados hoy.")

while True:
    print("\n=== CAFETERÍA ===")
    print("1. Procesar pedido")
    print("2. Mostrar resumen del día")
    print("3. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        procesar_pedido()
    elif opcion == "2":
        resumen_dia()
    elif opcion == "3":
        print("Saliendo del sistema...")
        resumen_dia()
        break
    else:
        print("Opción no válida.")
