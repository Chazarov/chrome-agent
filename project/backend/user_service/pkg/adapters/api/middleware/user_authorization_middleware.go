package middleware

import (
	"github.com/Chazarov/simple-shop/project/backend/pkg/adapters/api/v1/response"
	"github.com/Chazarov/simple-shop/project/backend/pkg/errors"
	"github.com/Chazarov/simple-shop/project/backend/pkg/logger"
	"github.com/Chazarov/simple-shop/project/backend/user_service/pkg/adapters/api/jwt"
	userContext "github.com/Chazarov/simple-shop/project/backend/user_service/pkg/context/user"
	"github.com/gin-gonic/gin"
)

type UserAuthorizationMiddleware struct {
	logger *logger.ContextLogger
}

func NewUserAuthorizationMiddleware(logger *logger.ContextLogger) *UserAuthorizationMiddleware {
	return &UserAuthorizationMiddleware{logger: logger}
}

// UserAuthorizationMiddleware добавляет access token в контекст
func (m UserAuthorizationMiddleware) AddAccessTokenToContext() gin.HandlerFunc {
	return func(c *gin.Context) {
		accessToken, _, err := jwt.GetTokensFromRequest(c, m.logger)
		if err != nil {
			accessToken = ""
			if errors.IsAutnTokenError(err) {
				m.logger.Errorf(c.Request.Context(), " Token invalid or not found error: %v", err)
				response.MakeErrorResponse(c, m.logger, err)
				c.Abort()
			} else {
				m.logger.Errorf(c.Request.Context(), " Can't get access token from request error: %v", err)
				response.MakeErrorResponse(c, m.logger, err)
				c.Abort()
			}

		}

		c.Request = c.Request.WithContext(userContext.WithAccessToken(c.Request.Context(), accessToken))
		c.Next()
	}
}
