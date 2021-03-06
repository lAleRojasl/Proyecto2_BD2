import csv
import string
import random
from random import randint
from datetime import date, timedelta
import operator
import numpy as np

#Estrategia de produccion ATO - Assemble To Order
#products ordered by customers are produced quickly and are customizable to a certain extent.
#The assemble-to-order (ATO) strategy requires that the basic parts for the product are already
#manufactured but not yet assembled. Once an order is received, the parts are assembled quickly and sent to the customer.

checkers = ["Juan Gomez H","Melissa Hernandez C","Pedro Rodriguez O","Javier Viquez T","Victor Arias B"]

autorizadores = ["Ana Laura Viquez M","Hector Venavidez T","Carolina Morera D","Manuel Hernandez G"]

carriers = ["FedEx","UPS","Correos de Costa Rica","DHL","GoPato"]

distribuidores = ["Allied Electronics","Neward","Toyo Communication Equipment CO.",
                  "NIC Components Corporations","RCD Components","Megaphase LLC","RARA Electronics Corp.",
                  "Avnet Inc.", "Future Electronics", "Digi-Key Corp.", "Bisco Industries Inc."]

mats_comunes = [("Battery","B"), ("Capacitor","C"), ("Microprocessor","MP"), ("Cathode Ray Tube","CTR"),
              ("Fuse","F"), ("Gas Discharge Tube","GDT"), ("Wire Link", "WL"), ("Motor","M"),
              ("Junction Gate Field-effect transistor","JFET"),("Glass Lense","GL"), ("Circuit Breaker","CBK"),("Resistor","R"),
              ("Operational Amplifier","OP"),("Silicon controlled rectifier","SCR"),("Switch","SW"), ("Peltier Cooler","PCL"),
              ("Tunnel Diode", "TDE"),("Metal Oxide Semiconductor FET","MOSFET"),("Static Induction transistor","SIT"),
              ("Filament lamp","FLP"),("LCD Screen","LCD"),("Light Emitting Diode","LED"), ("Phototube","PTT"),("Nixie Tube","NXT"),
              ("Transformer","T"),("Thin film transistor","TFT"),("Digital signal processor","DSP"),
              ("Integrated Circuit","IC"),("Variable capacitor","VC"),("Plastic Casing","PCS"),("Digital Signal Processor","DSP"),
              ("Relay","RLA"),("Field effect Transistor","FET"),("Very Large Scale Integration","VLSI"),
              ("Valve Tube","V"),("Crystal resonator","CRS"),("Test Point","TP"),("Zener Diode","ZDE"), ("Motherboard","MB")]

#productos IoT Nombre - Descripcion - link
productos = [("Ankuoo NEO Smart Switch","http://www.ankuoo.com/products/?sort=2","SS","1","59.99"),
             ("BayitHome Switch","http://www.bayithomeautomation.com/products/bayit-switch/","SS","1","79.99"),
             ("BlueSpray Irrigation","https://www.bluespray.net/","IRS","2","89.99"),
             ("Blossom Sprinkler System","https://www.myblossom.com/","IRS","2","99.99"),
             ("GreenIQ Smart Garden","http://greeniq.co/","IRS","2","185.99"),
             ("Neurio Energy Monitor","https://www.neur.io/","EM","3","219.99"),
             ("Eyedro Electricity Monitor","http://eyedro.com/home-electricity-monitors/","EM","3","250.99"),
             ("Smappee Electicity Monitor","http://www.smappee.com/eu_es/monitor-de-energia/","EM","3","229.99"),
             ("Smappee Gas&Water Monitor","http://www.smappee.com/eu_es/monitor-de-agua-y-gas/","GWM","4","315.99"),
             ("AcuRite Sensors","https://www.acurite.com/indoor-outdoor-thermometer-humidity-sensor-hd-display-my-acurite.html","THM","5","80.99"),
             ("Keen Temp&Air Control","https://keenhome.io/","THM","5","99.99"),
             ("ConnectSense Temperature Sensor","https://www.connectsense.com/wireless-temperature-sensor","THM","5","75.99"),
             ("SensorPush Monitors","http://www.sensorpush.com/","THM","5","88.85"),("LIFX SmartBulbs","https://www.lifx.com/","SLB","6","75.95"),
             ("Phillips Hue Bulbs","http://www2.meethue.com/en-us/productdetail/philips-hue-white-and-color-ambiance-br30-e26","SLB","6","60.99"),
             ("FluxSmart Bulbs","https://www.fluxsmartlighting.com/products/flux-bluetooth","SLB","6","75.99"),
             ("August Smart Lock","http://august.com/products/august-smart-lock/","SLK","7","140.95"),
             ("August Doorbell Cam","http://august.com/products/doorbell-camera/","SLK","7","99.95"),
             ("Lockitron Bolt","https://lockitron.com/","SLK","7","120.99"),
             ("Chipolo Tracker","https://chipolo.net/products","TKR","8","59.99"),("Lapa KeyTracker","https://findlapa.com/","TKR","8","49.99"),
             ("Neposmart Outdoor Camera","https://neposmart.com/outdoor-camera/","CAM","9","399.99"),
             ("Neposmart Indoor Camera","https://neposmart.com/indoor-camera/","CAM","9","420.95")]

