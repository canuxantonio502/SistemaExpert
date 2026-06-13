# Sistema Experto: Diagnóstico de 💻:

Este proyecto implementa un Sistema Experto para el diagnóstico de fallas comunes en computadoras. El sistema es capaz de deducir un problema a partir de síntomas generales que hayan siido respondidos por el usuario, o bien comprobar un diagnóstico específico.

Componentes de este sistema experto:

## 1. Base de Conocimiento
Es el base donde se encuentra el "conocimiento" del experto técnico. Está implementada como una lista de diccionarios, donde cada diccionario representa una **regla heurística**. Cada regla cuenta con:
- `id`: Identificador único de la regla (ej. "R01").
- `descripcion`: Nombre o título de la falla (ej. "Fuente de poder dañada").
- `condiciones`: Lista de síntomas necesarios para que la falla se considere presente.
- `conclusion`: La recomendación técnica o acción a tomar si la regla se cumple.
- `confianza`: Un factor de certeza entre 0 y 1 que indica la fiabilidad de ese diagnóstico.

## 2. Base de Hechos
Representa el estado actual del caso que se está evaluando. Se inicializa como una estructura de conjunto vacío, la cual se va llenando con los síntomas (hechos) que el usuario confirma.

## 3. Motor de Inferencia
Es el componente lógico central que procesa las reglas contra los hechos ingresados. Cuenta con los siguientes subprocesos y estrategias:
- **Equiparación:** Filtra qué reglas de la Base de Conocimiento tienen todas sus condiciones presentes en la Base de Hechos, generando un conjunto de reglas aplicables (Conflict Set).
- **Resolución de Conflictos:** Estrategia para decidir qué regla aplicar cuando múltiples reglas son válidas. En este sistema, se ordenan priorizando la mayor `confianza`, y en caso de empate, se prefiere la regla más específica (la que demanda más `condiciones`).
- **Encadenamiento hacia Adelante (Forward Chaining):** Proceso ejecutado en la función `inferir`, que toma los hechos conocidos y avanza hacia una conclusión/diagnóstico.
- **Encadenamiento hacia Atrás (Backward Chaining):** Proceso ejecutado en la función `backward_chain`, donde el sistema parte de una meta diagnóstica y va hacia atrás, preguntando al usuario solo por las condiciones estrictamente necesarias para confirmar o descartar dicha meta.

## 4. Interfaz de Explicación (Trazabilidad)
Añade transparencia y credibilidad al sistema, respondiendo al "cómo y por qué" de una decisión. Una vez que se entrega un diagnóstico, el sistema muestra la trazabilidad del razonamiento listando los síntomas exactos que dispararon la regla ganadora, y además informa qué otras reglas fueron contempladas pero descartadas por tener menor prioridad.

## 5. Interfaz de Usuario
Permite la interacción entre la persona y el motor lógico a través de la terminal de comandos:
- Contiene un diccionario (`PREGUNTAS`) que mapea cada código de síntoma lógico a una pregunta comprensible en lenguaje natural.
- Provee un menú con dos flujos de trabajo principales:
  1. Responder a un cuestionario general para evaluar múltiples síntomas y obtener el diagnóstico más probable.
  2. Someter a prueba un diagnóstico directo (ej. "R03") para que el sistema valide si es cierto evaluando sólo las preguntas correspondientes.

## Explicación y justificación de los desafíos implementados
1. En el **Nivel 1** se agregaron 5 nuevas reglas a la Base de conocimientos, y a cada una se le agregaron sus respectivos daignósticos y síntomas. Las cinco reglas agregadas fueron:
   - Batería de BIOS agotada.
   - Conflicto de perfiféricos o corto en puerto USB.
   - Falla de conectividad a red.
   - Ficheros de sistema corruptos.
   - Problema de retroalimentación.
2. En el **Nivel 2**, se modificó la función **resolver_conflictos**, dado que anteriormente, nos retornaba el valor máximo en confianza utilizando la función integrada max(), la cual terminamos reemplazando por sorted().
3. En el **Nivel 3**, nos apoyamos de la IA para que nos ayude generando la función que nos permite realizar un encadenamiento hacia atrás, el cuál fue adaptado al sistema ya existente, para luego corroborar su correcto funcionamiento.

## Cuestionario Reflexivo
- **¿Cuál es la diferencia principal entre un sistema experto y un programa de software tradicional?**
  La principal diferencia es que mientras que un sistema tradicional sigue una serie de pasos rígidps y exactos, un sistema experto usa lógica y reglas para deducir respuestas, simulando de esta manera el razonamiento humano.
