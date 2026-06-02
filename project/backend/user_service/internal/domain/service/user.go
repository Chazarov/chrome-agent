package service

import (
	"context"
	"crypto/sha256"
	"fmt"

	// "github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/entity"
	"github.com/Chazarov/simple-shop/project/backend/pkg/errors"
	"github.com/Chazarov/simple-shop/project/backend/pkg/logger"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/entity"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/interfaces"
	"github.com/Chazarov/simple-shop/project/backend/user_service/pkg/service/auth"
	"github.com/google/uuid"
)

type UserService struct {
	logger     *logger.ContextLogger
	userRepo   interfaces.UserRepository
	jwtService *auth.JWTService
}

func NewUserService(userRepo interfaces.UserRepository, logger *logger.ContextLogger, jwtService *auth.JWTService) interfaces.UserService {
	return &UserService{
		userRepo:   userRepo,
		logger:     logger,
		jwtService: jwtService,
	}
}

func (s *UserService) Register(ctx context.Context, input entity.RegisterRequest) (entity.TokenResponse, errors.DomainError) {
	hashedPassword := s.hashPassword(input.Password)

	user := entity.User{
		Username: input.Username,
		Password: hashedPassword,
	}
	userVerification := entity.UserVerification{
		Email:       input.Email,
		PhoneNumber: input.Phone,
	}

	user, err := s.userRepo.CreateUser(ctx, user)
	if err != nil {
		return entity.TokenResponse{}, err
	}

	_, err = s.userRepo.CreateUserVerification(ctx, userVerification, user.ID)
	if err != nil {
		return entity.TokenResponse{}, err
	}

	deviceUUID := uuid.New()
	device := entity.Device{
		UserID:     user.ID,
		UUID:       deviceUUID,
		DeviceName: input.DeviceName,
	}

	device, err = s.userRepo.CreateDevice(ctx, device)
	if err != nil {
		return entity.TokenResponse{}, err
	}

	// Генерируем токены
	accessToken, jwtErr := s.jwtService.GenerateAccessToken(ctx, user.UUID, device.UUID)
	if jwtErr != nil {
		return entity.TokenResponse{}, errors.NewInternalServiceError("failed to generate access token", jwtErr)
	}

	refreshToken, jwtErr := s.jwtService.GenerateRefreshToken(ctx, user.UUID, device.UUID)
	if jwtErr != nil {
		return entity.TokenResponse{}, errors.NewInternalServiceError("failed to generate refresh token", jwtErr)
	}

	// Сохраняем refresh token в базе данных
	err = s.userRepo.UpdateDeviceRefreshToken(ctx, deviceUUID, refreshToken)
	if err != nil {
		return entity.TokenResponse{}, err
	}

	return entity.TokenResponse{
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
	}, nil
}

func (s *UserService) Login(ctx context.Context, input entity.LoginRequest) (entity.TokenResponse, errors.DomainError) {
	user, err := s.userRepo.GetUserByUsername(ctx, input.Username)
	if err != nil {
		return entity.TokenResponse{}, err
	}

	if !s.checkPassword(input.Password, user.Password) {
		s.logger.Errorf(ctx, "login invalid credentials - username: %s", input.Username)
		return entity.TokenResponse{}, errors.NewUnauthorizedError("invalid credentials")
	}

	deviceUUID := uuid.New()
	device := entity.Device{
		UserID:     user.ID,
		UUID:       deviceUUID,
		DeviceName: input.DeviceName,
	}

	device, err = s.userRepo.CreateDevice(ctx, device)
	if err != nil {
		return entity.TokenResponse{}, errors.NewInternalServiceError("failed to create device", err)
	}

	// Генерируем токены
	accessToken, jwtErr := s.jwtService.GenerateAccessToken(ctx, user.UUID, device.UUID)
	if jwtErr != nil {
		return entity.TokenResponse{}, errors.NewInternalServiceError("failed to generate access token", jwtErr)
	}

	refreshToken, jwtErr := s.jwtService.GenerateRefreshToken(ctx, user.UUID, device.UUID)
	if jwtErr != nil {
		return entity.TokenResponse{}, errors.NewInternalServiceError("failed to generate refresh token", jwtErr)
	}

	// Сохраняем refresh token в базе данных
	err = s.userRepo.UpdateDeviceRefreshToken(ctx, deviceUUID, refreshToken)
	if err != nil {
		return entity.TokenResponse{}, err
	}

	return entity.TokenResponse{
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
	}, nil
}

