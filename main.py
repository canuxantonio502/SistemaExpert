# ================================================================
# SISTEMA EXPERTO: Diagnóstico de PC
# Implementación con motor de inferencia hacia adelante
# ================================================================

# ──────────────────────────────────────────────────────────────
# COMPONENTE 1: BASE DE CONOCIMIENTO
# Aquí vive el conocimiento del experto técnico.
# Cada regla tiene: id, condiciones (lista de síntomas requeridos),
# conclusión y un factor de confianza de 0 a 1.
# ──────────────────────────────────────────────────────────────

base_de_conocimiento = [
    {
        "id": "R01",
        "descripcion": "Fuente de poder dañada",
        "condiciones": ["no_enciende", "sin_luces", "sin_sonido"],
        "conclusion": "Revisar o reemplazar la fuente de poder",
        "confianza": 0.92
    },
    {
        "id": "R02",
        "descripcion": "Falla de RAM",
        "condiciones": ["enciende", "pitidos_arranque", "sin_video"],
        "conclusion": "Probar con módulos de RAM de a uno",
        "confianza": 0.88
    },
    {
        "id": "R03",
        "descripcion": "Falla de tarjeta de video",
        "condiciones": ["enciende", "pantalla_negra", "sin_pitidos"],
        "conclusion": "Revisar tarjeta de video y conexiones del monitor",
        "confianza": 0.80
    },
    {
        "id": "R04",
        "descripcion": "Problemas de almacenamiento",
        "condiciones": ["enciende", "inicia_lento", "disco_al_100"],
        "conclusion": "Verificar salud del disco duro con herramienta SMART",
        "confianza": 0.85
    },
    {
        "id": "R05",
        "descripcion": "Infección por malware",
        "condiciones": ["enciende", "inicia_lento", "ventilador_siempre_activo"],
        "conclusion": "Escanear con antivirus y revisar procesos en segundo plano",
        "confianza": 0.72
    },
    {
        "id": "R06",
        "descripcion": "Driver o RAM dañada",
        "condiciones": ["enciende", "pantalla_azul_frecuente"],
        "conclusion": "Actualizar drivers y testear memoria RAM con MemTest86",
        "confianza": 0.87
    },
    {
        "id": "R07",
        "descripcion": "Sobrecalentamiento",
        "condiciones": ["enciende", "se_apaga_solo", "calor_excesivo"],
        "conclusion": "Limpiar ventiladores y reaplicar pasta térmica",
        "confianza": 0.90
    },
    {
        "id": "R08",
        "descripcion": "Batería de la BIOS agotada",
        "condiciones": ["enciende", "hora_desconfigurada", "error_cmos_checksum"],
        "conclusion": "Reemplazar la batería CR2032 de la placa madre",
        "confianza": 0.95
    },
    {
        "id": "R09",
        "descripcion": "Conflicto de periféricos o corto en puerto USB",
        "condiciones": ["enciende", "se_apaga_solo", "bucle_reinicio_inmediato"],
        "conclusion": "Desconectar todos los periféricos y probar encender solo con componentes esenciales",
        "confianza": 0.78
    },
    {
        "id": "R10",
        "descripcion": "Falla de conectividad a red (Hardware o Driver)",
        "condiciones": ["enciende", "sin_internet", "icono_red_con_alerta"],
        "conclusion": "Reiniciar adaptador de red, reinstalar driver o verificar cable Ethernet",
        "confianza": 0.82
    },
    {
        "id": "R11",
        "descripcion": "Ficheros de sistema corruptos",
        "condiciones": ["enciende", "bucle_reparacion_automatica", "no_inicia_sistema"],
        "conclusion": "Ejecutar comando SFC /scannow o CHKDSK desde la consola de recuperación",
        "confianza": 0.80
    },
    {
        "id": "R12",
        "descripcion": "Problema de retroiluminación de pantalla (Laptop o Monitor)",
        "condiciones": ["enciende", "pantalla_negra", "video_de_fondo_con_linterna"],
        "conclusion": "Revisar inverter de la pantalla o cable flex de video",
        "confianza": 0.89
    }
]



# ──────────────────────────────────────────────────────────────
# COMPONENTE 2: BASE DE HECHOS (Working Memory)
# Estado actual del caso. Usamos un set de Python para
# representar los síntomas presentes (eficiente para búsqueda).
# ──────────────────────────────────────────────────────────────

base_de_hechos = set()  # vacía al inicio, se llena con los síntomas

