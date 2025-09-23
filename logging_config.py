"""
Advanced Logging System
Provides structured logging with multiple outputs, rotation, and external integrations.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import json
import asyncio
from datetime import datetime
import structlog
from pythonjsonlogger import jsonlogger
import requests
from config import config_manager
import traceback

class EnhancedJSONFormatter(jsonlogger.JsonFormatter):
    """Enhanced JSON formatter with additional context"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._additional_fields = {}

    def add_fields(self, level, message, args, exc_info=None, extra=None):
        """Add custom fields to log records"""
        super().add_fields(level, message, args, exc_info, extra)

        # Add timestamp with timezone
        if extra and 'time' in extra:
            extra['timestamp'] = datetime.fromtimestamp(extra['time']).isoformat()

        # Add component information
        if extra:
            extra.setdefault('component', 'bot')
            extra.setdefault('environment', config_manager.settings.environment)
            extra.setdefault('bot_name', config_manager.settings.bot_name)

    def set_additional_fields(self, fields: Dict[str, Any]):
        """Set additional fields to include in all logs"""
        self._additional_fields.update(fields)

class ExternalLogHandler(logging.Handler):
    """Handler for sending logs to external services"""

    def __init__(self, url: str, api_key: Optional[str] = None, batch_size: int = 10):
        super().__init__()
        self.url = url
        self.api_key = api_key
        self.batch_size = batch_size
        self._log_queue = asyncio.Queue()
        self._batch = []
        self._shutdown_event = asyncio.Event()

        # Start background task for sending logs
        self._task = asyncio.create_task(self._process_queue())

    def emit(self, record):
        """Add log record to queue for processing"""
        try:
            log_entry = self.format(record)
            # Use asyncio.create_task to avoid blocking
            asyncio.create_task(self._log_queue.put(log_entry))
        except Exception:
            self.handleError(record)

    async def _process_queue(self):
        """Process log queue and send batches to external service"""
        while not self._shutdown_event.is_set():
            try:
                # Wait for log entries with timeout
                try:
                    log_entry = await asyncio.wait_for(self._log_queue.get(), timeout=1.0)
                    self._batch.append(log_entry)
                except asyncio.TimeoutError:
                    pass

                # Send batch if it's large enough or timeout occurred
                if len(self._batch) >= self._batch_size:
                    await self._send_batch()

            except Exception as e:
                print(f"Error processing log queue: {e}")

    async def _send_batch(self):
        """Send batch of logs to external service"""
        if not self._batch:
            return

        try:
            headers = {'Content-Type': 'application/json'}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'

            payload = {
                'logs': self._batch,
                'timestamp': datetime.utcnow().isoformat(),
                'source': config_manager.settings.bot_name
            }

            async with asyncio.timeout(5):  # 5 second timeout
                response = requests.post(self.url, json=payload, headers=headers, timeout=5)

            if response.status_code == 200:
                self._batch.clear()
            else:
                print(f"Failed to send logs: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Error sending logs to external service: {e}")

    async def shutdown(self):
        """Shutdown the handler and send remaining logs"""
        self._shutdown_event.set()
        if self._task:
            await self._task
        await self._send_batch()  # Send any remaining logs

class DatabaseLogHandler(logging.Handler):
    """Handler for logging to database"""

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self._log_queue = asyncio.Queue()
        self._batch = []
        self._batch_size = 50
        self._shutdown_event = asyncio.Event()

        # Start background task
        self._task = asyncio.create_task(self._process_queue())

    def emit(self, record):
        """Add log record to queue"""
        try:
            log_entry = {
                'level': record.levelname,
                'message': record.getMessage(),
                'timestamp': datetime.fromtimestamp(record.created),
                'component': getattr(record, 'component', 'bot'),
                'extra': getattr(record, 'extra_data', {})
            }
            asyncio.create_task(self._log_queue.put(log_entry))
        except Exception:
            self.handleError(record)

    async def _process_queue(self):
        """Process log queue and batch insert to database"""
        while not self._shutdown_event.is_set():
            try:
                try:
                    log_entry = await asyncio.wait_for(self._log_queue.get(), timeout=1.0)
                    self._batch.append(log_entry)
                except asyncio.TimeoutError:
                    pass

                if len(self._batch) >= self._batch_size:
                    await self._insert_batch()

            except Exception as e:
                print(f"Error processing database log queue: {e}")

    async def _insert_batch(self):
        """Insert batch of logs to database"""
        if not self._batch:
            return

        try:
            # Convert batch to database log entries
            log_entries = []
            for entry in self._batch:
                # This would be implemented with actual database insertion
                # For now, just clear the batch
                pass

            self._batch.clear()

        except Exception as e:
            print(f"Error inserting logs to database: {e}")

    async def shutdown(self):
        """Shutdown handler"""
        self._shutdown_event.set()
        if self._task:
            await self._task
        await self._insert_batch()

