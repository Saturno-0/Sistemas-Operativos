# Respuestas al Formulario

## 3.1 Política y Filosofía

### ¿Cuál es la diferencia entre fragmentación interna y externa? Explica cómo cada una afecta el rendimiento de la memoria.
- **Fragmentación Interna:** Ocurre cuando el espacio asignado a un proceso es mayor al espacio que realmente utiliza. Esto sucede debido a las divisiones fijas de memoria que no se adaptan al tamaño exacto del proceso.
  - **Impacto:** Provoca desperdicio de memoria dentro de los bloques asignados.
- **Fragmentación Externa:** Se produce cuando hay suficiente memoria total disponible, pero está fragmentada en bloques pequeños que no son lo suficientemente grandes para satisfacer una solicitud.
  - **Impacto:** Afecta la capacidad de asignar memoria a nuevos procesos, aunque haya memoria disponible.

### Investiga y explica las políticas de reemplazo de páginas en sistemas operativos. ¿Cuál consideras más eficiente y por qué?
- **FIFO (First-In, First-Out):** Las páginas más antiguas en la memoria se reemplazan primero.
- **LRU (Least Recently Used):** Reemplaza la página que no ha sido usada durante más tiempo.
- **OPT (Optimal):** Reemplaza la página que no será utilizada por el mayor tiempo en el futuro.
- **Segunda oportunidad:** Variante de FIFO que revisa si las páginas han sido usadas recientemente antes de reemplazarlas.

**Política más eficiente:** 
- **LRU** es eficiente en términos de rendimiento general porque se basa en patrones recientes de acceso. Sin embargo, su implementación puede ser más costosa en comparación con FIFO.
## 3.2 Memoria real

### Escribe un programa en C o Python que simule la administración de memoria mediante particiones fijas.
```py
class Partition:
    def __init__(self, size, id):
        self.size = size
        self.id = id
        self.occupied_by = None  # Proceso actual que ocupa esta partición

class Process:
    def __init__(self, id, size):
        self.id = id
        self.size = size

class MemoryManager:
    def __init__(self, partition_sizes):
        self.partitions = [Partition(size, i) for i, size in enumerate(partition_sizes)]

    def allocate_process(self, process):
        for partition in self.partitions:
            if partition.occupied_by is None and process.size <= partition.size:
                partition.occupied_by = process
                print(f"Proceso {process.id} asignado a Partición {partition.id}.")
                return
        print(f"Proceso {process.id} no pudo ser asignado. Memoria insuficiente.")

    def deallocate_process(self, process_id):
        for partition in self.partitions:
            if partition.occupied_by and partition.occupied_by.id == process_id:
                partition.occupied_by = None
                print(f"Proceso {process_id} desalojado de Partición {partition.id}.")
                return
        print(f"Proceso {process_id} no se encontró en ninguna partición.")

    def display_memory(self):
        print("\nEstado de las particiones:")
        print(f"{'Partición':<10}{'Estado':<20}{'Tamaño':<10}")
        print("-" * 40)
        for partition in self.partitions:
            status = f"Proceso {partition.occupied_by.id}" if partition.occupied_by else "Libre"
            print(f"{partition.id:<10}{status:<20}{partition.size:<10}")

# Ejemplo de uso
if __name__ == "__main__":
    partition_sizes = [100, 200, 300, 400]  # Tamaños de las particiones
    memory_manager = MemoryManager(partition_sizes)

    processes = [
        Process(1, 150),
        Process(2, 300),
        Process(3, 50),
        Process(4, 400),
        Process(5, 250),
    ]

    print("\nAsignación de procesos:")
    for process in processes:
        memory_manager.allocate_process(process)

    memory_manager.display_memory()

    # Desasignar un proceso
    print("\nDesasignación de proceso 2:")
    memory_manager.deallocate_process(2)

    memory_manager.display_memory()

    # Asignar un nuevo proceso
    print("\nAsignación de un nuevo proceso 6 de tamaño 200:")
    memory_manager.allocate_process(Process(6, 200))

    memory_manager.display_memory()

```
### Diseña un algoritmo para calcular qué procesos pueden ser asignados a un sistema con memoria real limitada utilizando el algoritmo de "primera cabida".

