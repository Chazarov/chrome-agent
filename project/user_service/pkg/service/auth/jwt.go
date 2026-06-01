package auth

import (
	"context"
	"fmt"
	"time"

	"github.com/Chazarov/simple-shop/project/backend/pkg/errors"
	"github.com/Chazarov/simple-shop/project/backend/pkg/logger"
	user_context "github.com/Chazarov/simple-shop/project/backend/user_service/pkg/context/user"
	"github.com/Chazarov/simple-shop/project/backend/user_service/pkg/entity"
	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
)

type JWTService struct {
	secretKey             []byte
	accessTokenExpiresIn  string
	refreshTokenExpiresIn string
	logger                *logger.ContextLogger
}

func NewJWTService(secretKey string, accessTokenExpiresIn string, refreshTokenExpiresIn string, logger *logger.ContextLogger) *JWTService {
	return &JWTService{
		secretKey:             []byte(secretKey),
		accessTokenExpiresIn:  accessTokenExpiresIn,
		refreshTokenExpiresIn: refreshTokenExpiresIn,
		logger:                logger,
	}
}

func (j *JWTService) GenerateAccessToken(ctx context.Context, userUUID uuid.UUID, deviceID uuid.UUID) (string, errors.DomainError) {

	accessTokenExpiresIn, err := time.ParseDuration(j.accessTokenExpiresIn)
	if err != nil {
		j.logger.Errorf(ctx, "failed to parse access token expires in: %s", err.Error())
		return "", errors.NewInternalServiceError("failed to parse access token expires in", err)
	}

	claims := &entity.JWTClaims{
		UserUUID:   userUUID,
		DeviceUUID: deviceID,
		Type:       "access",
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(accessTokenExpiresIn)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			NotBefore: jwt.NewNumericDate(time.Now()),
			ID:        uuid.New().String(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	res, err := token.SignedString(j.secretKey)
	if err != nil {
		j.logger.Errorf(ctx, "failed to sign access token: %s", err.Error())
		return "", errors.NewInternalServiceError("failed to sign access token", err)
	}

	return res, nil
}

func (j *JWTService) GenerateRefreshToken(ctx context.Context, userUUID uuid.UUID, deviceID uuid.UUID) (string, errors.DomainError) {
	refreshTokenExpiresIn, err := time.ParseDuration(j.refreshTokenExpiresIn)
	if err != nil {
		j.logger.Errorf(ctx, "failed to parse refresh token expires in: %s", err.Error())
		return "", errors.NewInternalServiceError("failed to parse refresh token expires in", err)
	}

	claims := &entity.JWTClaims{
		UserUUID:   userUUID,
		DeviceUUID: deviceID,
		Type:       "refresh",
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(refreshTokenExpiresIn)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			NotBefore: jwt.NewNumericDate(time.Now()),
			ID:        uuid.New().String(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	res, err := token.SignedString(j.secretKey)
	if err != nil {
		j.logger.Errorf(ctx, "failed to sign refresh token: %s", err.Error())
		return "", errors.NewInternalServiceError("failed to sign refresh token", err)
	}

	return res, nil
}

func (j *JWTService) ValidateToken(ctx context.Context, tokenString string) (*entity.JWTClaims, errors.DomainError) {
	token, err := jwt.ParseWithClaims(tokenString, &entity.JWTClaims{}, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			j.logger.Errorf(ctx, "unexpected signing method: %v", token.Header["alg"])
			return nil, errors.NewInternalServiceError("unexpected signing method", fmt.Errorf("unexpected signing method: %v", token.Header["alg"]))
		}
		return j.secretKey, nil
	})

	if err != nil {
		j.logger.Errorf(ctx, "failed to parse token: %s", err.Error())
		return nil, errors.NewAuthTokenError(errors.InvalidToken)
	}

	if claims, ok := token.Claims.(*entity.JWTClaims); ok && token.Valid {
		return claims, nil
	}

	return nil, errors.NewAuthTokenError(errors.InvalidToken)
}

func (j *JWTService) ValidateAccessToken(ctx context.Context, tokenString string) (*entity.JWTClaims, errors.DomainError) {
	claims, err := j.ValidateToken(ctx, tokenString)
	if err != nil {
		return nil, err
	}

	if claims.Type != "access" {
		j.logger.Errorf(ctx, "invalid token type: %s", claims.Type)
		return nil, errors.NewAuthTokenError(errors.InvalidToken)
	}

	return claims, nil
}

func (j *JWTService) ValidateRefreshToken(ctx context.Context, tokenString string) (*entity.JWTClaims, errors.DomainError) {
	claims, err := j.ValidateToken(ctx, tokenString)
	if err != nil {
		return nil, err
	}

	if claims.Type != "refresh" {
		j.logger.Errorf(ctx, "invalid token type: %s", claims.Type)
		return nil, errors.NewAuthTokenError(errors.InvalidToken)
	}

	return claims, nil
}

func (j *JWTService) GetUserUUIDFromContext(ctx context.Context) (uuid.UUID, errors.DomainError) {
	accessToken, ok := ctx.Value(user_context.AccessTokenKey).(string)
	if !ok {
		j.logger.Errorf(ctx, "access token not found in context")
		return uuid.Nil, errors.NewAuthTokenError(errors.TokenNotFound)
	}

	if accessToken == "" {
		j.logger.Errorf(ctx, "access token is empty")
		return uuid.Nil, errors.NewAuthTokenError(errors.TokenNotFound)
	}

	claims, err := j.ValidateAccessToken(ctx, accessToken)
	if err != nil {
		return uuid.Nil, err
	}

	return claims.UserUUID, nil
}

func (j *JWTService) GetUserDataFromContext(ctx context.Context) (*entity.JWTClaims, errors.DomainError) {
	accessToken, ok := ctx.Value(user_context.AccessTokenKey).(string)
	if !ok {
		j.logger.Errorf(ctx, "access token not found in context")
		return nil, errors.NewAuthTokenError(errors.TokenNotFound)
	}

	return j.ValidateAccessToken(ctx, accessToken)

}
