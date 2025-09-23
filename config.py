"""
Enhanced Configuration Management System
Provides centralized configuration with validation, encryption, and environment-specific settings.
"""

import os
from typing import Optional, List, Dict, Any
from pathlib import Path
from pydantic import BaseSettings, validator, Field
from cryptography.fernet import Fernet
import json
import logging

# Set up logger
logger = logging.getLogger(__name__)

class DatabaseSettings(BaseSettings):
    """Database configuration settings"""
    database_url: str = Field(..., env="DATABASE_URL")
    pool_size: int = Field(default=20, env="DB_POOL_SIZE")
    max_overflow: int = Field(default=30, env="DB_MAX_OVERFLOW")
    pool_timeout: int = Field(default=30, env="DB_POOL_TIMEOUT")
    pool_recycle: int = Field(default=3600, env="DB_POOL_RECYCLE")

    @validator('database_url')
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("Database URL is required")
        return v

class RedisSettings(BaseSettings):
    """Redis configuration settings"""
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_max_connections: int = Field(default=20, env="REDIS_MAX_CONNECTIONS")

class DiscordSettings(BaseSettings):
    """Discord bot configuration settings"""
    token: str = Field(..., env="DISCORD_BOT_TOKEN")
    command_prefix: str = Field(default="!", env="COMMAND_PREFIX")
    application_id: Optional[int] = Field(default=None, env="APPLICATION_ID")
    guild_id: Optional[int] = Field(default=None, env="GUILD_ID")
    sync_commands_globally: bool = Field(default=True, env="SYNC_COMMANDS_GLOBALLY")

    @validator('token')
    def validate_token(cls, v):
        if not v:
            raise ValueError("Discord bot token is required")
        return v

class LoggingSettings(BaseSettings):
    """Logging configuration settings"""
    level: str = Field(default="INFO", env="LOG_LEVEL")
    format: str = Field(default="json", env="LOG_FORMAT")
    enable_file_logging: bool = Field(default=True, env="ENABLE_FILE_LOGGING")
    log_file_path: str = Field(default="logs/bot.log", env="LOG_FILE_PATH")
    max_file_size: int = Field(default=10485760, env="MAX_LOG_FILE_SIZE")  # 10MB
    backup_count: int = Field(default=5, env="LOG_BACKUP_COUNT")
    enable_external_logging: bool = Field(default=False, env="ENABLE_EXTERNAL_LOGGING")
    external_logging_url: Optional[str] = Field(default=None, env="EXTERNAL_LOGGING_URL")

class SecuritySettings(BaseSettings):
    """Security configuration settings"""
    encryption_key: str = Field(..., env="ENCRYPTION_KEY")
    enable_rate_limiting: bool = Field(default=True, env="ENABLE_RATE_LIMITING")
    max_commands_per_minute: int = Field(default=30, env="MAX_COMMANDS_PER_MINUTE")
    max_commands_per_hour: int = Field(default=300, env="MAX_COMMANDS_PER_HOUR")
    enable_nsfw_filter: bool = Field(default=True, env="ENABLE_NSFW_FILTER")
    allowed_nsfw_guilds: List[int] = Field(default_factory=list, env="ALLOWED_NSFW_GUILDS")

    @validator('encryption_key')
    def validate_encryption_key(cls, v):
        if not v:
            raise ValueError("Encryption key is required")
        try:
            Fernet(v.encode())
        except Exception:
            raise ValueError("Invalid encryption key format")
        return v

class FeatureSettings(BaseSettings):
    """Feature toggle settings"""
    enable_logging: bool = Field(default=True, env="ENABLE_LOGGING")
    enable_jail_system: bool = Field(default=True, env="ENABLE_JAIL_SYSTEM")
    enable_moderation: bool = Field(default=True, env="ENABLE_MODERATION")
    enable_fun_commands: bool = Field(default=True, env="ENABLE_FUN_COMMANDS")
    enable_gif_commands: bool = Field(default=True, env="ENABLE_GIF_COMMANDS")
    enable_utility_commands: bool = Field(default=True, env="ENABLE_UTILITY_COMMANDS")
    enable_community_commands: bool = Field(default=True, env="ENABLE_COMMUNITY_COMMANDS")

