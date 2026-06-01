package repository

import (
	"context"
	"strings"

	"github.com/Chazarov/simple-shop/project/backend/pkg/errors"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/entity"
	"github.com/lib/pq"
)

func (r *userRepository) GetUserVerification(ctx context.Context, userId int) (entity.UserVerification, errors.DomainError) {
	var userVerification entity.UserVerification
	query := `SELECT phone_number, email FROM user_verifications WHERE user_id = $1`
	err := r.db.Get(&userVerification, query, userId)
	if err != nil {
		r.logger.Errorf(ctx, "user verification get - user_id: %d, error: %s", userId, err.Error())

		// Проверяем sql.ErrNoRows
		if err.Error() == "sql: no rows in result set" {
			return userVerification, errors.NewNotFoundError("user verification", userId)
		}

		return userVerification, errors.NewInternalServiceError("failed to get user verification", err)
	}
	return userVerification, nil
}

func (r *userRepository) SetUserVerification(ctx context.Context, userVerification entity.UserVerification, userId int) errors.DomainError {
	query := `UPDATE user_verifications SET phone_number = $1, email = $2 WHERE user_id = $3`
	result, err := r.db.Exec(query, userVerification.PhoneNumber, userVerification.Email, userId)
	if err != nil {
		r.logger.Errorf(ctx, "user verification update - user_id: %v, phone: %v, email: %v, error: %v",
			userId, userVerification.PhoneNumber, userVerification.Email, err.Error())

		// Проверяем нарушение уникальности
		if pqErr, ok := err.(*pq.Error); ok {
			if pqErr.Code == "23505" { // unique_violation
				if strings.Contains(pqErr.Message, "phone_number") {
					return errors.NewUniqueConstraintError("user verification", "phone_number", userVerification.PhoneNumber)
				}
				if strings.Contains(pqErr.Message, "email") {
					return errors.NewUniqueConstraintError("user verification", "email", userVerification.Email)
				}
			}
		}

		return errors.NewInternalServiceError("failed to set user verification", err)
	}

	// Проверяем что верификация была найдена и обновлена
	rowsAffected, err := result.RowsAffected()
	if err != nil {
		r.logger.Errorf(ctx, "user verification update check - user_id: %d, error: %s", userId, err.Error())
		return errors.NewInternalServiceError("failed to check update result", err)
	}

	if rowsAffected == 0 {
		r.logger.Errorf(ctx, "user verification update - user_id: %d, error: user verification not found", userId)
		return errors.NewNotFoundError("user verification", userId)
	}

	return nil
}

func (r *userRepository) CreateUserVerification(ctx context.Context, userVerification entity.UserVerification, userId int) (entity.UserVerification, errors.DomainError) {
	query := `INSERT INTO user_verifications (user_id, phone_number, email) VALUES ($1, $2, $3) RETURNING phone_number, email`
	err := r.db.Get(&userVerification, query, userId, userVerification.PhoneNumber, userVerification.Email)
	if err != nil {
		r.logger.Errorf(ctx, "user verification creation - user_id: %d, phone: %v, email: %v, error: %s",
			userId, userVerification.PhoneNumber, userVerification.Email, err.Error())

		// Проверяем нарушение уникальности
		if pqErr, ok := err.(*pq.Error); ok {
			if pqErr.Code == "23505" { // unique_violation
				if strings.Contains(pqErr.Message, "phone_number") {
					return userVerification, errors.NewUniqueConstraintError("user verification", "phone_number", userVerification.PhoneNumber)
				}
				if strings.Contains(pqErr.Message, "email") {
					return userVerification, errors.NewUniqueConstraintError("user verification", "email", userVerification.Email)
				}
			}
		}

		return userVerification, errors.NewInternalServiceError("failed to create user verification", err)
	}
	return userVerification, nil
}