El algoritmo se creo en pseudocodigo para su mayor entendimiento:
```
Entrada:
  procesos: Lista de procesos, donde cada proceso tiene un ID y tamaño requerido.
  memoria: Lista de particiones de memoria, donde cada partición tiene un ID, tamaño total y espacio disponible.

Salida:
  Asignación de procesos a particiones, o mensaje de "no se puede asignar" si un proceso no cabe.

1. Inicializar asignaciones = {} (diccionario para almacenar la asignación proceso -> partición).
2. Para cada proceso en procesos hacer:
     3. Asignado = False
     4. Para cada partición en memoria hacer:
          5. Si partición.espacio_disponible >= proceso.tamaño entonces:
               6. Asignar el proceso a esta partición: asignaciones[proceso.ID] = partición.ID
               7. Actualizar partición.espacio_disponible -= proceso.tamaño
               8. Asignado = True
               9. Salir del ciclo de particiones.
          Fin Si
     Fin Para
     10. Si no se pudo asignar (Asignado == False) entonces:
          11. Mostrar "El proceso {proceso.ID} no puede ser asignado."
     Fin Si
Fin Para

12. Retornar asignaciones.
```
## 3.3 Organización de Memoria Virtual

### Investiga y explica el concepto de "paginación" y "segmentación" ¿Cuáles son las ventajas y desventajas de cada técnica?
- **Paginación:** Divide la memoria en bloques de tamaño fijo llamados "páginas". Cada página de un proceso puede asignarse a cualquier marco disponible en la memoria física.
  - **Ventajas:**
    - Reduce la fragmentación externa.
    - Simplifica la administración de memoria.
  - **Desventajas:**
    - Introduce fragmentación interna.
    - Requiere tiempo adicional para la traducción de direcciones.
- **Segmentación:** Divide la memoria en bloques de tamaño variable llamados "segmentos", que corresponden a unidades lógicas de un programa (código, datos, pila).
  - **Ventajas:**
    - Mejora la agrupación lógica de datos y código.
    - Facilita la protección y compartición de memoria.
  - **Desventajas:**
    - Sufre de fragmentación externa.
    - Más compleja de implementar.

## 3.4 Administración de memoria virtual

### Escribe un código que implemente el algoritmo de reemplazo de página "Least Recently Used" (LRU).
```py
def lru_page_replacement(pages, frame_count):
    frames = []
    page_faults = 0

    for page in pages:
        if page not in frames:
            page_faults += 1

            if len(frames) < frame_count:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
        else:
            frames.remove(page)
            frames.append(page)

        print(f"Page: {page} -> Frames: {frames}")

    return page_faults

if __name__ == "__main__":
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frame_count = 3

    page_faults = lru_page_replacement(pages, frame_count)

    print(f"\nTotal de fallos de página: {page_faults}")

```

### Diseña un diagrama que represente el proceso de traducción de direcciones virtuales a físicas en un sistema con memoria virtual.
### Flujo de Traducción de Direcciones Virtuales a Físicas

```plaintext
    +------------------------------+
    | Inicio                       |
    +------------------------------+
             |
             v
    +------------------------------+
    | CPU genera dirección virtual |
    +------------------------------+
             |
             v
    +------------------------------+
    | Se consulta la tabla de      |
    | páginas (Page Table)         |
    +------------------------------+
             |
             v
    +------------------------------+
    | ¿La página está en la memoria|
    | principal (RAM)?             |
    +------------------------------+
             |
        +----+----+
        |         |
       Sí         No
        |          |
        v          v
+-----------------+  +---------------------+
| Dirección       | | Cargar la página de  |
| virtual         | | disco a la memoria   |
| se traduce a    | | (swap in)            |
| dirección       | +----------------------+
| física en RAM   |           |
+-----------------+           v
         |           +------------------------+
         v           | Actualizar la tabla    |
+------------------+ | de páginas (Page Table)|
| Dirección física | +------------------------+
| generada y usada |
+------------------+
         |
         v
+------------------+
| Fin              |
+------------------+
```

## 3.5 Integración

### Analiza un sistema operativo moderno (por ejemplo, Linux o Windows) e identifica cómo administra la memoria virtual.
- **Linux:**
  - Utiliza un esquema de paginación con niveles jerárquicos para mapear direcciones virtuales a físicas.
  - Implementa políticas de reemplazo como LRU y variantes.
  - Soporta memoria caché para acelerar el acceso.
- **Windows:**
  - Utiliza tablas de páginas y traducción mediante TLB (Translation Lookaside Buffer).
  - Implementa paginación por demanda para cargar solo las páginas necesarias.
  - Soporta memoria compartida entre procesos.

