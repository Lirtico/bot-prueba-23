"""
Enhanced Database System
Provides persistent storage with SQLAlchemy ORM, migrations, and connection pooling.
"""

import asyncio
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, BigInteger, ForeignKey, Index, event, Float
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

class EconomySettings(Base):
    """Economy settings for guilds"""
    __tablename__ = "economy_settings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    currency_symbol = Column(String(10), default="$")
    start_balance = Column(BigInteger, default=100)
    max_balance = Column(BigInteger, default=1000000)
    audit_log_channel_id = Column(BigInteger, nullable=True)
    work_cooldown = Column(Integer, default=3600)  # seconds
    slut_cooldown = Column(Integer, default=3600)
    crime_cooldown = Column(Integer, default=3600)
    rob_cooldown = Column(Integer, default=3600)
    work_min_payout = Column(BigInteger, default=10)
    work_max_payout = Column(BigInteger, default=100)
    slut_min_payout = Column(BigInteger, default=20)
    slut_max_payout = Column(BigInteger, default=200)
    crime_min_payout = Column(BigInteger, default=50)
    crime_max_payout = Column(BigInteger, default=500)
    crime_fail_rate = Column(Float, default=0.4)
    slut_fail_rate = Column(Float, default=0.3)
    fine_type = Column(String(10), default="percent")  # percent or fixed
    fine_percent = Column(Float, default=0.1)
    fine_fixed = Column(BigInteger, default=50)
    chat_money_enabled = Column(Boolean, default=False)
    chat_money_min = Column(BigInteger, default=1)
    chat_money_max = Column(BigInteger, default=5)
    chat_money_cooldown = Column(Integer, default=60)
    chat_money_channels = Column(Text, nullable=True)  # JSON array of channel IDs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    guild = relationship("Guild")

    # Indexes
    __table_args__ = (
        Index('ix_economy_settings_guild_id', 'guild_id'),
    )

class UserEconomy(Base):
    """User economy data"""
    __tablename__ = "user_economy"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    cash = Column(BigInteger, default=0)
    bank = Column(BigInteger, default=0)
    total_earned = Column(BigInteger, default=0)
    last_work = Column(DateTime, nullable=True)
    last_slut = Column(DateTime, nullable=True)
    last_crime = Column(DateTime, nullable=True)
    last_rob = Column(DateTime, nullable=True)
    last_chat_money = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    guild = relationship("Guild")
    user = relationship("User")

    # Indexes
    __table_args__ = (
        Index('ix_user_economy_guild_user', 'guild_id', 'user_id'),
    )

