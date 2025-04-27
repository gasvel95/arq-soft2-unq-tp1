# Arquitectura de software 2 - Trabajo Práctico N1

## Modelo de Dominio (DDD)

- **Entidades **:
  - **Product**: (id, name, description, price, stock, idSeller, category).
  - **User**: (id, name, lastName, email) — representa compradores o vendedores.
  - **Order**: (id, itemList, price, idBuyer, shippingAddress, state).
  - **Category**: (id, name, parentCategory) — clasifica productos.

- **Objetos de Valor**:
  - **Money**: (amount, currency).
  - **Address**: (calle, ciudad, provincia, código postal).
  - **Item**: (idProduct, quantity, unitPrice).

- **Agregados**:
  - Cada agregado tiene una raíz (por ejemplo, `Product`, `Order`).
  - Garantizan consistencia y aplican reglas de negocio (como reducir stock, validar disponibilidad).

## Capa de Servicios (Servicios de Aplicación)

Servicios principales que orquestan casos de uso:

- **ProductService**: Crear, modificar, eliminar y buscar productos.
- **UserService**: Registrar y actualizar usuarios.
- **OrderService**: Procesar ventas, validar stock, calcular precios totales.
- **SellerService**: Crear y gestionar vendedores.

Los servicios trabajan exclusivamente a través de **puertos**, sin conocer detalles de base de datos o infraestructura.

## Puertos y Adaptadores

- **Puertos (Interfaces)**:
  - **Repositorios**: `ProductRepository`, `UserRepository`, `SellerRepository`.


- **Adaptadores (Implementaciones)**:
  - **Base de Datos**: `MongoProductRepository`, `MongoUserRepository`.
  - **Web (REST)**: Controladores que manejan las peticiones HTTP.


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
  - `DELETE /users/{id}` — Eliminar un usuario.

- **Vendedores**:
  - `POST /sellers` — Registrar un nuevo vendedor.
  - `PUT /sellers/{id}` — Actualizar un vendedor.
  - `DELETE /sellers/{id}` — Eliminar un vendedor.

- **Ventas**:
  - `POST /orders` — Procesar la venta de un producto.

---


## Diagramas
![umlArq2](https://github.com/user-attachments/assets/ac346447-5f5b-4e05-912a-091c1479cfce)
