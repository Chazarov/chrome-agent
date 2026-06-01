# User Service API

**Base URL:** `https://api.shop.develop.zaharow.ru/user`

---

## Auth

### POST /auth/register

> Публичный метод, авторизация не требуется.

**Описание:** Регистрация нового пользователя в системе. Возвращает пару токенов (access + refresh), refresh-token автоматически устанавливается в cookie.

**Request Body:**
| Поле | Тип | Обязательное | Описание |
|---|---|---|---|
| `username` | string | да | Имя пользователя |
| `password` | string | да | Пароль |
| `device_name` | string | да | Название устройства |
| `email` | string | нет | Email |
| `phone` | string | нет | Номер телефона |

```json
{
  "username": "john_doe",
  "password": "secret123",
  "device_name": "iPhone 15",
  "email": "john@example.com",
  "phone": "+79001234567"
}
```

**Response 201:**
```json
{
  "success": true,
  "message": "user registered successfully",
  "data": {
    "access_token": "eyJhbGci...",
    "refresh_token": "eyJhbGci..."
  }
}
```

---

### POST /auth/login

> Публичный метод, авторизация не требуется.

**Описание:** Авторизация существующего пользователя. Возвращает пару токенов, refresh-token устанавливается в cookie.

**Request Body:**
| Поле | Тип | Обязательное | Описание |
|---|---|---|---|
| `username` | string | да | Имя пользователя |
| `password` | string | да | Пароль |
| `device_name` | string | нет | Название устройства |
| `email` | string | нет | Email |
| `phone` | string | нет | Номер телефона |

```json
{
  "username": "john_doe",
  "password": "secret123",
  "device_name": "iPhone 15"
}
```

**Response 200:**
```json
{
  "success": true,
  "message": "login successful",
  "data": {
    "access_token": "eyJhbGci...",
    "refresh_token": "eyJhbGci..."
  }
}
```

---

## User

> Все методы этой группы требуют заголовок `Authorization: Bearer <access_token>`.

### GET /user/me

**Описание:** Возвращает данные текущего авторизованного пользователя. Пользователь определяется по device UUID из JWT-токена.

**Headers:**
| Заголовок | Значение |
|---|---|
| `Authorization` | `Bearer <access_token>` |

**Response 200:**
```json
{
  "success": true,
  "message": "user get current user successfully",
  "data": {
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "username": "john_doe",
    "created": "2024-01-01T00:00:00Z",
    "verifications": {
      "id": 1,
      "phone_number": "+79001234567",
      "email": "john@example.com"
    }
  }
}
```

---

### POST /user/logout

**Описание:** Выход из системы — удаляет сессию текущего устройства и refresh-token из cookie. Устройство определяется по device UUID из JWT-токена.

**Headers:**
| Заголовок | Значение |
|---|---|
| `Authorization` | `Bearer <access_token>` |

**Response 200:**
```json
{
  "success": true,
  "message": "logout successful",
  "data": null
}
```

---

### POST /user/refresh

**Описание:** Обновляет пару токенов по refresh-token из cookie. Новый refresh-token устанавливается в cookie.

**Headers:**
| Заголовок | Значение |
|---|---|
| `Authorization` | `Bearer <access_token>` |

**Cookie:**
| Cookie | Описание |
|---|---|
| `refresh_token` | Действующий refresh-token |

**Response 200:**
```json
{
  "success": true,
  "message": "tokens refreshed successfully",
  "data": {
    "access_token": "eyJhbGci...",
    "refresh_token": "eyJhbGci..."
  }
}
```

---

### DELETE /user/me

**Описание:** Полное удаление аккаунта пользователя. Требует подтверждения текущим паролем.

**Headers:**
| Заголовок | Значение |
|---|---|
| `Authorization` | `Bearer <access_token>` |

**Request Body:**
| Поле | Тип | Обязательное | Описание |
|---|---|---|---|
| `password` | string | да | Текущий пароль для подтверждения |

```json
{
  "password": "secret123"
}
```

**Response 200:**
```json
{
  "success": true,
  "message": "account deleted successfully",
  "data": null
}
```

---

## System

### GET /health

> Публичный метод.

**Описание:** Проверка доступности сервиса. Используется для мониторинга и health check в оркестраторе.

**Response 200:**
```json
{
  "status": "ok"
}
```