- **¿Por qué se dice que los sistemas expertos tienen conocimiento separado de su motor de razonamiento? ¿Cuál es la ventaja de esto?**
  Por que se dividen en dos partes: la base de conocimiento que contiene toda la información, y el mecanismo encargado de pensar y deducir. La ventaja de esto es que se puede agregar, quitar o actualiza reglas sin necesidad de reprogramar todo el sistema.
- **¿Qué es la base de hechos y en qué se diferencia de la base de conocimiento?**
  La base de conocimiento es auqel que contiene las reglas generales del experto y que es permanente. Mientras que la base de hechos es la información específica del problema actual que se esta resolviendo.
- **¿Qué significa que un sistema experto pueda "explicar su razonamiento"? ¿Por qué esto es importante en medicina o derecho?**
  Significa que el sistema es capaz de mostrar un paso a paso qué reglas utilizó para llegar a tal conclusión, por lo cual, en áreas profesionales críticas, al no poder confiar ciegamente en una máquina, es necesario ver una justificación lógica para poder tomar desiciones.
- **¿Por qué fracasaron comercialmente los sistemas expertos en los años 90? Menciona al menos 3 razones.**
  Podríamos resumirlo en tres razones principales: el costoso mantenimiento que estos sistemas requerían, lo lento que era la extracción de la información de expertos humanos y la incapacidad de los sistemas de aprender por sí solos.
- **Dada la siguiente regla: SI (fiebre AND tos) OR perdida_olfato ENTONCES sospecha_covid y los hechos: {fiebre=True, tos=False, perdida_olfato=True} — ¿Se activa la regla? ¿Por qué?**
  Sí, si se activa, debido a que después de la confición Y, nos aparece una condición O, la cual nos exige mínimo que se cumpla una condición para que se cumpla, y como se cumple por la perdida de olfato, esto activa la regla.
- **Completa la tabla de verdad para la expresión (A AND NOT B) OR (NOT A AND B) para todos los valores posibles de A y B.**
  <img width="473" height="72" alt="image" src="https://github.com/user-attachments/assets/91262186-374e-4204-9006-78a26b1fd798" />
- **¿Cuál es la diferencia entre encadenamiento hacia adelante y hacia atrás? Da un ejemplo de una situación real donde usarías cada uno.**
  La diferencia es que en el encadenamiento hacia adelante se parte de los datos iniciales para intentar llegar a una conclusión, mientras que en el encadenamiento hacia atrás, se parte de una hipótesis y se buscan los datos para confirmarla.
- **Diseña 3 reglas IF-THEN para un sistema experto que asesore a estudiantes sobre qué lenguaje de programación aprender primero, basándose en su objetivo (desarrollo web, análisis de datos, desarrollo de videojuegos).**
```bash
### Reglas de Recomendación de Lenguajes de Programación

* **R01:** SI `objetivo == "desarrollo web"` ENTONCES `recomendacion = "JavaScript"`
* **R02:** SI `objetivo == "analisis de datos"` ENTONCES `recomendacion = "Python"`
* **R03:** SI `objetivo == "desarrollo de videojuegos"` ENTONCES `recomendacion = "C++"`
```
- **Dibuja la red de inferencia correspondiente a las 3 reglas que diseñaste en la pregunta anterior.**
  ```bash
  [Hecho: objetivo]
       |
       |---(Es "desarrollo web") --------> [Conclusión: Aprender JavaScript]
       |
       |---(Es "analisis de datos") -----> [Conclusión: Aprender Python]
       |
       |---(Es "desarrollo de juegos") --> [Conclusión: Aprender C++]
  ```
- **¿Qué problema de diseño podría surgir si dos reglas tienen exactamente las mismas condiciones pero conclusiones diferentes? ¿Cómo lo resolverías?**
  Ante una situación así, se genera un conflicto de inferencia, digamos que el sistema se confunde, pues no sabe cual de las dos elegir. La primera solución que se podría implementar es agregar un nivel de confianza a cada regla y que se elija la más probable. O también se podría mejorar el conocimiento, preguntandole al experto humano que síntoma adicional o condicion extra podría diferenciar una conclusión de otrs.


### :feather: Autores

Este proyecto fue elaborado a partir de un código base ya existente, el cual fue modificado hasta su estado actual por las siguiente personas:

* **Antonio Canux** - *Único colaborador* - [canuxantonio502](https://github.com/canuxantonio502)
