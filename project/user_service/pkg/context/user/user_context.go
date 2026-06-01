package user_context

import (
	"context"

	pkgContext "github.com/Chazarov/simple-shop/project/backend/pkg/context"
)

const (
	AccessTokenKey pkgContext.CtxKey = "access_token"
)

func WithAccessToken(ctx context.Context, accessToken string) context.Context {
	ctx = context.WithValue(ctx, AccessTokenKey, accessToken)
	return ctx
}