### Realiza una simulación en cualquier lenguaje de programación que emule el swapping de procesos en memoria virtual.
```py
import random
import time

class SwapSimulation:
    def __init__(self, memory_size, disk_size):
        self.memory_size = memory_size
        self.disk_size = disk_size
        self.memory = []
        self.disk = []
        self.process_counter = 1

    def allocate_process(self):
        process_id = f"P{self.process_counter}"
        self.process_counter += 1
        
        if len(self.memory) < self.memory_size:
            self.memory.append(process_id)
            print(f"Proceso {process_id} cargado en la memoria.")
        else:
            self.swap_out()
            self.memory.append(process_id)
            print(f"Proceso {process_id} cargado en la memoria tras swapping.")

    def swap_out(self):
        process_out = self.memory.pop(0)
        self.disk.append(process_out)
        print(f"Proceso {process_out} movido al disco para liberar espacio.")

    def swap_in(self):
        if self.disk:
            process_in = self.disk.pop(0)
            if len(self.memory) < self.memory_size:
                self.memory.append(process_in)
                print(f"Proceso {process_in} regresado a la memoria desde el disco.")
            else:
                print("No hay espacio suficiente en la memoria para swap-in.")
        else:
            print("No hay procesos para swap-in en el disco.")

    def status(self):
        print(f"\nEstado actual de la simulación:")
        print(f"Memoria RAM: {self.memory}")
        print(f"Disco: {self.disk}")
        print("-" * 50)

def main():
    simulator = SwapSimulation(memory_size=3, disk_size=5)
    
    for _ in range(10):
        simulator.allocate_process()
        time.sleep(1)
        simulator.status()
    
    for _ in range(3):
        simulator.swap_in()
        time.sleep(1)
        simulator.status()

if __name__ == "__main__":
    main()

```

## 4.1 Dispositivos y Manejadores de Dispositivos

### Explica la diferencia entre dispositivos de bloque y dispositivos de carácter. Da un ejemplo de cada uno.
- **Dispositivos de bloque:** Acceden a datos en bloques fijos, como discos duros o SSDs.
  - **Ejemplo:** Disco duro.
- **Dispositivos de carácter:** Transfieren datos byte por byte, como teclados o ratones.
  - **Ejemplo:** Teclado.

### Diseña un programa que implemente un manejador de dispositivos sencillo para un dispositivo virtual de entrada.
```py
import queue

class Device:
    def __init__(self):
        self.input_queue = queue.Queue()
        self.is_active = False

    def activate(self):
        self.is_active = True
        print("Dispositivo activado.")

    def deactivate(self):
        self.is_active = False
        print("Dispositivo desactivado.")

    def read_input(self):
        if self.is_active and not self.input_queue.empty():
            data = self.input_queue.get()
            print(f"Datos leídos: {data}")
        else:
            print("No hay datos disponibles o dispositivo inactivo.")

    def write_input(self, data):
        if self.is_active:
            self.input_queue.put(data)
            print(f"Datos escritos en el dispositivo: {data}")
        else:
            print("Dispositivo inactivo, no se puede escribir.")

class DeviceManager:
    def __init__(self):
        self.device = Device()

    def handle_device(self, action, data=None):
        if action == "activar":
            self.device.activate()
        elif action == "desactivar":
            self.device.deactivate()
        elif action == "leer":
            self.device.read_input()
        elif action == "escribir" and data is not None:
            self.device.write_input(data)
        else:
            print("Acción no válida o falta de datos.")

def main():
    manager = DeviceManager()
    manager.handle_device("activar")
    manager.handle_device("escribir", "Entrada de datos 1")
    manager.handle_device("escribir", "Entrada de datos 2")
    manager.handle_device("leer")
    manager.handle_device("desactivar")
    manager.handle_device("leer")

if __name__ == "__main__":
    main()
```

## 4.2 Mecanismos y Funciones de los Manejadores de Dispositivos

### Investiga qué es la interrupción por E/S y cómo la administra el sistema operativo. Escribe un ejemplo en pseudocódigo para simular este proceso.
- Es un mecanismo donde el dispositivo notifica al sistema operativo que una operación de E/S ha finalizado, liberando al procesador de esperar activamente.
- **Proceso:**
  1. El dispositivo genera una interrupción.
  2. El CPU suspende la ejecución actual y llama al manejador de interrupción.
  3. El manejador procesa la solicitud y reanuda el proceso interrumpido.