# ──────────────────────────────────────────────────────────────
# COMPONENTE 3: MOTOR DE INFERENCIA
# Funciones de equiparación y resolución de conflictos
# ──────────────────────────────────────────────────────────────

def equiparar(base_conocimiento, base_de_hechos):
    """
    Proceso de equiparación (pattern matching).
    Retorna todas las reglas cuyas condiciones están satisfechas
    por los hechos actuales. Esto es el 'conflict set'.
    """
    conflict_set = []
    for regla in base_conocimiento:
        # Verificar si TODOS los síntomas de la regla están en los hechos
        # set.issubset() es O(len(condiciones)), más eficiente que un bucle
        if set(regla['condiciones']).issubset(base_de_hechos):
            conflict_set.append(regla)
    return conflict_set


def resolver_conflictos_ordenado(conflict_set):
    """
    Estrategia de resolución de conflictos: mayor confianza.
    Si hay empate, preferir la regla con más condiciones (más específica).
    """
    if not conflict_set:
        return []
    return sorted(
        conflict_set,
        key=lambda r: (r['confianza'], len(r['condiciones'])),
        reverse=True
    )


def inferir(base_conocimiento, base_de_hechos):
    """
    Motor de inferencia principal.
    Ejecuta el ciclo de equiparación → resolución → ejecución.
    """
    print()
    print('━' * 55)
    print('  MOTOR DE INFERENCIA INICIADO')
    print('━' * 55)
    print(f'  Hechos ingresados: {base_de_hechos}')
    print()

    conflict_set = equiparar(base_conocimiento, base_de_hechos)

    if not conflict_set:
        print('  ⚠ No se encontraron reglas aplicables.')
        print('  Considera agregar más síntomas o revisar la base de conocimiento.')
        return

    print(f'  Reglas que aplican (conflict set): {[r["id"] for r in conflict_set]}')
    print()

    # Ahora 'lista_ordenada' contiene todas las reglas candidatas de mayor a menor confianza
    lista_ordenada = resolver_conflictos_ordenado(conflict_set)
    
    # Extraemos la primera regla (la ganadora por máxima prioridad)
    regla_ganadora = lista_ordenada[0]

    print('  DIAGNÓSTICO')
    print('  ───────────────────────────────────────────────────')
    print(f'  Regla aplicada: {regla_ganadora["id"]} — {regla_ganadora["descripcion"]}')
    print(f'  Recomendación:  {regla_ganadora["conclusion"]}')
    print(f'  Confianza:      {regla_ganadora["confianza"] * 100:.0f}%')
    print()

    # COMPONENTE 4: INTERFAZ DE EXPLICACIÓN
    print('  TRAZABILIDAD DEL RAZONAMIENTO')
    print('  ───────────────────────────────────────────────────')
    print(f'  Síntomas que activaron la regla: {regla_ganadora["condiciones"]}')
    
    if len(lista_ordenada) > 1:
        # Ahora mostramos las descartadas manteniendo el nuevo orden de confianza que calculamos
        descartadas = [r['id'] for r in lista_ordenada[1:]]
        print(f'  Reglas descartadas por menor prioridad/confianza (en orden): {descartadas}')
    print('━' * 55)


# ──────────────────────────────────────────────────────────────
# COMPONENTE 5: INTERFAZ DE USUARIO
# ──────────────────────────────────────────────────────────────

PREGUNTAS = {
    "no_enciende":              "¿El equipo NO enciende (sin luces, sin sonido)?",
    "sin_luces":                "¿No hay ninguna luz LED encendida?",
    "sin_sonido":               "¿No se escucha ningún sonido al encender?",
    "enciende":                 "¿El equipo SÍ enciende (hay luces y/o sonido)?",
    "pitidos_arranque":         "¿Se escuchan pitidos (beeps) al encender?",
    "sin_video":                "¿La pantalla no muestra absolutamente nada?",
    "pantalla_negra":           "¿La pantalla queda en negro (sin pitidos)?",
    "sin_pitidos":              "¿No se escuchan pitidos?",
    "inicia_lento":             "¿El equipo tarda más de 3 minutos en iniciar?",
    "disco_al_100":             "¿El administrador de tareas muestra disco al 100%?",
    "ventilador_siempre_activo":"¿El ventilador está siempre a máxima velocidad?",
    "pantalla_azul_frecuente":  "¿Aparece pantalla azul (BSOD) con frecuencia?",
    "se_apaga_solo":            "¿El equipo se apaga solo sin advertencia?",
    "calor_excesivo":           "¿El chasis está muy caliente al tacto?",
    "hora_desconfigurada":       "¿La hora y fecha del sistema se desconfiguran al apagar el equipo?",
    "error_cmos_checksum":       "¿Aparece un mensaje de error como 'CMOS Checksum Error' al arrancar?",
    "bucle_reinicio_inmediato":  "¿El equipo se reinicia en un bucle infinito a los pocos segundos de encender?",
    "sin_internet":              "¿El equipo no tiene acceso a internet (ni por Wi-Fi ni por cable)?",
    "icono_red_con_alerta":      "¿El icono de red muestra un triángulo amarillo o una cruz roja?",
    "bucle_reparacion_automatica":"¿El sistema se queda atrapado en la pantalla de 'Reparación automática'?",
    "no_inicia_sistema":         "¿El sistema operativo no logra cargar y se queda congelado en el logo?",
    "video_de_fondo_con_linterna":"¿Si apuntas con una linterna a la pantalla negra logras ver el fondo de tu escritorio?"
}