max_mats = 6000
base_mats = []
base_prods = []
matsXProds = []
clientes = []

#Cargamos los clientes pre-generados
with open('clientes.csv', 'r') as clientesCSV:
    reader = csv.reader(clientesCSV)
    clientes = list(reader)
print("Cargando clientes pre-generados..................OK")


#Debemos simular los events ocurridos en un lapso de los ultimos 5 años
#Para esto usamos la libreria datetime para iterar sobre estas fechas de manera precisa.
startDate = date(2012, 5, 7)  # start date (lunes)
endDate = date(2017, 5, 31)  # end date

#Funcion para devolver la fecha X dias despues de la fecha actual
def getNextDate(currentDate, moveDays=1):
    return currentDate + timedelta(days=moveDays)

#dato = getNextDate(startDate, 20)
#print(dato)
#print(getNextDate(dato,20))

#Funcion para generar numeros seriales random de materiales o productos
#Tambien se usa para generar tracking numbers aleatorios
def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generateMats():
    generated_mats = 0
    #Primero vamos a generar una lista de materiales iniciales
    #En base a estos se van a generar las "entradas" y "salidas" para que sea mas realista
    #Luego de realizar las entradas y salida nos va a quedar un 
    while(generated_mats < 8000):
        #Material random basado en la lista de posibilidades
        random_mat = random.choice(mats_comunes)
        random_mat_name = random_mat[0]
        random_mat_letter = random_mat[1]
         
        #Modelo generado basado en el material seleccionado.
        #Formato: Letra + '-' + numero. Ej: C-592 para un Capacitor
        mat_modelNum = randint(0,1000)
        mat_model = random_mat_letter + '-' + str(mat_modelNum)

        #Cantidad disponible (Stock).
        #Deben haber suficientes materiales para 100 dispositivos
        #Vamos a usar stocks entre 50 y 70 hasta llegar a un total de 8000
        random_stock = randint(40,65)
            
        #Total de materiales que hemos generado
        generated_mats += random_stock

        #Generamos un costo del material
        random_cost = round(random.uniform(0.15,1.15),2)

        #Lista con la base de materiales iniciales
        base_mats.append([random_mat_name,mat_model,random_stock,random_cost])
    print("Materiales base generados..................OK")
generateMats()
        
# Datos de los productos.
#   - Estos no se guardan en el csv hasta despues de la simulacion de 5 años.
def generateProducts():
    for i in range(0,len(productos)):
        prod = productos[i]
        prod_models = randint(4,7)
        for x in range(0,prod_models):
            #Formato: Letra + '-' + numero. Ej: TKR-52 para productos de Smart Tracking
            prod_modelNum = randint(0,1000)
            mod_prct = random.uniform(-0.05,0.06)
            temp_price = float(prod[4])
            new_price = str(round((temp_price + temp_price*mod_prct), 2))
            prod_model = prod[2] + '-' + str(prod_modelNum)
            base_prods.append([prod[0],prod[1],prod_model,prod[3],new_price])
    print("Productos base generados..................OK")