class LogManager:
    """Enhanced logging manager with multiple outputs and structured logging"""

    def __init__(self):
        self._handlers = {}
        self._external_handler = None
        self._database_handler = None
        self._setup_logging()

    def _setup_logging(self):
        """Set up comprehensive logging configuration"""
        # Create logs directory
        log_dir = Path(config_manager.settings.logging.log_file_path).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        # Configure structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        # Set up root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, config_manager.settings.logging.level.upper()))

        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Create formatters
        json_formatter = EnhancedJSONFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(json_formatter)
        root_logger.addHandler(console_handler)

        # File handler with rotation
        if config_manager.settings.logging.enable_file_logging:
            file_handler = logging.handlers.RotatingFileHandler(
                filename=config_manager.settings.logging.log_file_path,
                maxBytes=config_manager.settings.logging.max_file_size,
                backupCount=config_manager.settings.logging.backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, config_manager.settings.logging.level.upper()))
            file_handler.setFormatter(json_formatter)
            root_logger.addHandler(file_handler)

        # External logging handler
        if (config_manager.settings.logging.enable_external_logging and
            config_manager.settings.logging.external_logging_url):

            self._external_handler = ExternalLogHandler(
                url=config_manager.settings.logging.external_logging_url,
                api_key=config_manager.get_encrypted_value('EXTERNAL_LOG_API_KEY')
            )
            self._external_handler.setLevel(logging.INFO)
            self._external_handler.setFormatter(json_formatter)
            root_logger.addHandler(self._external_handler)

        # Database logging handler
        # Note: This would be initialized after database is available
        # self._database_handler = DatabaseLogHandler(db_manager)

        # Set specific log levels for noisy libraries
        logging.getLogger('discord').setLevel(logging.WARNING)
        logging.getLogger('discord.http').setLevel(logging.WARNING)
        logging.getLogger('discord.gateway').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('asyncio').setLevel(logging.WARNING)

        # Log startup information
        logger = structlog.get_logger(__name__)
        logger.info("Logging system initialized",
                   environment=config_manager.settings.environment,
                   log_level=config_manager.settings.logging.level,
                   file_logging=config_manager.settings.logging.enable_file_logging,
                   external_logging=config_manager.settings.logging.enable_external_logging)

    def get_logger(self, name: str, **kwargs) -> Any:
        """Get a structured logger with context"""
        logger = structlog.get_logger(name)

        # Add default context
        context = {
            'component': name,
            'environment': config_manager.settings.environment,
            'bot_name': config_manager.settings.bot_name,
            **kwargs
        }

        return logger.bind(**context)

    def log_command_usage(self, guild_id: Optional[int], user_id: int,
                         command_name: str, execution_time: int,
                         success: bool = True, error_message: Optional[str] = None):
        """Log command usage"""
        logger = self.get_logger('command_usage')
        logger.info("Command executed",
                   guild_id=guild_id,
                   user_id=user_id,
                   command=command_name,
                   execution_time=execution_time,
                   success=success,
                   error=error_message)

    def log_guild_event(self, guild_id: int, event_type: str,
                       title: str, description: str,
                       user_id: Optional[int] = None,
                       channel_id: Optional[int] = None,
                       severity: str = "info",
                       metadata: Optional[Dict[str, Any]] = None):
        """Log guild-related events"""
        logger = self.get_logger('guild_event')
        logger.info("Guild event",
                   guild_id=guild_id,
                   event_type=event_type,
                   title=title,
                   description=description,
                   user_id=user_id,
                   channel_id=channel_id,
                   severity=severity,
                   **(metadata or {}))

    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None,
                  user_id: Optional[int] = None, guild_id: Optional[int] = None):
        """Log errors with context"""
        logger = self.get_logger('error_handler')

        error_context = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'user_id': user_id,
            'guild_id': guild_id,
            **(context or {})
        }

        logger.error("Exception occurred", **error_context)

    def log_performance(self, operation: str, duration: float,
                       **context):
        """Log performance metrics"""
        logger = self.get_logger('performance')
        logger.info("Performance metric",
                   operation=operation,
                   duration=duration,
                   **context)

    def log_security_event(self, event_type: str, user_id: Optional[int] = None,
                          guild_id: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        """Log security-related events"""
        logger = self.get_logger('security')
        logger.warning("Security event",
                      event_type=event_type,
                      user_id=user_id,
                      guild_id=guild_id,
                      **(details or {}))

    def update_context(self, **context):
        """Update default context for all loggers"""
        # This would update the structlog context factory
        pass

    async def shutdown(self):
        """Shutdown logging system gracefully"""
        logger = self.get_logger('logging')

        # Shutdown external handler
        if self._external_handler:
            await self._external_handler.shutdown()

        # Shutdown database handler
        if self._database_handler:
            await self._database_handler.shutdown()

        logger.info("Logging system shutdown complete")

# Global logging manager instance
log_manager = LogManager()
