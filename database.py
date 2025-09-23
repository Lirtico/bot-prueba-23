"""
Enhanced Database System
Provides persistent storage with SQLAlchemy ORM, migrations, and connection pooling.
"""

import asyncio
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, BigInteger, ForeignKey, Index, event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging
import json
from config import config_manager

# Set up logger
logger = logging.getLogger(__name__)

# Base class for all models
Base = declarative_base()

class Guild(Base):
    """Guild/Server model"""
    __tablename__ = "guilds"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(String(100), nullable=False)
    owner_id = Column(BigInteger, nullable=False)
    member_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    channels = relationship("Channel", back_populates="guild", cascade="all, delete-orphan")
    roles = relationship("Role", back_populates="guild", cascade="all, delete-orphan")
    members = relationship("GuildMember", back_populates="guild", cascade="all, delete-orphan")
    log_configs = relationship("LogConfig", back_populates="guild", cascade="all, delete-orphan")
    jail_configs = relationship("JailConfig", back_populates="guild", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('ix_guilds_name', 'name'),
        Index('ix_guilds_owner_id', 'owner_id'),
    )

class Channel(Base):
    """Channel model"""
    __tablename__ = "channels"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # text, voice, category
    category_id = Column(BigInteger, nullable=True)
    position = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    guild = relationship("Guild", back_populates="channels")
    log_entries = relationship("LogEntry", back_populates="channel", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('ix_channels_guild_id', 'guild_id'),
        Index('ix_channels_type', 'type'),
    )

class Role(Base):
    """Role model"""
    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    name = Column(String(100), nullable=False)
    color = Column(Integer, default=0)
    permissions = Column(BigInteger, default=0)
    position = Column(Integer, default=0)
    mentionable = Column(Boolean, default=False)
    hoist = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    guild = relationship("Guild", back_populates="roles")
    members = relationship("GuildMember", back_populates="role", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('ix_roles_guild_id', 'guild_id'),
        Index('ix_roles_position', 'position'),
    )

class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String(100), nullable=False)
    discriminator = Column(String(10), nullable=False)
    display_name = Column(String(100), nullable=True)
    avatar_hash = Column(String(100), nullable=True)
    banner_hash = Column(String(100), nullable=True)
    bot = Column(Boolean, default=False)
    system = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    guild_memberships = relationship("GuildMember", back_populates="user", cascade="all, delete-orphan")
    log_entries = relationship("LogEntry", back_populates="user", cascade="all, delete-orphan")
    jail_records = relationship("JailRecord", back_populates="user", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('ix_users_username', 'username'),
        Index('ix_users_discriminator', 'discriminator'),
    )

class GuildMember(Base):
    """Guild member model"""
    __tablename__ = "guild_members"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    nickname = Column(String(100), nullable=True)
    joined_at = Column(DateTime, nullable=True)
    roles = Column(Text, nullable=True)  # JSON array of role IDs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    guild = relationship("Guild", back_populates="members")
    user = relationship("User", back_populates="guild_memberships")
    role = relationship("Role", back_populates="members")

    # Indexes
    __table_args__ = (
        Index('ix_guild_members_guild_id', 'guild_id'),
        Index('ix_guild_members_user_id', 'user_id'),
        Index('ix_guild_members_joined_at', 'joined_at'),
    )

class LogConfig(Base):
    """Logging configuration model"""
    __tablename__ = "log_configs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    channel_id = Column(BigInteger, nullable=False)
    enabled = Column(Boolean, default=True)
    log_member_joins = Column(Boolean, default=True)
    log_member_leaves = Column(Boolean, default=True)
    log_message_deletes = Column(Boolean, default=True)
    log_bulk_deletes = Column(Boolean, default=True)
    log_role_changes = Column(Boolean, default=True)
    log_channel_changes = Column(Boolean, default=True)
    log_moderation_actions = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    guild = relationship("Guild", back_populates="log_configs")
    log_entries = relationship("LogEntry", back_populates="log_config", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('ix_log_configs_guild_id', 'guild_id'),
        Index('ix_log_configs_channel_id', 'channel_id'),
    )