generateProducts()

#Teniendo los productos y los materiales base
#Podemos simular cuales materiales se necesitan para ensamblar cada producto
#   - Vamos a asumir que un dispositivo necesita en promedio ~60 materiales
#     divididos entre 10 a 20 tipos. Esto es, un dispositivo puede necesitar
#     por ejemplo, 6 transistores, 4 resistores, 2 baterias, 1 motor, etc.
with open('MaterialXProducto.csv', 'w', newline='') as mXpCSV:
    #-Encabezados-
    spamwriter = csv.writer(mXpCSV, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["ProductoID","MaterialID","Cantidad"])
    prodNum = 0
    cant_prods = len(base_prods)
    for i in range(0, cant_prods):
        prodNum += 1
        #cantidad de materiales necesarios para un producto
        distribucion_mats = randint(7,15)
        #escogemos los 10 a 25 materiales aleatorios (sin repetir) 
        selected_mats = random.sample(range(1,len(base_mats)),distribucion_mats)
        for matXprod in selected_mats:
            mat_cant = randint(1,5)
            matsXProds.append([prodNum, matXprod, mat_cant])
            spamwriter.writerow([prodNum, matXprod, mat_cant])
    print("Generando Materiales necesarios por Producto..................OK")

#Debemos simular las entradas y salidas de materiales durante 5 años
#Aspectos a considerar:
#   - Deben ser 80000 movimientos, esto es aproximadamente 43.8 movimientos por dia
#     O 333 movimientos por semana.
#   VENTAS:
#   - Las ventas deben sumar minimo 9000 en los ultimos 5 años, lo que son 1800 al año, 150 por mes o 37 por semana.
#   SALIDAS:
#   - Para tratar de hacerlo distribuido vamos a generar entre 4 y 8 ventas diarias, para clientes aleatorios.
#   ENTRADAS:
#   - Vamos a asumir que las entradas (re-supply) son en base a los componentes que se
#     van gastando, por lo que a principio de cada semana (lunes) se hacen ordenes de compra con los componentes que estan
#     por debajo de cierta cantidad minima (30). Esta orden llega a la bodega entre 2 a 5 dias despues.
#     finalmente tambien se simula si la orden tuvo algun inconveniente (llego tarde, partes defectuosas, devoluciones,etc)
#     sin embargo la probabilidad de que esto pase es muy baja. Aprox. 0.001% de posibilidad o 10 de cada 10000.

