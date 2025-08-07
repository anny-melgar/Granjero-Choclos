# Prueba
# Fase 1: El Granjero de Choclos - Rate Limiter Básico

## Contexto
Don José es un granjero muy justo que vende choclos frescos. Para asegurar que todos sus clientes tengan oportunidad de comprar, ha decidido implementar una política muy estricta: **cada cliente solo puede comprar 1 choclo por minuto**.

Tu tarea es crear un backend que simule este sistema de ventas con un rate limiter.

## Requerimientos Técnicos

### Backend
- Crear un servidor web en el lenguaje de programación que prefieras
- Exponer **una sola ruta**: `POST /comprar-choclo` o `GET /comprar-choclo`
- La ruta debe simular la compra de un choclo
- Conectar a una base de datos de tu elección

### Rate Limiter
- Implementar un sistema que permita **máximo 1 compra por minuto por cliente**
- Si el cliente intenta comprar antes del minuto, debe rechazar la petición
- **OBLIGATORIO**: El rate limiter debe implementarse usando base de datos

### Desafío Principal
- Debes resolver cómo identificar a cada cliente de forma única
- Considera que las pruebas se realizarán desde Postman
- Piensa en las diferentes formas que tiene HTTP para identificar requests

## Respuestas Esperadas

### Compra Exitosa
```json
{
  "mensaje": "¡Choclo comprado exitosamente!",
  "cliente": "juan_perez"
}
```

### Rate Limit Excedido
```json
{
  "error": "Rate limit excedido",
  "mensaje": "Solo puedes comprar 1 choclo por minuto",
  "cliente": "juan_perez"
}
```

## Criterios de Evaluación
- **Funcionalidad**: El rate limiter funciona correctamente
- **Base de datos**: Implementación correcta usando BD
- **Identificación de cliente**: Método elegido para identificar clientes únicos
- **Manejo de errores**: Respuestas apropiadas y códigos HTTP correctos
- **Código limpio**: Estructura y legibilidad del código
- **Testing**: Evidencia de pruebas con Postman

## Entregables
1. Código fuente del backend
2. Archivo README con instrucciones de instalación y ejecución
3. Capturas de pantalla de las pruebas en Postman
4. (Opcional) Script de creación de BD o esquema

## Notas Adicionales
- El backend debe ser simple, no implementar autenticación
- La prueba principal será desde Postman
- Asegúrate de que tu base de datos esté correctamente configurada

---
**Tiempo estimado**: 3-4 horas  
**Dificultad**: Intermedio

# Fase 2: Extensión - Múltiples Choclos

## Contexto
¡Don José ha tenido una excelente cosecha! Ahora puede ser más generoso con sus clientes. Ha decidido cambiar su política de ventas: **cada cliente puede comprar hasta 10 choclos por minuto**.

Tu tarea es **modificar tu backend existente** para adaptarse a este nuevo requerimiento.

## Nuevos Requerimientos

### Rate Limiter Actualizado
- Cada cliente puede hacer **máximo 10 compras por minuto**
- Una vez que el cliente haga 10 compras, debe esperar hasta el próximo minuto
- **IMPORTANTE**: El rate limited debe seguir implementandose en DB

### Funcionalidad Adicional
- La ruta debe indicar cuántas compras le quedan al cliente en el minuto actual
- Debe manejar compras múltiples en una sola petición (opcional)

## Respuestas Esperadas

### Compra Exitosa
```json
{
  "mensaje": "¡Choclo comprado exitosamente!",
  "cliente": "juan_perez",
  "comprasRealizadas": 3,
  "comprasRestantes": 7
}
```

### Rate Limit Excedido
```json
{
  "error": "Rate limit excedido",
  "mens aje": "Ya compraste 10 choclos este minuto",
  "cliente": "juan_perez", 
  "comprasRealizadas": 10
}
```

### Compra Múltiple (Opcional)
Permitir especificar cantidad en la petición:
```json
// Request
{
  "cantidad": 3
}

// Response exitoso
{
  "mensaje": "¡3 choclos comprados exitosamente!",
  "cliente": "juan_perez",
  "comprasRealizadas": 5,
  "comprasRestantes": 5
}

// Response cuando no hay suficiente cuota
{
  "error": "Cantidad excede el límite",
  "mensaje": "Solo puedes comprar 2 choclos más este minuto",
  "cliente": "juan_perez",
  "comprasRealizadas": 8,
  "comprasRestantes": 2
}
```

## Consideraciones de Implementación

### Manejo del Tiempo
- Considera cómo manejar el "último minuto"
- Piensa en la ventana deslizante vs ventana fija

### Adaptabilidad del Código
- ¿Tu código de la Fase 1 es fácil de modificar?
- ¿Necesitas reestructurar tu rate limiter?
- ¿Puedes hacer el límite configurable?

## Criterios de Evaluación
- **Funcionalidad**: El nuevo rate limiter funciona correctamente
- **Base de datos**: Mantiene y mejora el uso de BD
- **Información detallada**: Respuestas informativas sobre el estado actual
- **Compras múltiples**: (Opcional) Manejo de cantidad en una petición

## Entregables
1. Código fuente modificado
2. README actualizado explicando los cambios realizados
3. Capturas de pantalla de las nuevas pruebas en Postman
4. Breve reflexión sobre qué tuviste que cambiar de la Fase 1

## Desafío Adicional (Puntos Extra)
- Hacer el límite configurable (cantidad)
- Implementar diferentes ventanas de tiempo (por minuto, por hora)
- Agregar endpoint para consultar el estado actual sin comprar

---
**Tiempo estimado**: 2-3 horas (partiendo de la Fase 1)  
**Dificultad**: Intermedio-Avanzado