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
![umlArq2](https://github.com/user-attachments/assets/ac346447-5f5b-4e05-912a-091c1479cfce)

### Diagramas de secuencia
![buscarProd](/doc/buscarProducto.png)
![crearProd](/doc/crearProducto.png)
![crearUsr](/doc/crearUsuario.png)
![crearSeller](/doc/crearVendedor.png)
![venta](/doc/venta.png)

### Video
[Video corriendo en ambiente local](/doc/VideoMuestra.mp4)