print("Iniciando simulacion de datos durante 5 años....")
currentDate = startDate
# ------------ CSV de Variaciones Precios ------------- #
with open('VariacionPrecio.csv','w',newline='') as variacionesCSV:
    #-Encabezados-
    varsWriter = csv.writer(variacionesCSV, delimiter=',',
                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
    varsWriter.writerow(["ProductoID","NuevoPrecio","FechaMod"])
    #Agregamos los precios iniciales de los productos
    for prodIndex in range(len(base_prods)):
        varsWriter.writerow([prodIndex,base_prods[prodIndex][4],str(currentDate)])
    # ------------ CSV de Ordenes de Compra ------------- #
    with open('OrdenDeCompra.csv','w',newline='') as ordenesCSV:
        #-Encabezados-
        ordenWriter = csv.writer(ordenesCSV, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)
        ordenWriter.writerow(["OrdenID","Autorizador","FechaOrden","Distribuidor","TotalFacturado","Estado","TotalCancelado","FechaEstado"])
        # ------------ CSV de Lineas X Orden de Compra ------------- #
        with open('LineasXOrden.csv','w',newline='') as lineasCSV:
            #-Encabezados-
            lineaWriter = csv.writer(lineasCSV, delimiter=',',
                                   quotechar='"', quoting=csv.QUOTE_MINIMAL)
            lineaWriter.writerow(["OrdenID","MaterialID","Cantidad","PrecioUnitario","PrecioTotal"])
            # ------------ CSV de Ventas Por Cliente ------------- #
            with open('VentasXCliente.csv','w',newline='') as ventasCSV:
                #-Encabezados-
                ventaWriter = csv.writer(ventasCSV, delimiter=',',
                                       quotechar='"', quoting=csv.QUOTE_MINIMAL)
                ventaWriter.writerow(["ClienteID","ProductoID","CostoProducto","FechaCompra"])
                # ------------ CSV de Salidas De Materiales ------------- #
                with open('MovSalidas.csv','w',newline='') as salidasCSV:
                    #-Encabezados-
                    salidaWriter = csv.writer(salidasCSV, delimiter=',',
                                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    salidaWriter.writerow(["BoletaID","MaterialID","Cantidad"])
                    # ------------ CSV de Despachos De Productos ------------- #
                    with open('Despachos.csv','w',newline='') as despachosCSV:
                        #-Encabezados-
                        despachoWriter = csv.writer(despachosCSV, delimiter=',',
                                               quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        despachoWriter.writerow(["NombreChequeador","FechaDespacho","HoraDespacho","Carrier","NumeroGuia",
                                                 "CantidadDespachada","PaisDestino","ClienteID"])
                        
                        #Variables iniciales
                        delta = endDate - startDate
                        currentMonth = currentDate.month
                        currentYear = currentDate.year
                        min_prods_changed = int(len(base_prods)/3)
                        max_prods_changed = int(len(base_prods) - min_prods_changed)
                        ticket_number = 0
                        order_number = 0
                        total_invoice = 0
                        order_result = "Recibido"
                        order_date = currentDate
                        #Iteramos sobre todas las fechas desde 1-5-2012 hasta 31-5-2017 (~5 años)
                        while currentDate < endDate:
                            currentDate = getNextDate(currentDate)

                            #Los domingos no se trabaja, nos lo brincamos
                            if(currentDate.weekday() == 7):
                                currentDate = getNextDate(currentDate)
                    
                            if(currentDate.weekday() == 1):
                                new_order = False
                                order_fulfilled = True
                                total_cancelled = 0
                                # A principio de semana (cada lunes) se realizan las ordenes de compra
                                # Estas son en base a los materiales que se han gastado mas y estan ahora
                                # por debajo de cierta cantidad minima (30), se compran materiales para subir el stock de nuevo a 60-80.
                                for matIndx in range(len(base_mats)):
                                    if(int(base_mats[matIndx][2]) < 60):
                                        #Nueva orden
                                        if(not new_order):
                                            new_order = True
                                            order_number += 1
                                            # Existe una muy baja probabilidad de que la orden haya tenido algun problema
                                            # La orden puede llegar a tiempo, llegar tarde, o si llegar con partes defectuosas
                                            # Las probabilidades de que las ultimas 2 ocurran son muy bajas (0.4% cada una)
                                            order_result_num = np.random.choice(np.arange(1, 7), p=[0.23, 0.23, 0.23, 0.23, 0.04, 0.04]) 
                                            # Tiempo de llegada normal (si sale de 1 a 4)
                                            order_result = "Recibido"
                                            order_date = getNextDate(currentDate,int(order_result_num))
                                            # El paquete llego tarde (si sale 5)
                                            if(order_result_num == 5):
                                                order_result = "Recibido con atraso"                                                
                                            # El paquete tuvo que ser devuelto por partes defectuosas (si sale 6)
                                            if(order_result_num == 6):
                                                order_result = "Devuelto por componentes defectuosos"
                                                #En este caso se hacen las lineas de orden pero no se actualiza el inventario
                                                order_fulfilled = False
                                                #De igual manera el total cancelado es 0, pues se devolvieron los materiales 
                                                total_cancelled = 0
                                        
                                        # ------------ CSV de Lineas por Orden (Detalle de la Orden) ------------- #
                                        mats = base_mats[matIndx]
                                        rand_supply = randint(80,100)
                                        resupply = rand_supply - int(mats[2])
                                        precio_unitario = float(mats[3])
                                        totalXmat = round(resupply * precio_unitario,2)
                                        total_invoice =  round(total_invoice + totalXmat, 2)
                                        
                                        #Consecutivo de Orden, IDMaterial, cantidad, precio_unitario, totalXmaterial
                                        lineaWriter.writerow([order_number, matIndx,resupply, precio_unitario, totalXmat])
                                        
                                        if(order_fulfilled):
                                            #Volvemos a "ingresar" los materiales al stock (solo si la orden llego bien)
                                            mats[2] = rand_supply

                                
                                # Total cancelado por financiero (si la orden llego bien, si no es 0)
                                if(order_fulfilled):
                                    mod_prct = random.uniform(0.05,0.13)
                                    total_cancelled = round((total_invoice + (total_invoice*mod_prct)), 2)
                                if(new_order):
                                    # ------------ CSV de Orden_de_Compra (Entrada) ------------- #
                                    auth_name = random.choice(autorizadores)
                                    distrib = randint(1,len(distribuidores))
                                    #Consecutivo de Orden, autorizado_por, fecha_orden,total_facturado, distribuidor, estado, total_cancelado, fecha_estado
                                    ordenWriter.writerow([order_number,auth_name, currentDate, distrib, total_invoice, order_result, total_cancelled, order_date])
                                    total_invoice = 0
                                
                                
                                # Cada mes se ajustan los precios de ciertos productos para controlar la demanda y ganancias
                                # Esto tambien se debe en parte a que los precios de los materiales tambien varia.
                                if(currentMonth != currentDate.month):
                                    # Cantidad de precios de productos a modificar
                                    cant_mod_prods = randint(min_prods_changed,max_prods_changed)
                                    # Escogemos aleatoriamente cuales se modifican (sin repetir)
                                    selected_prods = random.sample(range(len(base_prods)),cant_mod_prods)
                                    # Moficamos cada precio con +- ~%5 uniform(-5,6)
                                    for prodIndex in selected_prods:
                                        mod_prct = random.uniform(-0.05,0.06)
                                        temp_price = float(base_prods[prodIndex][4])
                                        new_price = str(round((temp_price + temp_price*mod_prct), 2))
                                        base_prods[prodIndex][4] = new_price
                                        # ------------ CSV de Variaciones de Precio ------------- #
                                        varsWriter.writerow([prodIndex+1,new_price,str(currentDate)])
                                    currentMonth = currentDate.month
                                
                            daily_mats = []
                            # Cada dia se hacen entre 6 y 9 ventas a clientes
                            daily_sales = randint(7,10)
                            # Determinamos cuales clientes compraron esos productos y lo guardamos
                            # Utilizamos un while ya que un cliente puede comprar mas de 1 producto
                            while daily_sales > 0:
                                # Tenemos un listado de 450 clientes unicos
                                # por lo que escogemos aleatoriamente cual hizo la compra
                                selected_client = randint(0,449)
                                # Cantidad de productos que este cliente compro
                                amount_purchased = randint(1,3)
                                # Cuales productos compro exactamente, basado en el catalogo
                                purchased_prods = random.sample(range(1,len(base_prods)),amount_purchased)
                                # Lo agregamos al registro de ventas
                                for prodIndex in purchased_prods:
                                    # ------------ CSV de Ventas ------------- #
                                    # IDCliente, IDProducto, costo_producto, fecha_compra
                                    ventaWriter.writerow([selected_client+1, prodIndex+1, base_prods[prodIndex][4], currentDate])

                                    # Las salidas de materiales son en base a los productos vendidos diariamente
                                    # Para esto revisamos los datos de matsXProds que nos indica la "receta" de cada producto
                                    required_mats = [[mXp[1],mXp[2]] for mXp in matsXProds if mXp[0] == prodIndex]
                                    for mat in required_mats:
                                        #Los daily_mats son los que se usaran para registrar las salidas diarias de materiales
                                        daily_mats.append(mat)
                                        # Debemos reducir la cantidad de materiales disponibles (stock) en base_mats
                                        # Esto determina al inicio de cada semana cuales materiales se deben comprar (re-supply).
                                        cant_mat = int(base_mats[mat[0]][2])
                                        base_mats[mat[0]][2] = str(cant_mat - int(mat[1]))

                                # ----------- CSV de Despachos ----------- #
                                # Los despachos se realizan 2 dias despues de la venta, pues es lo que tardan
                                # en hacer las salidas de materiales (1d) y en ensamblarlos (1d). Se hace un despacho por cliente.
                                # Id del chequeador encargado de revisar el despacho
                                checker_name = random.choice(checkers)

                                # Los paquetes suelen despacharse entre las 7:00 y las 12:00
                                rand_time = str(randint(7,13))+':00:00'
                                    
                                # Nombre del carrier
                                carrier_name = random.choice(carriers)

                                pais = clientes[selected_client][5]
                                av = ""
                                if(pais == "Guatemala"): av = "GTM"                                
                                if(pais == "Costa Rica"): av = "CRC"                                
                                if(pais == "Nicaragua"): av = "NIC"
                                if(pais == "Panama"): av = "PAN"
                                    
                                # Nombre del chequeador, fecha, hora, nombre del carrier
                                # numero de guia, cantidad despachada, pais destino y consumidor
                                despachoWriter.writerow([checker_name, currentDate, rand_time, carrier_name,
                                                    av+'-'+id_generator(14), amount_purchased, pais, selected_client+1 ])

                                #Actualizamos cantidad de ventas
                                daily_sales -= amount_purchased
                                
                            # ------------ CSV de Salidas ------------- #
                            ticket_number += 1
                            daily_mats_array = np.array(daily_mats)
                            unq, unq_inv = np.unique(daily_mats_array[:, 0], return_inverse=True)
                            salida_mats = np.zeros((len(unq), daily_mats_array.shape[1]), dtype=daily_mats_array.dtype)
                            salida_mats[:, 0] = unq
                            np.add.at(salida_mats[:, 1:], unq_inv, daily_mats_array[:, 1:])
                            #Guardamos las salidas al csv
                            for mat in salida_mats:
                                # consecutivo de boleta, ID Material, cantidad
                                salidaWriter.writerow([ticket_number, mat[0], mat[1]])
                            
                            
                            if(currentDate.year != currentYear):
                                print("-->Datos del año "+str(currentYear)+" generados...........OK")
                                currentYear = currentDate.year

                        print("-->Datos del año "+str(currentYear)+" generados...........OK")
#Guardamos los productos con los precios mas recientes (luego de la simulacion de los 5 años)
with open('Productos.csv', 'w', newline='') as prodCSV:
    csvwriter = csv.writer(prodCSV, delimiter=',',
                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["Nombre","Link","Modelo","Categoria","PrecioVenta"])
    for prod in base_prods:
        csvwriter.writerow(prod)
    print("Guardando ultimo estado de productos a prodsData.csv..................OK")

#Guardamos los materiales con los stocks mas recientes (luego de la simulacion de los 5 años)
with open('Materiales.csv', 'w', newline='') as matsCSV:    
    matWriter = csv.writer(matsCSV, delimiter=',',
                           quotechar='"', quoting=csv.QUOTE_MINIMAL) 
    matWriter.writerow(["Nombre","Modelo","Stock","CostoUnitario"])
    sortedlist = sorted(base_mats)
    for mat in sortedlist:
        matWriter.writerow([mat[0],mat[1],mat[2],mat[3]])
    print("Guardando ultimo estado de materiales a matsData.csv..................OK")

#Excel: 