func (s *UserService) Logout(ctx context.Context, deviceUUID uuid.UUID) errors.DomainError {
	err := s.userRepo.DeleteDevice(ctx, deviceUUID)
	return err
}

func (s *UserService) GetCurrentUser(ctx context.Context, deviceUUID uuid.UUID) (entity.User, errors.DomainError) {
	user, err := s.userRepo.GetUserByDeviceUUID(ctx, deviceUUID)
	s.userRepo.UpdateDeviceLastUsed(ctx, deviceUUID)
	if err != nil {
		return entity.User{}, err
	}
	return user, nil
}

func (s *UserService) GetUserByUUID(ctx context.Context, userUUID uuid.UUID) (entity.User, errors.DomainError) {
	user, err := s.userRepo.GetUserByUUID(ctx, userUUID)
	if err != nil {
		return entity.User{}, err
	}
	return user, nil
}

func (s *UserService) LogoutByDeviceUUID(ctx context.Context, deviceUUID uuid.UUID) errors.DomainError {
	err := s.userRepo.DeleteDevice(ctx, deviceUUID)
	return err
}

func (s *UserService) RefreshTokens(ctx context.Context, refreshToken string, userUUID uuid.UUID, deviceUUID uuid.UUID) (entity.TokenResponse, errors.DomainError) {
	// Валидируем refresh token
	claims, err := s.jwtService.ValidateRefreshToken(ctx, refreshToken)
	if err != nil {
		s.logger.Errorf(ctx, "invalid refresh token - error: %s", err.Error())
		return entity.TokenResponse{}, errors.NewUnauthorizedError("invalid refresh token")
	}

	// Получаем устройство по refresh token
	device, domainErr := s.userRepo.GetDeviceByRefreshToken(ctx, refreshToken)
	if domainErr != nil {
		return entity.TokenResponse{}, domainErr
	}

	// Проверяем, что device ID из токена совпадает с device ID из базы
	if device.UUID != claims.DeviceUUID {
		s.logger.Errorf(ctx, "device ID mismatch - token: %d, database: %d", claims.DeviceUUID, device.ID)
		return entity.TokenResponse{}, errors.NewUnauthorizedError("invalid refresh token")
	}

	// Генерируем новые токены
	newAccessToken, jwtErr := s.jwtService.GenerateAccessToken(ctx, claims.UserUUID, claims.DeviceUUID)
	if jwtErr != nil {
		return entity.TokenResponse{}, errors.NewInternalServiceError("failed to generate access token", jwtErr)
	}

	newRefreshToken, jwtErr := s.jwtService.GenerateRefreshToken(ctx, claims.UserUUID, claims.DeviceUUID)
	if jwtErr != nil {
		return entity.TokenResponse{}, errors.NewInternalServiceError("failed to generate refresh token", jwtErr)
	}

	// Обновляем refresh token в базе данных
	domainErr = s.userRepo.UpdateDeviceRefreshToken(ctx, device.UUID, newRefreshToken)
	if domainErr != nil {
		return entity.TokenResponse{}, domainErr
	}

	return entity.TokenResponse{
		AccessToken:  newAccessToken,
		RefreshToken: newRefreshToken,
	}, nil
}

func (s *UserService) hashPassword(password string) string {
	hash := sha256.Sum256([]byte(password))
	return fmt.Sprintf("%x", hash)
}

func (s *UserService) checkPassword(password, hash string) bool {
	return s.hashPassword(password) == hash
}

func (s *UserService) DeleteAccount(ctx context.Context, userUUID uuid.UUID, password string) errors.DomainError {
	hashedPassword := s.hashPassword(password)
	return s.userRepo.DeleteUser(ctx, userUUID, hashedPassword)
}
