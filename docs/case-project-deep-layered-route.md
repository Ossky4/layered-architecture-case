# Case Project PR1: ruta multicapa con dependencias profundas (documental)

## Propósito del caso
Delimitar una hipótesis de trabajo para un cleanup pequeño y conservador en una ruta interna con varias capas (`api` → `services`/`dependency` → `factories` → `dao`/`uow`), sin implementar cambios técnicos todavía.

## Hipótesis del experimento
Codex puede mantener criterio conservador en una ruta multicapa con dependencias más profundas, evaluando 2–3 alternativas pequeñas y competitivas, sin perder disciplina de PR pequeña ni claridad de validación.

## Capas o módulos bajo observación
- `src/layered_architecture/api/routers/v1/orders.py`
- `src/layered_architecture/services/dependency.py`
- `src/layered_architecture/factories/order.py`
- Dependencias que aparecen en la construcción de servicios: `dao/*`, `db/uow/*`, `services/concrete/*`

## Ruta interna bajo observación
Ruta de trabajo a observar (como hipótesis, no como defecto demostrado):
1. `orders` router recibe request y selecciona resolución de servicio.
2. `DependencyService` delega en `OrderServiceFactory`.
3. `OrderServiceFactory` instancia dependencias de persistencia y resuelve implementación concreta de `OrderServiceInterface`.
4. Servicio concreto ejecuta la operación usando DAOs y UoW.

## Alternativas plausibles de cleanup pequeño (competitivas)
1. **Ajuste mínimo del punto de resolución en router/dependency**  
   Reducir fricción en cómo se solicita el servicio (sin cambiar contratos externos ni comportamiento).
2. **Ajuste mínimo de construcción en factory**  
   Hacer más explícita o uniforme la creación de dependencias en `OrderServiceFactory` para mejorar legibilidad local.
3. **Ajuste mínimo de borde entre dependency y factory**  
   Simplificar la frontera entre ambos módulos para disminuir ambigüedad de responsabilidades, manteniendo la misma arquitectura general.

## Criterio para elegir entre alternativas
Se priorizará la alternativa que:
- permita una **PR técnica de una sola intención**,
- tenga **menor superficie de cambio**,
- conserve comportamiento observable,
- y permita validación simple con tests existentes o checks acotados.

## Fuera de alcance
- Rediseño arquitectónico amplio.
- Cambios transversales en múltiples rutas o dominios.
- Reorganización grande de paquetes/módulos.
- Ajustes de setup, tooling o estrategia de testing.

## Secuencia prevista de PRs
- **PR1 (esta):** delimitación documental del caso e hipótesis.
- **PR2 (técnica, pequeña):** ejecutar una sola alternativa de cleanup en la ruta observada.
- **PR3 (opcional):** ajuste menor adicional solo si queda evidencia concreta y acotada tras PR2.
