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