class JailConfig(Base):
    """Jail configuration model"""
    __tablename__ = "jail_configs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    channel_id = Column(BigInteger, nullable=True)
    role_id = Column(BigInteger, nullable=True)
    enabled = Column(Boolean, default=True)
    auto_setup = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    guild = relationship("Guild", back_populates="jail_configs")
    jail_records = relationship("JailRecord", back_populates="jail_config", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('ix_jail_configs_guild_id', 'guild_id'),
    )

class JailRecord(Base):
    """Jail record model"""
    __tablename__ = "jail_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    jail_config_id = Column(BigInteger, ForeignKey('jail_configs.id'), nullable=False)
    moderator_id = Column(BigInteger, nullable=False)
    reason = Column(Text, nullable=True)
    original_roles = Column(Text, nullable=True)  # JSON array of role IDs
    jailed_at = Column(DateTime, default=datetime.utcnow)
    released_at = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="jail_records")
    jail_config = relationship("JailConfig", back_populates="jail_records")

    # Indexes
    __table_args__ = (
        Index('ix_jail_records_guild_id', 'guild_id'),
        Index('ix_jail_records_user_id', 'user_id'),
        Index('ix_jail_records_active', 'active'),
        Index('ix_jail_records_jailed_at', 'jailed_at'),
    )

class LogEntry(Base):
    """Log entry model"""
    __tablename__ = "log_entries"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    channel_id = Column(BigInteger, ForeignKey('channels.id'), nullable=True)
    log_config_id = Column(BigInteger, ForeignKey('log_configs.id'), nullable=False)
    event_type = Column(String(50), nullable=False)  # join, leave, message_delete, etc.
    severity = Column(String(20), default="info")  # info, warning, error, critical
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    metadata = Column(Text, nullable=True)  # JSON data
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="log_entries")
    channel = relationship("Channel", back_populates="log_entries")
    log_config = relationship("LogConfig", back_populates="log_entries")

    # Indexes
    __table_args__ = (
        Index('ix_log_entries_guild_id', 'guild_id'),
        Index('ix_log_entries_event_type', 'event_type'),
        Index('ix_log_entries_severity', 'severity'),
        Index('ix_log_entries_timestamp', 'timestamp'),
    )

class CommandUsage(Base):
    """Command usage tracking model"""
    __tablename__ = "command_usage"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    command_name = Column(String(50), nullable=False)
    execution_time = Column(Integer, nullable=False)  # in milliseconds
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User")

    # Indexes
    __table_args__ = (
        Index('ix_command_usage_guild_id', 'guild_id'),
        Index('ix_command_usage_user_id', 'user_id'),
        Index('ix_command_usage_command_name', 'command_name'),
        Index('ix_command_usage_timestamp', 'timestamp'),
    )

class RateLimit(Base):
    """Rate limiting model"""
    __tablename__ = "rate_limits"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    command_name = Column(String(50), nullable=False)
    count = Column(Integer, default=1)
    window_start = Column(DateTime, default=datetime.utcnow)
    window_end = Column(DateTime, nullable=False)

    # Relationships
    user = relationship("User")

    # Indexes
    __table_args__ = (
        Index('ix_rate_limits_guild_user_cmd', 'guild_id', 'user_id', 'command_name'),
        Index('ix_rate_limits_window_end', 'window_end'),
    )