class Settings(BaseSettings):
    """Main configuration settings"""
    # Core settings
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")

    # Component settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    discord: DiscordSettings = Field(default_factory=DiscordSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    features: FeatureSettings = Field(default_factory=FeatureSettings)

    # Additional settings
    bot_name: str = Field(default="Enhanced Discord Bot", env="BOT_NAME")
    bot_description: str = Field(default="A comprehensive Discord bot with advanced features", env="BOT_DESCRIPTION")
    support_server_url: Optional[str] = Field(default=None, env="SUPPORT_SERVER_URL")
    website_url: Optional[str] = Field(default=None, env="WEBSITE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

class ConfigurationManager:
    """Manages configuration with encryption and validation"""

    def __init__(self):
        self.settings = Settings()
        self._fernet = Fernet(self.settings.security.encryption_key.encode())
        self._config_cache: Dict[str, Any] = {}

    def get_encrypted_value(self, key: str, default: Any = None) -> Any:
        """Get a decrypted configuration value"""
        if key in self._config_cache:
            return self._config_cache[key]

        encrypted_value = os.getenv(f"{key}_ENCRYPTED")
        if encrypted_value:
            try:
                decrypted = self._fernet.decrypt(encrypted_value.encode()).decode()
                self._config_cache[key] = decrypted
                return decrypted
            except Exception as e:
                logger.error(f"Failed to decrypt {key}: {e}")
                return default

        return default

    def set_encrypted_value(self, key: str, value: Any) -> None:
        """Set an encrypted configuration value"""
        if value is not None:
            encrypted = self._fernet.encrypt(str(value).encode()).decode()
            os.environ[f"{key}_ENCRYPTED"] = encrypted
            self._config_cache[key] = value

    def validate_configuration(self) -> List[str]:
        """Validate all configuration settings"""
        errors = []

        try:
            # Test database connection
            if not self.settings.database.database_url:
                errors.append("Database URL is required")

            # Test Redis connection
            if not self.settings.redis.redis_url:
                errors.append("Redis URL is required")

            # Validate Discord token format
            if not self.settings.discord.token.startswith(('Bot ', 'Bearer ')):
                errors.append("Discord token should start with 'Bot ' or 'Bearer '")

            # Validate logging configuration
            if self.settings.logging.enable_file_logging:
                log_path = Path(self.settings.logging.log_file_path)
                log_path.parent.mkdir(parents=True, exist_ok=True)

        except Exception as e:
            errors.append(f"Configuration validation error: {e}")

        return errors

    def get_settings_dict(self) -> Dict[str, Any]:
        """Get all settings as a dictionary"""
        return {
            "environment": self.settings.environment,
            "debug": self.settings.debug,
            "database": {
                "database_url": self._mask_sensitive_value(self.settings.database.database_url),
                "pool_size": self.settings.database.pool_size,
                "max_overflow": self.settings.database.max_overflow,
                "pool_timeout": self.settings.database.pool_timeout,
                "pool_recycle": self.settings.database.pool_recycle,
            },
            "redis": {
                "redis_url": self._mask_sensitive_value(self.settings.redis.redis_url),
                "redis_db": self.settings.redis.redis_db,
                "redis_max_connections": self.settings.redis.redis_max_connections,
            },
            "discord": {
                "token": self._mask_sensitive_value(self.settings.discord.token),
                "command_prefix": self.settings.discord.command_prefix,
                "application_id": self.settings.discord.application_id,
                "sync_commands_globally": self.settings.discord.sync_commands_globally,
            },
            "logging": {
                "level": self.settings.logging.level,
                "format": self.settings.logging.format,
                "enable_file_logging": self.settings.logging.enable_file_logging,
                "log_file_path": self.settings.logging.log_file_path,
                "max_file_size": self.settings.logging.max_file_size,
                "backup_count": self.settings.logging.backup_count,
            },
            "security": {
                "encryption_key": self._mask_sensitive_value(self.settings.security.encryption_key),
                "enable_rate_limiting": self.settings.security.enable_rate_limiting,
                "max_commands_per_minute": self.settings.security.max_commands_per_minute,
                "max_commands_per_hour": self.settings.security.max_commands_per_hour,
            },
            "features": {
                "enable_logging": self.settings.features.enable_logging,
                "enable_jail_system": self.settings.features.enable_jail_system,
                "enable_moderation": self.settings.features.enable_moderation,
                "enable_fun_commands": self.settings.features.enable_fun_commands,
                "enable_gif_commands": self.settings.features.enable_gif_commands,
                "enable_utility_commands": self.settings.features.enable_utility_commands,
                "enable_community_commands": self.settings.features.enable_community_commands,
            },
            "bot_info": {
                "bot_name": self.settings.bot_name,
                "bot_description": self.settings.bot_description,
                "support_server_url": self.settings.support_server_url,
                "website_url": self.settings.website_url,
            }
        }

    def _mask_sensitive_value(self, value: str) -> str:
        """Mask sensitive configuration values"""
        if not value or len(value) < 8:
            return "****"

        return f"{value[:4]}****{value[-4:]}"

    def reload_configuration(self) -> None:
        """Reload configuration from environment variables"""
        self.settings = Settings()
        self._config_cache.clear()
        logger.info("Configuration reloaded")

# Global configuration instance
config_manager = ConfigurationManager()

# Validate configuration on import
validation_errors = config_manager.validate_configuration()
if validation_errors:
    logger.error(f"Configuration validation errors: {validation_errors}")
    raise ValueError(f"Configuration validation failed: {validation_errors}")