### Escribe un programa que utilice el manejo de interrupciones en un sistema básico de simulación.
```py
import random
import time

class Interrupt:
    def __init__(self, id, handler):
        self.id = id
        self.handler = handler

    def trigger(self):
        self.handler(self.id)

class System:
    def __init__(self):
        self.interrupts = []
        self.is_running = False

    def register_interrupt(self, interrupt):
        self.interrupts.append(interrupt)

    def trigger_interrupt(self):
        interrupt = random.choice(self.interrupts)
        print(f"Interrupción {interrupt.id} activada.")
        interrupt.trigger()

    def start(self):
        self.is_running = True
        while self.is_running:
            time.sleep(random.uniform(1, 3))
            self.trigger_interrupt()

    def stop(self):
        self.is_running = False
        print("Sistema detenido.")

def interrupt_handler_1(id):
    print(f"Controlando la interrupción {id} en el sistema.")

def interrupt_handler_2(id):
    print(f"Procesando la interrupción {id} en el sistema.")

def main():
    system = System()
    interrupt1 = Interrupt(1, interrupt_handler_1)
    interrupt2 = Interrupt(2, interrupt_handler_2)

    system.register_interrupt(interrupt1)
    system.register_interrupt(interrupt2)

    system.start()

if __name__ == "__main__":
    main()

```

## 4.3 Estructuras de Datos para Manejo de Dispositivos

### Investiga y explica qué es una cola de E/S. Diseña una simulación de una cola con prioridad.
- Una estructura de datos que organiza las solicitudes de entrada/salida en espera. Puede implementarse con prioridad para procesar solicitudes críticas antes que las no críticas.
- **Ventajas:**
  - Mejora la eficiencia del sistema.
  - Reduce el tiempo de espera de procesos prioritarios.

### Escribe un programa que simule las operaciones de un manejador de dispositivos utilizando una tabla de estructuras.
```c
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_DISPOSITIVOS 10
#define MAX_NOMBRE 20

typedef struct {
    char nombre[MAX_NOMBRE];
    bool activo;
    void (*leer)(void);
    void (*escribir)(const char *datos);
} Dispositivo;

void leer_generico() {
    printf("Leyendo datos del dispositivo\n");
}

void escribir_generico(const char *datos) {
    printf("Escribiendo datos al dispositivo: %s\n", datos);
}

Dispositivo tabla_dispositivos[MAX_DISPOSITIVOS];
int num_dispositivos = 0;

void registrar_dispositivo(const char *nombre) {
    if (num_dispositivos >= MAX_DISPOSITIVOS) {
        printf("Error: No se pueden registrar más dispositivos.\n");
        return;
    }
    
    strcpy(tabla_dispositivos[num_dispositivos].nombre, nombre);
    tabla_dispositivos[num_dispositivos].activo = true;
    tabla_dispositivos[num_dispositivos].leer = leer_generico;
    tabla_dispositivos[num_dispositivos].escribir = escribir_generico;
    num_dispositivos++;
    printf("Dispositivo '%s' registrado exitosamente.\n", nombre);
}

void listar_dispositivos() {
    printf("\nDispositivos registrados:\n");
    for (int i = 0; i < num_dispositivos; i++) {
        printf("%d. Nombre: %s, Estado: %s\n",
               i + 1,
               tabla_dispositivos[i].nombre,
               tabla_dispositivos[i].activo ? "Activo" : "Inactivo");
    }
}

void operar_dispositivo(int indice, const char *operacion, const char *datos) {
    if (indice < 0 || indice >= num_dispositivos) {
        printf("Error: Índice de dispositivo inválido.\n");
        return;
    }

    Dispositivo *dispositivo = &tabla_dispositivos[indice];
    if (!dispositivo->activo) {
        printf("Error: El dispositivo '%s' está inactivo.\n", dispositivo->nombre);
        return;
    }

    if (strcmp(operacion, "leer") == 0) {
        dispositivo->leer();
    } else if (strcmp(operacion, "escribir") == 0) {
        dispositivo->escribir(datos);
    } else {
        printf("Operación no soportada: %s\n", operacion);
    }
}

int main() {
    registrar_dispositivo("Teclado");
    registrar_dispositivo("Pantalla");
    registrar_dispositivo("Impresora");

    listar_dispositivos();

    printf("\nProbando operaciones:\n");
    operar_dispositivo(0, "leer", "");
    operar_dispositivo(1, "escribir", "Hola, mundo!");
    operar_dispositivo(2, "escribir", "Documento importante");

    return 0;
}
```