class DatabaseManager:
    """Enhanced database manager with connection pooling and async support"""

    def __init__(self):
        self._engine = None
        self._async_engine = None
        self._session_factory = None
        self._async_session_factory = None
        self._initialize_database()

    def _initialize_database(self):
        """Initialize database engines and session factories"""
        try:
            # Create sync engine for migrations and sync operations
            self._engine = create_engine(
                config_manager.settings.database.database_url,
                poolclass=QueuePool,
                pool_size=config_manager.settings.database.pool_size,
                max_overflow=config_manager.settings.database.max_overflow,
                pool_timeout=config_manager.settings.database.pool_timeout,
                pool_recycle=config_manager.settings.database.pool_recycle,
                echo=config_manager.settings.debug,
                future=True
            )

            # Create async engine for async operations
            self._async_engine = create_async_engine(
                config_manager.settings.database.database_url.replace('postgresql://', 'postgresql+asyncpg://'),
                pool_size=config_manager.settings.database.pool_size,
                max_overflow=config_manager.settings.database.max_overflow,
                pool_timeout=config_manager.settings.database.pool_timeout,
                pool_recycle=config_manager.settings.database.pool_recycle,
                echo=config_manager.settings.debug,
                future=True
            )

            # Create session factories
            self._session_factory = sessionmaker(bind=self._engine, expire_on_commit=False)
            self._async_session_factory = async_sessionmaker(bind=self._async_engine, expire_on_commit=False)

            logger.info("Database engines initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(SQLAlchemyError)
    )
    def get_session(self):
        """Get a synchronous database session"""
        return self._session_factory()

    @asynccontextmanager
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(SQLAlchemyError)
    )
    async def get_async_session(self):
        """Get an asynchronous database session"""
        async with self._async_session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def create_tables(self):
        """Create all database tables"""
        try:
            async with self._async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise

    async def drop_tables(self):
        """Drop all database tables (use with caution)"""
        try:
            async with self._async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            logger.warning("Database tables dropped")
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise

    async def get_or_create_guild(self, guild_id: int, guild_data: Dict[str, Any]) -> Guild:
        """Get or create a guild record"""
        async with self.get_async_session() as session:
            try:
                guild = await session.get(Guild, guild_id)
                if guild:
                    # Update existing guild
                    guild.name = guild_data.get('name', guild.name)
                    guild.owner_id = guild_data.get('owner_id', guild.owner_id)
                    guild.member_count = guild_data.get('member_count', guild.member_count)
                    await session.commit()
                    return guild

                # Create new guild
                guild = Guild(
                    id=guild_id,
                    name=guild_data['name'],
                    owner_id=guild_data['owner_id'],
                    member_count=guild_data.get('member_count', 0)
                )
                session.add(guild)
                await session.commit()
                await session.refresh(guild)
                return guild

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to get or create guild {guild_id}: {e}")
                raise

    async def get_or_create_user(self, user_id: int, user_data: Dict[str, Any]) -> User:
        """Get or create a user record"""
        async with self.get_async_session() as session:
            try:
                user = await session.get(User, user_id)
                if user:
                    # Update existing user
                    user.username = user_data.get('username', user.username)
                    user.discriminator = user_data.get('discriminator', user.discriminator)
                    user.display_name = user_data.get('display_name', user.display_name)
                    user.avatar_hash = user_data.get('avatar_hash', user.avatar_hash)
                    user.banner_hash = user_data.get('banner_hash', user.banner_hash)
                    user.bot = user_data.get('bot', user.bot)
                    user.system = user_data.get('system', user.system)
                    await session.commit()
                    return user

                # Create new user
                user = User(
                    id=user_id,
                    username=user_data['username'],
                    discriminator=user_data['discriminator'],
                    display_name=user_data.get('display_name'),
                    avatar_hash=user_data.get('avatar_hash'),
                    banner_hash=user_data.get('banner_hash'),
                    bot=user_data.get('bot', False),
                    system=user_data.get('system', False)
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to get or create user {user_id}: {e}")
                raise

    async def log_event(self, guild_id: int, event_type: str, title: str, description: str,
                       user_id: Optional[int] = None, channel_id: Optional[int] = None,
                       severity: str = "info", metadata: Optional[Dict[str, Any]] = None) -> LogEntry:
        """Log an event to the database"""
        async with self.get_async_session() as session:
            try:
                # Get or create log config
                log_config = await session.query(LogConfig).filter_by(guild_id=guild_id).first()
                if not log_config:
                    log_config = LogConfig(guild_id=guild_id, enabled=True)
                    session.add(log_config)
                    await session.flush()

                log_entry = LogEntry(
                    guild_id=guild_id,
                    user_id=user_id,
                    channel_id=channel_id,
                    log_config_id=log_config.id,
                    event_type=event_type,
                    severity=severity,
                    title=title,
                    description=description,
                    metadata=json.dumps(metadata) if metadata else None
                )
                session.add(log_entry)
                await session.commit()
                await session.refresh(log_entry)
                return log_entry

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to log event: {e}")
                raise

    async def get_guild_log_config(self, guild_id: int) -> Optional[LogConfig]:
        """Get logging configuration for a guild"""
        async with self.get_async_session() as session:
            return await session.query(LogConfig).filter_by(guild_id=guild_id).first()

    async def update_guild_log_config(self, guild_id: int, **kwargs) -> LogConfig:
        """Update logging configuration for a guild"""
        async with self.get_async_session() as session:
            try:
                log_config = await session.query(LogConfig).filter_by(guild_id=guild_id).first()
                if not log_config:
                    log_config = LogConfig(guild_id=guild_id)
                    session.add(log_config)

                for key, value in kwargs.items():
                    if hasattr(log_config, key):
                        setattr(log_config, key, value)

                await session.commit()
                await session.refresh(log_config)
                return log_config

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to update log config for guild {guild_id}: {e}")
                raise

    async def get_jail_config(self, guild_id: int) -> Optional[JailConfig]:
        """Get jail configuration for a guild"""
        async with self.get_async_session() as session:
            return await session.query(JailConfig).filter_by(guild_id=guild_id).first()

    async def update_jail_config(self, guild_id: int, **kwargs) -> JailConfig:
        """Update jail configuration for a guild"""
        async with self.get_async_session() as session:
            try:
                jail_config = await session.query(JailConfig).filter_by(guild_id=guild_id).first()
                if not jail_config:
                    jail_config = JailConfig(guild_id=guild_id)
                    session.add(jail_config)

                for key, value in kwargs.items():
                    if hasattr(jail_config, key):
                        setattr(jail_config, key, value)

                await session.commit()
                await session.refresh(jail_config)
                return jail_config

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to update jail config for guild {guild_id}: {e}")
                raise

    async def jail_user(self, guild_id: int, user_id: int, moderator_id: int,
                       reason: Optional[str] = None, original_roles: Optional[List[int]] = None) -> JailRecord:
        """Jail a user"""
        async with self.get_async_session() as session:
            try:
                # Get or create jail config
                jail_config = await session.query(JailConfig).filter_by(guild_id=guild_id).first()
                if not jail_config:
                    jail_config = JailConfig(guild_id=guild_id, enabled=True)
                    session.add(jail_config)
                    await session.flush()

                # Check if user is already jailed
                existing_jail = await session.query(JailRecord).filter_by(
                    guild_id=guild_id, user_id=user_id, active=True
                ).first()

                if existing_jail:
                    raise ValueError("User is already jailed")

                jail_record = JailRecord(
                    guild_id=guild_id,
                    user_id=user_id,
                    jail_config_id=jail_config.id,
                    moderator_id=moderator_id,
                    reason=reason,
                    original_roles=json.dumps(original_roles) if original_roles else None
                )
                session.add(jail_record)
                await session.commit()
                await session.refresh(jail_record)
                return jail_record

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to jail user {user_id} in guild {guild_id}: {e}")
                raise

    async def unjail_user(self, guild_id: int, user_id: int) -> Optional[JailRecord]:
        """Release a user from jail"""
        async with self.get_async_session() as session:
            try:
                jail_record = await session.query(JailRecord).filter_by(
                    guild_id=guild_id, user_id=user_id, active=True
                ).first()

                if not jail_record:
                    return None

                jail_record.active = False
                jail_record.released_at = datetime.utcnow()
                await session.commit()
                return jail_record

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to unjail user {user_id} in guild {guild_id}: {e}")
                raise

    async def get_active_jail_records(self, guild_id: int) -> List[JailRecord]:
        """Get all active jail records for a guild"""
        async with self.get_async_session() as session:
            result = await session.query(JailRecord).filter_by(guild_id=guild_id, active=True).all()
            return result

    async def track_command_usage(self, guild_id: Optional[int], user_id: int,
                                 command_name: str, execution_time: int,
                                 success: bool = True, error_message: Optional[str] = None):
        """Track command usage"""
        async with self.get_async_session() as session:
            try:
                usage = CommandUsage(
                    guild_id=guild_id,
                    user_id=user_id,
                    command_name=command_name,
                    execution_time=execution_time,
                    success=success,
                    error_message=error_message
                )
                session.add(usage)
                await session.commit()

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to track command usage: {e}")

    async def check_rate_limit(self, guild_id: Optional[int], user_id: int,
                              command_name: str) -> bool:
        """Check if user has exceeded rate limits"""
        async with self.get_async_session() as session:
            try:
                now = datetime.utcnow()
                one_minute_ago = now - timedelta(minutes=1)
                one_hour_ago = now - timedelta(hours=1)

                # Check per-minute limit
                minute_count = await session.query(RateLimit).filter(
                    RateLimit.guild_id == guild_id,
                    RateLimit.user_id == user_id,
                    RateLimit.command_name == command_name,
                    RateLimit.window_start >= one_minute_ago
                ).count()

                if minute_count >= config_manager.settings.security.max_commands_per_minute:
                    return False

                # Check per-hour limit
                hour_count = await session.query(RateLimit).filter(
                    RateLimit.guild_id == guild_id,
                    RateLimit.user_id == user_id,
                    RateLimit.command_name == command_name,
                    RateLimit.window_start >= one_hour_ago
                ).count()

                if hour_count >= config_manager.settings.security.max_commands_per_hour:
                    return False

                # Record this usage
                rate_limit = RateLimit(
                    guild_id=guild_id,
                    user_id=user_id,
                    command_name=command_name,
                    window_end=now + timedelta(hours=1)
                )
                session.add(rate_limit)
                await session.commit()

                return True

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to check rate limit: {e}")
                return True  # Allow on error to prevent blocking

    async def cleanup_old_logs(self, days: int = 30):
        """Clean up old log entries"""
        async with self.get_async_session() as session:
            try:
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                deleted_count = await session.query(LogEntry).filter(
                    LogEntry.timestamp < cutoff_date
                ).delete()

                await session.commit()
                logger.info(f"Cleaned up {deleted_count} old log entries")

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to cleanup old logs: {e}")

    async def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        async with self.get_async_session() as session:
            try:
                stats = {}

                # Count records in each table
                stats['guilds'] = await session.query(Guild).count()
                stats['users'] = await session.query(User).count()
                stats['channels'] = await session.query(Channel).count()
                stats['roles'] = await session.query(Role).count()
                stats['log_entries'] = await session.query(LogEntry).count()
                stats['jail_records'] = await session.query(JailRecord).count()
                stats['command_usage'] = await session.query(CommandUsage).count()

                # Get recent activity
                recent_logs = await session.query(LogEntry).filter(
                    LogEntry.timestamp >= datetime.utcnow() - timedelta(hours=24)
                ).count()
                stats['recent_logs_24h'] = recent_logs

                active_jails = await session.query(JailRecord).filter_by(active=True).count()
                stats['active_jails'] = active_jails

                return stats

            except Exception as e:
                logger.error(f"Failed to get database stats: {e}")
                return {}

# Global database manager instance
db_manager = DatabaseManager()
