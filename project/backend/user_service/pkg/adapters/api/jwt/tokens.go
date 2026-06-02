package jwt

import (
	"strings"

	"github.com/Chazarov/simple-shop/project/backend/pkg/errors"
	"github.com/Chazarov/simple-shop/project/backend/pkg/logger"
	"github.com/gin-gonic/gin"
)

const (
	RefreshTokenCookieName = "refresh_token"
)

func GetTokensFromRequest(c *gin.Context, logger *logger.ContextLogger) (string, string, error) {
	authHeader := c.GetHeader("Authorization")
	headerParts := strings.Split(authHeader, " ")
	if len(headerParts) != 2 {
		logger.Errorf(c.Request.Context(), "invalid access token format")
		return "", "", errors.NewAuthTokenError(errors.InvalidToken)
	}

	accessToken := headerParts[1]

	refreshToken, err := c.Cookie(RefreshTokenCookieName)
	if err != nil {
		logger.Warnf(c.Request.Context(), "can't get refresh token from cookie: %s", err.Error())
	}

	const prefix = "Bearer "
	if !strings.HasPrefix(authHeader, prefix) {
		logger.Errorf(c.Request.Context(), "invalid access token format")
		return "", "", errors.NewAuthTokenError(errors.InvalidToken)
	}

	return accessToken, refreshToken, nil
}

func SetRefreshToken(c *gin.Context, refreshToken string) {
	c.SetCookie("refresh_token", refreshToken, 0, "/", "", false, true)
}

func RemoveRefreshToken(c *gin.Context) {
	c.SetCookie(RefreshTokenCookieName, "", -1, "/", "", false, true)
}
