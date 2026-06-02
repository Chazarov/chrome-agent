package handler

import (
	"net/http"
	"strings"

	"github.com/Chazarov/simple-shop/project/backend/pkg/adapters/api/v1/response"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/entity"
	jwtTokens "github.com/Chazarov/simple-shop/project/backend/user_service/pkg/adapters/api/jwt"
	"github.com/gin-gonic/gin"
)

func (h *Handler) Register(c *gin.Context) {
	ctx := c.Request.Context()
	h.logger.Infof(ctx, "Register request received")

	var input entity.RegisterRequest
	if err := c.ShouldBindJSON(&input); err != nil {
		h.logger.Errorf(ctx, "register invalid_parameters - error: %s", err.Error())
		response.MakeResponse(c, h.logger, false, err.Error(), nil, http.StatusBadRequest)
		return
	}

	tokens, err := h.services.UserService.Register(ctx, input)
	if err != nil {
		response.MakeErrorResponse(c, h.logger, err)
		return
	}

	jwtTokens.SetRefreshToken(c, tokens.RefreshToken)

	response.MakeResponse(c, h.logger, true, "user registered successfully", tokens, http.StatusCreated)
}

func (h *Handler) GetCurrentUser(c *gin.Context) {
	ctx := c.Request.Context()
	h.logger.Infof(ctx, "GetCurrentUser request received")

	userData, err := h.jwtService.GetUserDataFromContext(ctx)
	if err != nil {
		h.logger.Errorf(ctx, "get_current_user - can't get user data from context: %s", err.Error())
		response.MakeErrorResponse(c, h.logger, err)
		return
	}

	// Получаем пользователя по userID из токена
	user, domainErr := h.services.UserService.GetCurrentUser(ctx, userData.DeviceUUID)
	if domainErr != nil {
		response.MakeErrorResponse(c, h.logger, domainErr)
		return
	}

	response.MakeResponse(c, h.logger, true, "user get current user successfully", user, http.StatusOK)
}

func (h *Handler) Login(c *gin.Context) {
	ctx := c.Request.Context()
	h.logger.Infof(ctx, "Login request received")

	var input entity.LoginRequest
	if err := c.ShouldBindJSON(&input); err != nil {
		h.logger.Errorf(ctx, "login invalid_parameters - error: %s", err.Error())
		response.MakeResponse(c, h.logger, false, err.Error(), nil, http.StatusBadRequest)
		return
	}

	tokens, err := h.services.UserService.Login(ctx, input)
	if err != nil {
		response.MakeErrorResponse(c, h.logger, err)
		return
	}

	jwtTokens.SetRefreshToken(c, tokens.RefreshToken)

	response.MakeResponse(c, h.logger, true, "login successful", tokens, http.StatusOK)
}

func (h *Handler) Logout(c *gin.Context) {
	ctx := c.Request.Context()
	h.logger.Infof(ctx, "Logout request received")

	// Получаем access token из Authorization header
	authHeader := c.GetHeader("Authorization")
	if authHeader == "" {
		h.logger.Errorf(ctx, "logout - missing authorization header")
		response.MakeResponse(c, h.logger, false, "missing authorization header", nil, http.StatusUnauthorized)
		return
	}

	if !strings.HasPrefix(authHeader, "Bearer ") {
		h.logger.Errorf(ctx, "logout - invalid authorization header format")
		response.MakeResponse(c, h.logger, false, "invalid authorization header format", nil, http.StatusUnauthorized)
		return
	}

	accessToken := strings.TrimPrefix(authHeader, "Bearer ")

	// Валидируем access token
	claims, err := h.jwtService.ValidateAccessToken(ctx, accessToken)
	if err != nil {
		h.logger.Errorf(ctx, "logout - invalid access token: %s", err.Error())
		response.MakeResponse(c, h.logger, false, "invalid access token", nil, http.StatusUnauthorized)
		return
	}

	// Удаляем устройство по deviceID из токена
	err = h.services.UserService.LogoutByDeviceUUID(ctx, claims.DeviceUUID)
	if err != nil {
		h.logger.Errorf(ctx, "logout service error - error: %s", err.Error())
		response.MakeErrorResponse(c, h.logger, err)
		return
	}

	jwtTokens.RemoveRefreshToken(c)

	response.MakeResponse(c, h.logger, true, "logout successful", nil, http.StatusOK)
}

func (h *Handler) RefreshTokens(c *gin.Context) {
	ctx := c.Request.Context()
	h.logger.Infof(ctx, "RefreshTokens request received")

	_, refreshToken, err := jwtTokens.GetTokensFromRequest(c, h.logger)
	if err != nil {
		h.logger.Errorf(ctx, "refresh_tokens - invalid access token: %s", err.Error())
		response.MakeResponse(c, h.logger, false, "invalid access token", nil, http.StatusUnauthorized)
		return
	}
	if refreshToken == "" {
		h.logger.Errorf(ctx, "refresh_tokens - refresh token not found")
		response.MakeResponse(c, h.logger, false, "refresh token not found", nil, http.StatusUnauthorized)
		return
	}

	claims, err := h.jwtService.ValidateRefreshToken(ctx, refreshToken)
	if err != nil {
		h.logger.Errorf(ctx, "refresh_tokens - invalid refresh token: %s", err.Error())
		response.MakeResponse(c, h.logger, false, "invalid refresh token", nil, http.StatusUnauthorized)
		return
	}

	tokens, err := h.services.UserService.RefreshTokens(ctx, refreshToken, claims.UserUUID, claims.DeviceUUID)
	if err != nil {
		response.MakeErrorResponse(c, h.logger, err)
		return
	}

	jwtTokens.SetRefreshToken(c, tokens.RefreshToken)

	response.MakeResponse(c, h.logger, true, "tokens refreshed successfully", tokens, http.StatusOK)
}

func (h *Handler) DeleteAccount(c *gin.Context) {
	ctx := c.Request.Context()
	h.logger.Infof(ctx, "DeleteAccount request received")

	var input entity.DeleteAccountRequest
	if err := c.ShouldBindJSON(&input); err != nil {
		h.logger.Errorf(ctx, " invalid_parameters - error: %s", err.Error())
		response.MakeResponse(c, h.logger, false, err.Error(), nil, http.StatusBadRequest)
		return
	}

	userData, err := h.jwtService.GetUserDataFromContext(ctx)
	if err != nil {
		h.logger.Errorf(ctx, " can't get user data from context: %s", err.Error())
		response.MakeErrorResponse(c, h.logger, err)
		return
	}

	err = h.services.UserService.DeleteAccount(ctx, userData.UserUUID, input.Password)
	if err != nil {
		response.MakeErrorResponse(c, h.logger, err)
		return
	}

	jwtTokens.RemoveRefreshToken(c)

	response.MakeResponse(c, h.logger, true, "account deleted successfully", nil, http.StatusOK)
}