class EconomyTransaction(Base):
    """Economy transactions for audit log"""
    __tablename__ = "economy_transactions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    type = Column(String(50), nullable=False)  # add_money, remove_money, deposit, withdraw, etc.
    amount = Column(BigInteger, nullable=False)
    reason = Column(Text, nullable=True)
    moderator_id = Column(BigInteger, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    guild = relationship("Guild")
    user = relationship("User")

    # Indexes
    __table_args__ = (
        Index('ix_economy_transactions_guild_user', 'guild_id', 'user_id'),
        Index('ix_economy_transactions_timestamp', 'timestamp'),
    )

class EconomyItem(Base):
    """Store items"""
    __tablename__ = "economy_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(BigInteger, nullable=False)
    sell_price = Column(BigInteger, nullable=True)
    stock = Column(Integer, default=-1)  # -1 for unlimited
    role_required = Column(BigInteger, nullable=True)  # role ID required to buy
    role_granted = Column(BigInteger, nullable=True)  # role ID granted on use
    usable = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    guild = relationship("Guild")

    # Indexes
    __table_args__ = (
        Index('ix_economy_items_guild_id', 'guild_id'),
    )

class UserItem(Base):
    """User inventory"""
    __tablename__ = "user_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    item_id = Column(BigInteger, ForeignKey('economy_items.id'), nullable=False)
    quantity = Column(Integer, default=1)
    acquired_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    guild = relationship("Guild")
    user = relationship("User")
    item = relationship("EconomyItem")

    # Indexes
    __table_args__ = (
        Index('ix_user_items_guild_user', 'guild_id', 'user_id'),
        Index('ix_user_items_item_id', 'item_id'),
    )

class RoleIncome(Base):
    """Role-based income"""
    __tablename__ = "role_income"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    role_id = Column(BigInteger, nullable=False)
    income_amount = Column(BigInteger, nullable=False)
    cooldown = Column(Integer, default=86400)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    guild = relationship("Guild")

    # Indexes
    __table_args__ = (
        Index('ix_role_income_guild_role', 'guild_id', 'role_id'),
    )

class UserRoleIncome(Base):
    """User role income tracking"""
    __tablename__ = "user_role_income"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    role_income_id = Column(BigInteger, ForeignKey('role_income.id'), nullable=False)
    last_collected = Column(DateTime, nullable=True)

    # Relationships
    guild = relationship("Guild")
    user = relationship("User")
    role_income = relationship("RoleIncome")

    # Indexes
    __table_args__ = (
        Index('ix_user_role_income_guild_user', 'guild_id', 'user_id'),
    )

class CustomReply(Base):
    """Custom replies for commands"""
    __tablename__ = "custom_replies"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    command = Column(String(20), nullable=False)  # work, slut, crime
    type = Column(String(10), nullable=False)  # success, fail
    reply = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    guild = relationship("Guild")

    # Indexes
    __table_args__ = (
        Index('ix_custom_replies_guild_cmd', 'guild_id', 'command'),
    )

class GameSettings(Base):
    """Game settings for guilds"""
    __tablename__ = "game_settings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    min_bet = Column(BigInteger, default=1)
    max_bet = Column(BigInteger, default=10000)
    blackjack_decks = Column(Integer, default=1)
    game_cooldown = Column(Integer, default=10)  # seconds
    slot_symbols = Column(Text, default='["🍒", "🍊", "🍇", "🍉", "⭐", "💎"]')  # JSON
    cock_fight_win_chance = Column(Float, default=0.5)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    guild = relationship("Guild")

    # Indexes
    __table_args__ = (
        Index('ix_game_settings_guild_id', 'guild_id'),
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
                stats['economy_settings'] = await session.query(EconomySettings).count()
                stats['user_economy'] = await session.query(UserEconomy).count()
                stats['economy_transactions'] = await session.query(EconomyTransaction).count()
                stats['economy_items'] = await session.query(EconomyItem).count()
                stats['user_items'] = await session.query(UserItem).count()
                stats['role_income'] = await session.query(RoleIncome).count()
                stats['custom_replies'] = await session.query(CustomReply).count()
                stats['game_settings'] = await session.query(GameSettings).count()

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

    # Economy-related methods
    async def get_or_create_economy_settings(self, guild_id: int) -> EconomySettings:
        """Get or create economy settings for a guild"""
        async with self.get_async_session() as session:
            try:
                settings = await session.query(EconomySettings).filter_by(guild_id=guild_id).first()
                if settings:
                    return settings

                settings = EconomySettings(guild_id=guild_id)
                session.add(settings)
                await session.commit()
                await session.refresh(settings)
                return settings

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to get or create economy settings for guild {guild_id}: {e}")
                raise

    async def update_economy_settings(self, guild_id: int, **kwargs) -> EconomySettings:
        """Update economy settings for a guild"""
        async with self.get_async_session() as session:
            try:
                settings = await session.query(EconomySettings).filter_by(guild_id=guild_id).first()
                if not settings:
                    settings = EconomySettings(guild_id=guild_id)
                    session.add(settings)

                for key, value in kwargs.items():
                    if hasattr(settings, key):
                        setattr(settings, key, value)

                await session.commit()
                await session.refresh(settings)
                return settings

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to update economy settings for guild {guild_id}: {e}")
                raise

    async def get_or_create_user_economy(self, guild_id: int, user_id: int) -> UserEconomy:
        """Get or create user economy data"""
        async with self.get_async_session() as session:
            try:
                economy = await session.query(UserEconomy).filter_by(guild_id=guild_id, user_id=user_id).first()
                if economy:
                    return economy

                settings = await self.get_or_create_economy_settings(guild_id)
                economy = UserEconomy(
                    guild_id=guild_id,
                    user_id=user_id,
                    cash=settings.start_balance
                )
                session.add(economy)
                await session.commit()
                await session.refresh(economy)
                return economy

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to get or create user economy for user {user_id} in guild {guild_id}: {e}")
                raise

    async def update_user_balance(self, guild_id: int, user_id: int, cash_change: int = 0, bank_change: int = 0,
                                 reason: str = None, moderator_id: int = None) -> UserEconomy:
        """Update user balance and log transaction"""
        async with self.get_async_session() as session:
            try:
                economy = await session.query(UserEconomy).filter_by(guild_id=guild_id, user_id=user_id).first()
                if not economy:
                    economy = await self.get_or_create_user_economy(guild_id, user_id)

                # Check max balance
                settings = await self.get_or_create_economy_settings(guild_id)
                new_cash = economy.cash + cash_change
                new_bank = economy.bank + bank_change

                if new_cash > settings.max_balance or new_bank > settings.max_balance:
                    raise ValueError(f"Balance would exceed maximum of {settings.max_balance}")

                if new_cash < 0 or new_bank < 0:
                    raise ValueError("Balance cannot be negative")

                economy.cash = new_cash
                economy.bank = new_bank
                economy.total_earned += max(0, cash_change) + max(0, bank_change)

                # Log transaction
                if cash_change != 0 or bank_change != 0:
                    transaction = EconomyTransaction(
                        guild_id=guild_id,
                        user_id=user_id,
                        type="balance_update",
                        amount=cash_change + bank_change,
                        reason=reason,
                        moderator_id=moderator_id
                    )
                    session.add(transaction)

                await session.commit()
                await session.refresh(economy)
                return economy

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to update balance for user {user_id} in guild {guild_id}: {e}")
                raise

    async def get_leaderboard(self, guild_id: int, limit: int = 10) -> List[UserEconomy]:
        """Get economy leaderboard for a guild"""
        async with self.get_async_session() as session:
            try:
                result = await session.query(UserEconomy).filter_by(guild_id=guild_id).order_by(
                    (UserEconomy.cash + UserEconomy.bank).desc()
                ).limit(limit).all()
                return result

            except Exception as e:
                logger.error(f"Failed to get leaderboard for guild {guild_id}: {e}")
                return []

    async def get_game_settings(self, guild_id: int) -> GameSettings:
        """Get game settings for a guild"""
        async with self.get_async_session() as session:
            try:
                settings = await session.query(GameSettings).filter_by(guild_id=guild_id).first()
                if settings:
                    return settings

                settings = GameSettings(guild_id=guild_id)
                session.add(settings)
                await session.commit()
                await session.refresh(settings)
                return settings

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to get game settings for guild {guild_id}: {e}")
                raise

    async def update_game_settings(self, guild_id: int, **kwargs) -> GameSettings:
        """Update game settings for a guild"""
        async with self.get_async_session() as session:
            try:
                settings = await session.query(GameSettings).filter_by(guild_id=guild_id).first()
                if not settings:
                    settings = GameSettings(guild_id=guild_id)
                    session.add(settings)

                for key, value in kwargs.items():
                    if hasattr(settings, key):
                        setattr(settings, key, value)

                await session.commit()
                await session.refresh(settings)
                return settings

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to update game settings for guild {guild_id}: {e}")
                raise

    async def add_economy_transaction(self, guild_id: int, user_id: int, transaction_type: str,
                                    amount: int, reason: str = None, moderator_id: int = None):
        """Add an economy transaction"""
        async with self.get_async_session() as session:
            try:
                transaction = EconomyTransaction(
                    guild_id=guild_id,
                    user_id=user_id,
                    type=transaction_type,
                    amount=amount,
                    reason=reason,
                    moderator_id=moderator_id
                )
                session.add(transaction)
                await session.commit()

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to add economy transaction: {e}")

    async def get_user_inventory(self, guild_id: int, user_id: int) -> List[UserItem]:
        """Get user's inventory"""
        async with self.get_async_session() as session:
            try:
                result = await session.query(UserItem).filter_by(guild_id=guild_id, user_id=user_id).all()
                return result

            except Exception as e:
                logger.error(f"Failed to get inventory for user {user_id} in guild {guild_id}: {e}")
                return []

    async def add_item_to_inventory(self, guild_id: int, user_id: int, item_id: int, quantity: int = 1):
        """Add item to user's inventory"""
        async with self.get_async_session() as session:
            try:
                # Check if user already has this item
                existing = await session.query(UserItem).filter_by(
                    guild_id=guild_id, user_id=user_id, item_id=item_id
                ).first()

                if existing:
                    existing.quantity += quantity
                else:
                    user_item = UserItem(
                        guild_id=guild_id,
                        user_id=user_id,
                        item_id=item_id,
                        quantity=quantity
                    )
                    session.add(user_item)

                await session.commit()

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to add item to inventory: {e}")

    async def remove_item_from_inventory(self, guild_id: int, user_id: int, item_id: int, quantity: int = 1) -> bool:
        """Remove item from user's inventory"""
        async with self.get_async_session() as session:
            try:
                existing = await session.query(UserItem).filter_by(
                    guild_id=guild_id, user_id=user_id, item_id=item_id
                ).first()

                if not existing or existing.quantity < quantity:
                    return False

                existing.quantity -= quantity
                if existing.quantity <= 0:
                    await session.delete(existing)

                await session.commit()
                return True

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to remove item from inventory: {e}")
                return False

    async def get_store_items(self, guild_id: int) -> List[EconomyItem]:
        """Get all store items for a guild"""
        async with self.get_async_session() as session:
            try:
                result = await session.query(EconomyItem).filter_by(guild_id=guild_id).all()
                return result

            except Exception as e:
                logger.error(f"Failed to get store items for guild {guild_id}: {e}")
                return []

    async def create_store_item(self, guild_id: int, name: str, description: str, price: int,
                              sell_price: int = None, stock: int = -1, role_required: int = None,
                              role_granted: int = None, usable: bool = False) -> EconomyItem:
        """Create a new store item"""
        async with self.get_async_session() as session:
            try:
                item = EconomyItem(
                    guild_id=guild_id,
                    name=name,
                    description=description,
                    price=price,
                    sell_price=sell_price,
                    stock=stock,
                    role_required=role_required,
                    role_granted=role_granted,
                    usable=usable
                )
                session.add(item)
                await session.commit()
                await session.refresh(item)
                return item

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to create store item: {e}")
                raise

    async def get_custom_replies(self, guild_id: int, command: str, reply_type: str) -> List[CustomReply]:
        """Get custom replies for a command"""
        async with self.get_async_session() as session:
            try:
                result = await session.query(CustomReply).filter_by(
                    guild_id=guild_id, command=command, type=reply_type
                ).all()
                return result

            except Exception as e:
                logger.error(f"Failed to get custom replies: {e}")
                return []

    async def add_custom_reply(self, guild_id: int, command: str, reply_type: str, reply: str):
        """Add a custom reply"""
        async with self.get_async_session() as session:
            try:
                custom_reply = CustomReply(
                    guild_id=guild_id,
                    command=command,
                    type=reply_type,
                    reply=reply
                )
                session.add(custom_reply)
                await session.commit()

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to add custom reply: {e}")

    async def delete_custom_reply(self, guild_id: int, reply_id: int) -> bool:
        """Delete a custom reply"""
        async with self.get_async_session() as session:
            try:
                reply = await session.get(CustomReply, reply_id)
                if reply and reply.guild_id == guild_id:
                    await session.delete(reply)
                    await session.commit()
                    return True
                return False

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to delete custom reply: {e}")
                return False

    async def get_role_income(self, guild_id: int, role_id: int) -> Optional[RoleIncome]:
        """Get role income settings"""
        async with self.get_async_session() as session:
            try:
                return await session.query(RoleIncome).filter_by(guild_id=guild_id, role_id=role_id).first()

            except Exception as e:
                logger.error(f"Failed to get role income: {e}")
                return None

    async def set_role_income(self, guild_id: int, role_id: int, income_amount: int, cooldown: int = 86400):
        """Set role income"""
        async with self.get_async_session() as session:
            try:
                role_income = await session.query(RoleIncome).filter_by(guild_id=guild_id, role_id=role_id).first()
                if role_income:
                    role_income.income_amount = income_amount
                    role_income.cooldown = cooldown
                else:
                    role_income = RoleIncome(
                        guild_id=guild_id,
                        role_id=role_id,
                        income_amount=income_amount,
                        cooldown=cooldown
                    )
                    session.add(role_income)

                await session.commit()

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to set role income: {e}")

    async def collect_role_income(self, guild_id: int, user_id: int, role_id: int) -> Optional[int]:
        """Collect role income for user"""
        async with self.get_async_session() as session:
            try:
                role_income = await session.query(RoleIncome).filter_by(guild_id=guild_id, role_id=role_id).first()
                if not role_income:
                    return None

                # Check if user can collect
                user_role_income = await session.query(UserRoleIncome).filter_by(
                    guild_id=guild_id, user_id=user_id, role_income_id=role_income.id
                ).first()

                now = datetime.utcnow()
                if user_role_income and user_role_income.last_collected:
                    time_diff = (now - user_role_income.last_collected).total_seconds()
                    if time_diff < role_income.cooldown:
                        return None  # Not ready yet

                # Update last collected
                if user_role_income:
                    user_role_income.last_collected = now
                else:
                    user_role_income = UserRoleIncome(
                        guild_id=guild_id,
                        user_id=user_id,
                        role_income_id=role_income.id,
                        last_collected=now
                    )
                    session.add(user_role_income)

                await session.commit()
                return role_income.income_amount

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to collect role income: {e}")
                return None

    async def reset_economy(self, guild_id: int):
        """Reset all economy data for a guild"""
        async with self.get_async_session() as session:
            try:
                # Reset user economies
                await session.query(UserEconomy).filter_by(guild_id=guild_id).update({"cash": 0, "bank": 0, "total_earned": 0})
                # Delete transactions
                await session.query(EconomyTransaction).filter_by(guild_id=guild_id).delete()
                # Delete user items
                await session.query(UserItem).filter_by(guild_id=guild_id).delete()
                # Delete custom replies
                await session.query(CustomReply).filter_by(guild_id=guild_id).delete()

                await session.commit()

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to reset economy for guild {guild_id}: {e}")

    async def clean_leaderboard(self, guild_id: int):
        """Remove users from leaderboard that have left the guild"""
        async with self.get_async_session() as session:
            try:
                # Get all users in economy
                economy_users = await session.query(UserEconomy).filter_by(guild_id=guild_id).all()

                # Check which users are still in the guild (this would need guild member data)
                # For now, just remove users with 0 balance
                deleted_count = await session.query(UserEconomy).filter(
                    UserEconomy.guild_id == guild_id,
                    UserEconomy.cash == 0,
                    UserEconomy.bank == 0
                ).delete()

                await session.commit()
                return deleted_count

            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to clean leaderboard for guild {guild_id}: {e}")
                return 0

# Global database manager instance
db_manager = DatabaseManager()
