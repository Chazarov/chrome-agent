package entity

import (
	"time"

	"github.com/google/uuid"
)

type User struct {
	ID            int              `json:"-" db:"id"`
	UUID          uuid.UUID        `json:"uuid" db:"uuid"`
	Username      string           `json:"username" db:"username"`
	Password      string           `json:"-" db:"password_hash"`
	Created       time.Time        `json:"created" db:"created_at"`
	Verifications UserVerification `json:"verifications" db:"verifications"`
}

type UserVerification struct {
	ID          int     `json:"id" db:"id"`
	PhoneNumber *string `json:"phone_number" db:"phone_number"`
	Email       *string `json:"email" db:"email"`
}

type Device struct {
	ID           int       `json:"id" db:"id"`
	UserID       int       `json:"user_id" db:"user_id"`
	UUID         uuid.UUID `json:"uuid" db:"uuid"`
	DeviceName   string    `json:"device_name" db:"device_name"`
	RefreshToken *string   `json:"-" db:"refresh_token"`
	Created      time.Time `json:"created" db:"created_at"`
	LastUsed     time.Time `json:"last_used" db:"last_used"`
}

type TokenResponse struct {
	AccessToken  string `json:"access_token"`
	RefreshToken string `json:"refresh_token"`
}

type RefreshTokenRequest struct {
	RefreshToken string `json:"refresh_token" binding:"required"`
}

type LoginRequest struct {
	Username   string  `json:"username" binding:"required"`
	Password   string  `json:"password" binding:"required"`
	DeviceName string  `json:"device_name"`
	Email      *string `json:"email"`
	Phone      *string `json:"phone"`
}

type RegisterRequest struct {
	Username   string  `json:"username" binding:"required"`
	Password   string  `json:"password" binding:"required"`
	DeviceName string  `json:"device_name" binding:"required"`
	Email      *string `json:"email"`
	Phone      *string `json:"phone"`
}

type DeleteAccountRequest struct {
	Password string `json:"password" binding:"required"`
}
