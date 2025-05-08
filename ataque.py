class Ataque:
    def __init__(self, nombre: str, tipo: str, puntos_daño: int, 
                 razas_vulnerables: list[str], razas_resistentes: list[str],
                 anim_index: int = 0):  # Nuevo parámetro para índice de animación
        if tipo not in ['corte', 'contundente', 'blaster']:
            raise ValueError("Tipo de ataque debe ser 'corte', 'contundente' o 'blaster'")
        if not (50 <= puntos_daño <= 100):
            raise ValueError("Puntos de daño deben estar entre 50 y 100")
            
        self.nombre = nombre
        self.tipo = tipo
        self.puntos_daño = puntos_daño
        self.razas_vulnerables = razas_vulnerables
        self.razas_resistentes = razas_resistentes
        self.anim_index = anim_index  # Índice de animación asociada

    def __str__(self):
        return f"{self.nombre} ({self.tipo}): {self.puntos_daño} daño"