package repository

import (
	"context"
	"strings"

	"github.com/Chazarov/simple-shop/project/backend/pkg/errors"
	"github.com/Chazarov/simple-shop/project/backend/user_service/internal/domain/entity"
	"github.com/google/uuid"
	"github.com/lib/pq"
)

func (r *userRepository) CreateDevice(ctx context.Context, device entity.Device) (entity.Device, errors.DomainError) {
	query := `INSERT INTO devices (user_id, device_name, uuid) VALUES ($1, $2, $3) RETURNING *`
	err := r.db.Get(&device, query, device.UserID, device.DeviceName, device.UUID)
	if err != nil {
		r.logger.Errorf(ctx, "device creation - user_id: %d, device_name: %s, uuid: %s, error: %s",
			device.UserID, device.DeviceName, device.UUID, err.Error())

		// Проверяем нарушение уникальности
		if pqErr, ok := err.(*pq.Error); ok {
			if pqErr.Code == "23505" { // unique_violation
				if strings.Contains(pqErr.Message, "uuid") {
					return device, errors.NewUniqueConstraintError("device", "uuid", device.UUID)
				}
			}
		}

		return device, errors.NewInternalServiceError("failed to create device", err)
	}
	return device, nil
}

func (r *userRepository) GetDevice(ctx context.Context, deviceUUID uuid.UUID) (entity.Device, errors.DomainError) {
	var device entity.Device
	query := `SELECT id, user_id, uuid, device_name, refresh_token, created_at, last_used FROM devices WHERE uuid = $1`
	err := r.db.Get(&device, query, deviceUUID)
	if err != nil {
		r.logger.Errorf(ctx, "device get - uuid: %s, error: %s", deviceUUID, err.Error())

		// Проверяем sql.ErrNoRows
		if err.Error() == "sql: no rows in result set" {
			return device, errors.NewNotFoundError("device", deviceUUID)
		}

		return device, errors.NewInternalServiceError("failed to get device", err)
	}
	return device, nil
}

func (r *userRepository) DeleteDevice(ctx context.Context, deviceUUID uuid.UUID) errors.DomainError {
	query := `DELETE FROM devices WHERE uuid = $1`
	result, err := r.db.Exec(query, deviceUUID)
	if err != nil {
		r.logger.Errorf(ctx, "device delete - uuid: %s, error: %s", deviceUUID, err.Error())
		return errors.NewInternalServiceError("failed to delete device", err)
	}

	// Проверяем что устройство было найдено и удалено
	rowsAffected, err := result.RowsAffected()
	if err != nil {
		r.logger.Errorf(ctx, "device delete check - uuid: %s, error: %s", deviceUUID, err.Error())
		return errors.NewInternalServiceError("failed to check delete result", err)
	}

	if rowsAffected == 0 {
		r.logger.Errorf(ctx, "device delete - uuid: %s, error: device not found", deviceUUID)
		return errors.NewNotFoundError("device", deviceUUID)
	}

	return nil
}

func (r *userRepository) DeleteDeviceByUUID(ctx context.Context, deviceUUID uuid.UUID) errors.DomainError {
	query := `DELETE FROM devices WHERE uuid = $1`
	result, err := r.db.Exec(query, deviceUUID)
	if err != nil {
		r.logger.Errorf(ctx, "device delete by uuid - uuid: %s, error: %s", deviceUUID, err.Error())
		return errors.NewInternalServiceError("failed to delete device by uuid", err)
	}

	// Проверяем что устройство было найдено и удалено
	rowsAffected, err := result.RowsAffected()
	if err != nil {
		r.logger.Errorf(ctx, "device delete by uuid check - uuid: %s, error: %s", deviceUUID, err.Error())
		return errors.NewInternalServiceError("failed to check delete result", err)
	}

	if rowsAffected == 0 {
		r.logger.Errorf(ctx, "device delete by uuid - uuid: %s, error: device not found", deviceUUID)
		return errors.NewNotFoundError("device", deviceUUID)
	}

	return nil
}

