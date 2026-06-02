package entity

import (
	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
)

type JWTClaims struct {
	UserUUID   uuid.UUID `json:"user_uuid"`
	DeviceUUID uuid.UUID `json:"device_uuid"`
	Type       string    `json:"type"` // "access" or "refresh"
	jwt.RegisteredClaims
}
