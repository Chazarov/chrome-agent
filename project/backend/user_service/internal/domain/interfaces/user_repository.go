package interfaces

import (
	"context"

	"github.com/Chazarov/simple-shop/project/backend/pkg/errors"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/entity"
	"github.com/google/uuid"
)

type UserRepository interface {
	CreateUser(ctx context.Context, user entity.User) (entity.User, errors.DomainError)
	DeleteUser(ctx context.Context, userUUID uuid.UUID, password string) errors.DomainError
	GetUserByUUID(ctx context.Context, userUUID uuid.UUID) (entity.User, errors.DomainError)
	GetUserByID(ctx context.Context, userID int) (entity.User, errors.DomainError)
	GetUserByUsername(ctx context.Context, username string) (entity.User, errors.DomainError)
	GetUserByDeviceUUID(ctx context.Context, deviceUUID uuid.UUID) (entity.User, errors.DomainError)
	GetUserByUsernameAndPassword(ctx context.Context, username string, password string) (entity.User, errors.DomainError)

	CreateUserVerification(ctx context.Context, userVerification entity.UserVerification, userId int) (entity.UserVerification, errors.DomainError)
	GetUserVerification(ctx context.Context, userId int) (entity.UserVerification, errors.DomainError)
	SetUserVerification(ctx context.Context, userVerification entity.UserVerification, userId int) errors.DomainError

	CreateDevice(ctx context.Context, device entity.Device) (entity.Device, errors.DomainError)
	GetDevice(ctx context.Context, deviceUUID uuid.UUID) (entity.Device, errors.DomainError)
	GetDeviceByUserUUID(ctx context.Context, userUUID uuid.UUID, deviceName string) (entity.Device, errors.DomainError)
	DeleteDevice(ctx context.Context, deviceUUID uuid.UUID) errors.DomainError
	DeleteDeviceByUUID(ctx context.Context, deviceUUID uuid.UUID) errors.DomainError
	UpdateDeviceLastUsed(ctx context.Context, deviceUUID uuid.UUID) errors.DomainError
	UpdateDeviceRefreshToken(ctx context.Context, deviceUUID uuid.UUID, refreshToken string) errors.DomainError
	GetDeviceByRefreshToken(ctx context.Context, refreshToken string) (entity.Device, errors.DomainError)
}