func (r *userRepository) UpdateDeviceLastUsed(ctx context.Context, deviceUUID uuid.UUID) errors.DomainError {
	query := `UPDATE devices SET last_used = NOW() WHERE uuid = $1`
	result, err := r.db.Exec(query, deviceUUID)
	if err != nil {
		r.logger.Errorf(ctx, "device update last_used - uuid: %s, error: %s", deviceUUID, err.Error())
		return errors.NewInternalServiceError("failed to update device last used", err)
	}

	// Проверяем что устройство было найдено и обновлено
	rowsAffected, err := result.RowsAffected()
	if err != nil {
		r.logger.Errorf(ctx, "device update check - uuid: %s, error: %s", deviceUUID, err.Error())
		return errors.NewInternalServiceError("failed to check update result", err)
	}

	if rowsAffected == 0 {
		r.logger.Errorf(ctx, "device update - uuid: %s, error: device not found", deviceUUID)
		return errors.NewNotFoundError("device", deviceUUID)
	}

	return nil
}

func (r *userRepository) GetDeviceByUserUUID(ctx context.Context, userUUID uuid.UUID, deviceName string) (entity.Device, errors.DomainError) {
	var device entity.Device
	query := `SELECT id, user_id, uuid, device_name, refresh_token, created_at, last_used FROM devices WHERE user_id = $1 AND device_name = $2`
	err := r.db.Get(&device, query, userUUID.String(), deviceName)
	if err != nil {
		r.logger.Errorf(ctx, "device get by user - user_uuid: %s, device_name: %s, error: %s",
			userUUID, deviceName, err.Error())

		// Проверяем sql.ErrNoRows
		if err.Error() == "sql: no rows in result set" {
			return device, errors.NewNotFoundError("device", map[string]interface{}{
				"user_id":     userUUID,
				"device_name": deviceName,
				"user_uuid":   userUUID,
			})
		}

		return device, errors.NewInternalServiceError("failed to get device", err)
	}
	return device, nil
}

func (r *userRepository) UpdateDeviceRefreshToken(ctx context.Context, deviceUUID uuid.UUID, refreshToken string) errors.DomainError {
	query := `UPDATE devices SET refresh_token = $1 WHERE uuid = $2`
	result, err := r.db.Exec(query, refreshToken, deviceUUID)
	if err != nil {
		r.logger.Errorf(ctx, "device update refresh_token - uuid: %s, error: %s", deviceUUID, err.Error())
		return errors.NewInternalServiceError("failed to update device refresh token", err)
	}

	// Проверяем что устройство было найдено и обновлено
	rowsAffected, err := result.RowsAffected()
	if err != nil {
		r.logger.Errorf(ctx, "device update refresh_token check - uuid: %s, error: %s", deviceUUID, err.Error())
		return errors.NewInternalServiceError("failed to check update result", err)
	}

	if rowsAffected == 0 {
		r.logger.Errorf(ctx, "device update refresh_token - uuid: %s, error: device not found", deviceUUID)
		return errors.NewNotFoundError("device", deviceUUID)
	}

	return nil
}

func (r *userRepository) GetDeviceByRefreshToken(ctx context.Context, refreshToken string) (entity.Device, errors.DomainError) {
	var device entity.Device
	query := `SELECT id, user_id, uuid, device_name, refresh_token, created_at, last_used FROM devices WHERE refresh_token = $1`
	err := r.db.Get(&device, query, refreshToken)
	if err != nil {
		r.logger.Errorf(ctx, "device get by refresh_token - error: %s", err.Error())

		// Проверяем sql.ErrNoRows
		if err.Error() == "sql: no rows in result set" {
			return device, errors.NewNotFoundError("device", "refresh_token")
		}

		return device, errors.NewInternalServiceError("failed to get device by refresh token", err)
	}
	return device, nil
}
