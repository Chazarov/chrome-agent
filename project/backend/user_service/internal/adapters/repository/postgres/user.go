package repository

import (
	"context"
	"strings"

	"github.com/Chazarov/simple-shop/project/backend/pkg/errors"
	"github.com/Chazarov/simple-shop/project/backend/pkg/logger"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/entity"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/interfaces"
	"github.com/google/uuid"
	"github.com/jmoiron/sqlx"
	"github.com/lib/pq"
)

type userRepository struct {
	logger *logger.ContextLogger
	db     *sqlx.DB
}

func NewUserRepository(db *sqlx.DB, contextLogger *logger.ContextLogger) interfaces.UserRepository {
	return &userRepository{db: db, logger: contextLogger}
}

func (r *userRepository) CreateUser(ctx context.Context, user entity.User) (entity.User, errors.DomainError) {
	user.UUID = uuid.New()
	query := `INSERT INTO users (username, password_hash, uuid) VALUES ($1, $2, $3) RETURNING *`
	err := r.db.Get(&user, query, user.Username, user.Password, user.UUID)
	if err != nil {
		r.logger.Errorf(ctx, "user creation - username: %s, error: %s", user.Username, err.Error())
		if pqErr, ok := err.(*pq.Error); ok {
			if pqErr.Code == "23505" { // unique_violation
				if strings.Contains(pqErr.Message, "username") {
					return user, errors.NewUniqueConstraintError("user", "username", user.Username)
				}
			}
		}

		return user, errors.NewInternalServiceError("failed to create user", err)
	}

	r.logger.Infof(ctx, "user created successfully - username: %s, id: %d", user.Username, user.ID)
	return user, nil
}

func (r *userRepository) GetUserByDeviceUUID(ctx context.Context, deviceUUID uuid.UUID) (entity.User, errors.DomainError) {
	var user entity.User
	query := `SELECT id, uuid, username, password_hash, created_at FROM users WHERE id = (SELECT user_id FROM devices WHERE uuid = $1)`
	err := r.db.Get(&user, query, deviceUUID)
	if err != nil {
		r.logger.Errorf(ctx, "user get by device - device_uuid: %s, error: %s", deviceUUID, err.Error())

		// Проверяем sql.ErrNoRows
		if err.Error() == "sql: no rows in result set" {
			return user, errors.NewNotFoundError("user", deviceUUID)
		}

		return user, errors.NewInternalServiceError("failed to get user", err)
	}
	return user, nil
}

func (r *userRepository) GetUserByUsername(ctx context.Context, username string) (entity.User, errors.DomainError) {
	var user entity.User
	query := `SELECT id, uuid, username, password_hash, created_at FROM users WHERE username = $1`
	err := r.db.Get(&user, query, username)
	if err != nil {
		r.logger.Errorf(ctx, "user get by username - username: %s, error: %s", username, err.Error())

		// Проверяем sql.ErrNoRows
		if err.Error() == "sql: no rows in result set" {
			return user, errors.NewNotFoundError("user", username)
		}

		return user, errors.NewInternalServiceError("failed to get user", err)
	}

	r.logger.Debugf(ctx, "user found by username - username: %s, id: %d", username, user.ID)
	return user, nil
}

func (r *userRepository) GetUserByUsernameAndPassword(ctx context.Context, username string, password string) (entity.User, errors.DomainError) {
	var user entity.User
	query := `SELECT id, uuid, username, email, password_hash, created_at FROM users WHERE username = $1 AND password_hash = $2`
	err := r.db.Get(&user, query, username, password)
	if err != nil {
		r.logger.Errorf(ctx, "user get by credentials - username: %s, error: %s", username, err.Error())

		// Проверяем sql.ErrNoRows
		if err.Error() == "sql: no rows in result set" {
			return user, errors.NewNotFoundError("user", username)
		}

		return user, errors.NewInternalServiceError("failed to get user", err)
	}

	r.logger.Debugf(ctx, "user authenticated successfully - username: %s, id: %d", username, user.ID)
	return user, nil
}

func (r *userRepository) GetUserByUUID(ctx context.Context, userUUID uuid.UUID) (entity.User, errors.DomainError) {
	var user entity.User
	query := `SELECT id, uuid, username, email, password_hash, created_at FROM users WHERE uuid = $1`
	err := r.db.Get(&user, query, userUUID)
	if err != nil {
		r.logger.Errorf(ctx, "user get by uuid - user_uuid: %s, error: %s", userUUID, err.Error())

		// Проверяем sql.ErrNoRows
		if err.Error() == "sql: no rows in result set" {
			return user, errors.NewNotFoundError("user", userUUID)
		}

		return user, errors.NewInternalServiceError("failed to get user", err)
	}

	r.logger.Debugf(ctx, "user found by uuid - user_uuid: %s, username: %s", userUUID, user.Username)
	return user, nil
}

func (r *userRepository) GetUserByID(ctx context.Context, userID int) (entity.User, errors.DomainError) {
	var user entity.User
	query := `SELECT id, uuid, username, email, password_hash, created_at FROM users WHERE id = $1`
	err := r.db.Get(&user, query, userID)
	if err != nil {
		r.logger.Errorf(ctx, "user get by id - user_id: %d, error: %s", userID, err.Error())
		return user, errors.NewInternalServiceError("failed to get user", err)
	}

	r.logger.Debugf(ctx, "user found by id - user_id: %d, username: %s", userID, user.Username)
	return user, nil
}

func (r *userRepository) DeleteUser(ctx context.Context, userUUID uuid.UUID, password string) errors.DomainError {
	query := `DELETE FROM users WHERE uuid = $1 AND password_hash = $2`
	result, err := r.db.ExecContext(ctx, query, userUUID, password)
	if err != nil {
		r.logger.Errorf(ctx, "user deletion - user_uuid: %s, error: %s", userUUID, err.Error())
		return errors.NewInternalServiceError("failed to delete user", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		r.logger.Errorf(ctx, "user deletion check - user_uuid: %s, error: %s", userUUID, err.Error())
		return errors.NewInternalServiceError("failed to check deletion result", err)
	}

	if rowsAffected == 0 {
		r.logger.Errorf(ctx, "user deletion failed - user_uuid: %s, invalid credentials or user not found", userUUID)
		return errors.NewUnauthorizedError("invalid credentials")
	}

	r.logger.Infof(ctx, "user deleted successfully - user_uuid: %s", userUUID)
	return nil
}
