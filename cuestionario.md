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
```
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


### Diseña un diagrama que represente el proceso de traducción de direcciones virtuales a físicas en un sistema con memoria virtual.


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
```
Hello world
```

## 4.1 Dispositivos y Manejadores de Dispositivos

### Explica la diferencia entre dispositivos de bloque y dispositivos de carácter. Da un ejemplo de cada uno.
- **Dispositivos de bloque:** Acceden a datos en bloques fijos, como discos duros o SSDs.
  - **Ejemplo:** Disco duro.
- **Dispositivos de carácter:** Transfieren datos byte por byte, como teclados o ratones.
  - **Ejemplo:** Teclado.

### Diseña un programa que implemente un manejador de dispositivos sencillo para un dispositivo virtual de entrada.
```
Hello world
```

## 4.2 Mecanismos y Funciones de los Manejadores de Dispositivos

### Investiga qué es la interrupción por E/S y cómo la administra el sistema operativo. Escribe un ejemplo en pseudocódigo para simular este proceso.
- Es un mecanismo donde el dispositivo notifica al sistema operativo que una operación de E/S ha finalizado, liberando al procesador de esperar activamente.
- **Proceso:**
  1. El dispositivo genera una interrupción.
  2. El CPU suspende la ejecución actual y llama al manejador de interrupción.
  3. El manejador procesa la solicitud y reanuda el proceso interrumpido.

### Escribe un programa que utilice el manejo de interrupciones en un sistema básico de simulación.


## 4.3 Estructuras de Datos para Manejo de Dispositivos

### Investiga y explica qué es una cola de E/S. Diseña una simulación de una cola con prioridad.
- Una estructura de datos que organiza las solicitudes de entrada/salida en espera. Puede implementarse con prioridad para procesar solicitudes críticas antes que las no críticas.
- **Ventajas:**
  - Mejora la eficiencia del sistema.
  - Reduce el tiempo de espera de procesos prioritarios.

### Escribe un programa que simule las operaciones de un manejador de dispositivos utilizando una tabla de estructuras.
```
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


### Implementa un programa en Python, C o java que realice operaciones de entrada/salida asíncronas usando archivos.
```
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
```
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
```
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