## 4.4 Operaciones de Entrada/Salida.

### Diseña un flujo que describa el proceso de lectura de un archivo desde un disco magnético. Acompáñalo con un programa básico que simule el proceso.

Flujo de Lectura de un Archivo desde un Disco Magnético

```plaintext
    +------------------+
    | Inicio           |
    +------------------+
            |
            v
    +------------------+
    | Solicitud de     |
    | lectura del      |
    | archivo          |
    +------------------+
            |
            v
    +------------------+
    | Localización del |
    | archivo en el    |
    | disco            |
    +------------------+
            |
            v
    +------------------+
    | Acceso al disco  |
    | (Controlador)    |
    +------------------+
            |
            v
    +------------------+
    | Movimiento del   |
    | cabezal de       |
    | lectura/escritura|
    +------------------+
            |
            v
    +------------------+
    | Lectura de los   |
    | datos desde el   |
    | disco            |
    +------------------+
            |
            v
    +------------------+
    | Transferencia de |
    | datos a la RAM   |
    +------------------+
            |
            v
    +------------------+
    | Finalización     |
    | de la lectura    |
    +------------------+
            |
            v
         +---------+
         | Fin     |
         +---------+
```
```py
import time
import random

class DiscoMagnetico:
    def __init__(self, tamaño_dispositivo):
        self.tamaño = tamaño_dispositivo  # Número de bloques en el disco
        self.datos = self.generar_datos()  # Datos simulados en el disco

    def generar_datos(self):
        """Simula la creación de datos en el disco."""
        return [f'Dato{str(i)}' for i in range(self.tamaño)]

    def leer(self, direccion, bloques):
        """Simula la lectura de bloques desde el disco."""
        print(f"Accediendo a la dirección {direccion}...")
        time.sleep(random.uniform(0.5, 1))  # Simulación de tiempo de espera por el movimiento del cabezal
        datos_leidos = self.datos[direccion: direccion + bloques]
        return datos_leidos

class Sistema:
    def __init__(self, disco):
        self.disco = disco  # El disco en el sistema

    def leer_archivo(self, direccion, bloques):
        """Simula el proceso de leer un archivo del disco"""
        print("Comenzando la lectura del archivo...")
        datos = self.disco.leer(direccion, bloques)
        print("Lectura completada.")
        return datos

# Simulación
if __name__ == "__main__":
    disco = DiscoMagnetico(tamaño_dispositivo=100)
    sistema = Sistema(disco)

    direccion_archivo = 30  # Dirección de inicio donde el archivo comienza
    bloques_archivo = 10  # Número de bloques a leer

    print("Proceso de lectura iniciado...\n")
    datos_archivo = sistema.leer_archivo(direccion_archivo, bloques_archivo)
    print(f"Datos leídos: {datos_archivo}")

```

### Implementa un programa en Python, C o java que realice operaciones de entrada/salida asíncronas usando archivos.
```py
import asyncio
import aiofiles

async def escribir_archivo(nombre_archivo, contenido):
    async with aiofiles.open(nombre_archivo, mode='w') as archivo:
        await archivo.write(contenido)
        print(f"Se escribió en el archivo {nombre_archivo}")

async def leer_archivo(nombre_archivo):
    async with aiofiles.open(nombre_archivo, mode='r') as archivo:
        contenido = await archivo.read()
        print(f"Contenido del archivo {nombre_archivo}:\n{contenido}")
        return contenido

async def main():
    nombre_archivo = "archivo_asincrono.txt"
    contenido = "Esta es una prueba de E/S asíncrona.\n¡Funciona correctamente!"
    await escribir_archivo(nombre_archivo, contenido)
    await leer_archivo(nombre_archivo)

asyncio.run(main())
```

## 4.5 Integración
### Escribe un programa que implemente el algoritmo de planificación de discos "Elevator (SCAN)".
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_REQUESTS 100

