package interfaces

import (
	"context"

	"github.com/Chazarov/simple-shop/project/backend/pkg/errors"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/entity"
	"github.com/google/uuid"
)

type UserService interface {
	Register(ctx context.Context, input entity.RegisterRequest) (entity.TokenResponse, errors.DomainError)
	Login(ctx context.Context, input entity.LoginRequest) (entity.TokenResponse, errors.DomainError)
	Logout(ctx context.Context, deviceUUID uuid.UUID) errors.DomainError
	DeleteAccount(ctx context.Context, userUUID uuid.UUID, password string) errors.DomainError
	LogoutByDeviceUUID(ctx context.Context, deviceUUID uuid.UUID) errors.DomainError
	GetCurrentUser(ctx context.Context, deviceUUID uuid.UUID) (entity.User, errors.DomainError)
	GetUserByUUID(ctx context.Context, userUUID uuid.UUID) (entity.User, errors.DomainError)
	RefreshTokens(ctx context.Context, refreshToken string, userUUID uuid.UUID, deviceUUID uuid.UUID) (entity.TokenResponse, errors.DomainError)
}