def consultar():
    print()
    print('=' * 55)
    print('  SISTEMA EXPERTO: Diagnóstico de Computador')
    print('  1 - Responder preguntas para llegar a un diágnostico')
    print('  2 - Confirmar un diagnóstico (Backward-Chain)')
    print('=' * 55)
    print()
    opc = int(input('Seleccione a opción a ejecutar:'))

    if opc == 1:
        print('  Responde s (sí) o n (no) a cada pregunta')
        print('=' * 55)
        print()
        for sintoma, pregunta in PREGUNTAS.items():
            resp = input(f'  {pregunta} [s/n]: ').strip().lower()
            if resp == 's':
                base_de_hechos.add(sintoma)

        inferir(base_de_conocimiento, base_de_hechos)
    elif opc == 2:
        print('=' * 55)
        print()
        meta = input('Ingrese la regla a comprobar (R##):').upper()
        hechos = set()
        resultado = backward_chain(meta, base_de_conocimiento, hechos, PREGUNTAS)
        
        if resultado:
            print(f"\n[+] RESULTADO: El diagnóstico {meta} ha sido CONFIRMADO con los síntomas ingresados.")
        else:
            print(f"\n[-] RESULTADO: El diagnóstico {meta} ha sido DESCARTADO porque faltan síntomas clave.")
    else:
        print('Opción inválida')


def backward_chain(meta, base_conocimiento, hechos, preguntas_dict, visitados=None):
    """
    Evalúa si se puede llegar a una 'meta' (diagnóstico/regla) mediante encadenamiento hacia atrás.
    """
    # Inicializamos el set de nodos visitados para evitar ciclos infinitos en reglas cruzadas
    if visitados is None:
        visitados = set()
        
    if meta in visitados:
        return False
    visitados.add(meta)

    # CASO BASE 1: La meta ya es un hecho confirmado previamente
    if meta in hechos:
        return True

    # Buscar si la meta es el ID de alguna regla en nuestra base de conocimiento
    regla = next((r for r in base_conocimiento if r["id"] == meta), None)

    if regla:
        # Es una regla (diagnóstico). Debemos probar todas sus condiciones recursivamente.
        print(f"\n[?] Evaluando hipótesis: {regla['descripcion']} ({regla['id']})")
        todas_cumplidas = True
        
        for condicion in regla["condiciones"]:
            # Llamada recursiva: intentamos probar cada condición de la regla
            if not backward_chain(condicion, base_conocimiento, hechos, preguntas_dict, visitados):
                todas_cumplidas = False
                print(f"    [-] Se descartó '{regla['id']}' porque falla la condición: {condicion}")
                break # Fallo rápido: si una condición no se cumple, la regla se descarta
        
        if todas_cumplidas:
            print(f"    [+] ¡Hipótesis '{regla['id']}' confirmada!")
            return True
        else:
            return False

    else:
        # CASO BASE 2: No es una regla, es un síntoma (hoja del árbol).
        # Como no está en los 'hechos' y no hay reglas para deducirlo, preguntamos al usuario.
        if meta in preguntas_dict:
            respuesta = input(f"  {preguntas_dict[meta]} [s/n]: ").strip().lower()
            if respuesta == 's':
                hechos.add(meta) # Guardamos el hecho para no volver a preguntar
                return True
            else:
                return False
        else:
            print(f"  ⚠ Advertencia: No se reconoce el síntoma ni la regla '{meta}'.")
            return False


# Ejecutar
consultar()