# Arquitectura de software 2 - Trabajo Práctico 1

## Requisitos para su ejecución

- [Python >= 3](https://www.python.org/downloads/)
- Realizar la instalación de los requisitos mediante el siguiente comando en la carptea src:

```
pip install -r requirements.txt

```

- Archivo .env con la url de la BDD Mongo en la vairable MONGO_URI

## Ejecución del API
Ubicarse en la raiz de la carpeta src y ejecutar el siguiente comando
```
fastapi run main.py

```

## Ejecución de los tests
Ubicarse en la raiz de la carpeta src y ejecutar el siguiente comando
```
pytest

```

En caso de ejecutar algun archivo test especifico:
```
pytest order_test.py

```

## Modelo de Dominio (DDD)

- **Entidades **:
  - **Product**: (id, name, description, price, stock, seller_id, category).
  - **User**: (id, first_name, last_name, email) — representa compradores o vendedores.
  - **Order**: (id, product_id, total, buyer_id).
  - **Seller**: (id, company_name, email).


- **Objetos de Valor**:
  - **Price**: (amount, currency).
  - **Category**: (name) — clasifica productos.

- **Agregados**:
  - Cada agregado tiene una raíz (por ejemplo, `Product`, `Order`).
  - Garantizan consistencia y aplican reglas de negocio (como reducir stock, validar disponibilidad).

## Capa de Servicios (Servicios de Aplicación)

Servicios principales que orquestan casos de uso:

- **ProductService**: Crear, modificar, eliminar y buscar productos.
- **UserService**: Crear, modificar, eliminar usuarios.
- **OrderService**: Procesar ventas.
- **SellerService**: Crear, modificar, eliminar vendedores.

Los servicios trabajan exclusivamente a través de **puertos**, sin conocer detalles de base de datos o infraestructura.

## Puertos y Adaptadores

- **Puertos**:
  - **Repositorios**: `ProductRepository`, `UserRepository`, `SellerRepository`, `OrderRepository`.


- **Adaptadores**:
  - **Base de Datos**: `MongoProductRepository`, `MongoUserRepository`,`MongoSellerRepository`,`MongoOrderRepository`.
  - **REST**: Controladores que manejan las peticiones HTTP, ubicado en main (temporalmente).


## Estructura del Componente

Aunque es un **monolito**, se organiza internamente:

1. **Dominio**: Entidades, objetos de valor, agregados, servicios de dominio.
2. **Aplicación**: Servicios que implementan casos de uso.
3. **Puertos**: Interfaces de persistencia y servicios externos.
4. **Adaptadores**: Implementaciones específicas (MongoDB, HTTP, etc.).

## Posibles Endpoints REST

- **Productos**:
  - `GET /products` — Listar o buscar productos.
  - `GET /products/{id}` — Obtener detalles de un producto.
  - `POST /products` — Crear un nuevo producto.
  - `PUT /products/{id}` — Modificar un producto.
  - `DELETE /products/{id}` — Eliminar un producto.

- **Usuarios**:
  - `POST /users` — Registrar un nuevo usuario.
  - `PUT /users/{id}` — Actualizar información de un usuario.
  - `GET /users/{id}` — Obtener información de un usuario.
  - `DELETE /users/{id}` — Elimina un usuario.

- **Vendedores**:
  - `POST /sellers` — Registrar un nuevo vendedor.
  - `PUT /sellers/{id}` — Actualizar un vendedor.
  - `GET /sellers/{id}` — Obtener información de un vendedor.
  - `DELETE /sellers/{id}` — Elimina vendedor.

- **Ventas**:
  - `POST /orders` — Procesar la venta de un producto.
  - `GET /orders/{id}` — Obtener información de la venta de un producto.

---


## Diagramas
![umlArq2](/doc/UML.png)

### Diagramas de secuencia
![buscarProd](/doc/buscarProducto.png)
![crearProd](/doc/crearProducto.png)
![crearUsr](/doc/crearUsuario.png)
![crearSeller](/doc/crearVendedor.png)
![venta](/doc/venta.png)

### Video
[Video corriendo en ambiente local](/doc/VideoMuestra.mp4)

# Entregable 2

## Granularidad

Para mejorar la legibilidad, la mantenibilidad y la resiliencia del sistema, hemos desgranularizado el main en tres módulos independientes:

Users

    Gestiona toda la lógica relacionada con la creación, consulta, actualización y eliminación de usuarios.

    Incluye validaciones específicas de dominio.

Notifications

    Encapsula el envío de notificaciones (email, SMS, push).

    Permite agregar nuevas estrategias de notificación sin afectar la lógica de negocio de otros componentes.

    Gestiona reintentos, colas y circuit breakers para garantizar entrega confiable.

Orders (Products)

    Maneja la lógica de creación y gestión de pedidos, así como el catálogo de productos.

    Incluye cálculos de precios, aplicación de promociones y validaciones de inventario.

    Se integra con servicios externos (métodos de pago, stock) a través de adaptadores específicos.

### Decisiones de la granularidad

**Principio de responsabilidad única (SRP):** cada módulo tiene una única razón para cambiar, minimizando el acoplamiento y simplificando el alcance de pruebas unitarias y de integración.

**Volatilidad del código:** al aislar las áreas con mayor frecuencia de cambio (por ejemplo, políticas de notificación o reglas de negocio de pedidos), reducimos el riesgo de efectos colaterales en otras partes de la aplicación.

**Escalabilidad y rendimiento:** cada componente puede escalar de forma independiente. Por ejemplo, en picos de alta carga de notificaciones, podemos desplegar más instancias del módulo de Notifications sin necesidad de replicar los servicios de Users u Orders.

**Tolerancia a fallos:** un fallo o degradación en un módulo (por ejemplo, caída de un proveedor de notificaciones) no afecta la disponibilidad de los demás. Podemos aplicar patrones como circuit breaker y fallback a nivel de módulo.

**Despliegue continuo:** la granularidad reduce el tamaño de los paquetes de despliegue y disminuye el riesgo de errores al actualizar una funcionalidad concreta, acelerando los ciclos de entrega.