void scan_algorithm(int requests[], int n, int start, bool direction, int disk_size) {
    int seek_sequence[MAX_REQUESTS];
    int seek_count = 0, total_seek_operations = 0, current_position = start;
    bool processed[MAX_REQUESTS] = {false};

    printf("\nOrden inicial de peticiones: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", requests[i]);
    }

    while (seek_count < n) {
        int next_index = -1;
        int min_distance = abs(disk_size - current_position) + 1;

        for (int i = 0; i < n; i++) {
            if (!processed[i]) {
                int distance = abs(requests[i] - current_position);
                bool valid_direction = direction ? (requests[i] >= current_position) : (requests[i] <= current_position);

                if (valid_direction && distance < min_distance) {
                    next_index = i;
                    min_distance = distance;
                }
            }
        }

        if (next_index == -1) {
            direction = !direction;
            printf("\nCambio de direcci\u00f3n hacia %s.\n", direction ? "arriba" : "abajo");
        } else {
            processed[next_index] = true;
            seek_sequence[seek_count++] = requests[next_index];
            total_seek_operations += abs(requests[next_index] - current_position);
            current_position = requests[next_index];
        }
    }

    printf("\nSecuencia de movimientos del cabezal: ");
    for (int i = 0; i < seek_count; i++) {
        printf("%d ", seek_sequence[i]);
    }

    printf("\n\nOperaciones totales de movimiento: %d\n", total_seek_operations);
}

int main() {
    int n, start, disk_size, requests[MAX_REQUESTS] = {0};
    bool direction;

    printf("Ingrese el tama\u00f1o del disco: ");
    scanf("%d", &disk_size);

    printf("Ingrese el n\u00famero de peticiones: ");
    scanf("%d", &n);

    if (n > MAX_REQUESTS) {
        printf("Error: Demasiadas peticiones. El m\u00e1ximo permitido es %d.\n", MAX_REQUESTS);
        return 1;
    }

    printf("Ingrese las posiciones de las peticiones: ");
    for (int i = 0; i < n; i++) {
        scanf("%d", &requests[i]);
    }

    printf("Ingrese la posici\u00f3n inicial del cabezal: ");
    scanf("%d", &start);

    if (start < 0 || start > disk_size) {
        printf("Error: Posici\u00f3n inicial fuera de rango.\n");
        return 1;
    }

    printf("Ingrese la direcci\u00f3n inicial (1 para hacia arriba, 0 para hacia abajo): ");
    scanf("%d", &direction);

    scan_algorithm(requests, n, start, direction, disk_size);

    return 0;
}

```

### Diseña un sistema que maneje múltiples dispositivos simulados (disco duro, impresora, teclado) y muestra cómo se realiza la comunicación entre ellos.
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_DEVICES 3

typedef enum { DISK, PRINTER, KEYBOARD } DeviceType;

typedef struct {
    DeviceType type;
    char name[20];
    int id;
} Device;

void communicate(Device sender, Device receiver, const char *message) {
    printf("%s(ID: %d) -> %s(ID: %d): %s\n", 
           sender.name, sender.id, receiver.name, receiver.id, message);
}

void simulate_disk_operations(Device device) {
    printf("%s(ID: %d): Performing disk operations...\n", device.name, device.id);
}

void simulate_printer_operations(Device device) {
    printf("%s(ID: %d): Printing documents...\n", device.name, device.id);
}

void simulate_keyboard_input(Device device) {
    printf("%s(ID: %d): Capturing user input...\n", device.name, device.id);
}

int main() {
    Device devices[MAX_DEVICES] = {
        {DISK, "Hard Disk", 1},
        {PRINTER, "Printer", 2},
        {KEYBOARD, "Keyboard", 3}
    };

    printf("Simulating device communications and operations:\n\n");

    simulate_disk_operations(devices[0]);
    simulate_printer_operations(devices[1]);
    simulate_keyboard_input(devices[2]);

    printf("\nSimulating inter-device communication:\n\n");

    communicate(devices[2], devices[0], "Send saved file for storage.");
    communicate(devices[0], devices[1], "Print the stored file.");
    communicate(devices[1], devices[2], "Printing completed.\n");

    return 0;
}
```

## Avanzados

### Optimización de operaciones de E/S con caché
- Los sistemas operativos modernos utilizan **memoria caché** para almacenar temporalmente datos frecuentemente usados.
- **Beneficios:**
  - Reduce los accesos al disco, que son más lentos.
  - Mejora el rendimiento general del sistema.
  - Minimiza el tiempo de respuesta en operaciones repetidas.