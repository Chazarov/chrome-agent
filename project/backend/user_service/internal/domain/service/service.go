package service

import "github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/interfaces"

type Service struct {
	UserService interfaces.UserService
}

func NewService(userService interfaces.UserService) *Service {
	return &Service{UserService: userService}
}
