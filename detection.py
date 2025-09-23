"""
Enhanced Detection Module
Provides sophisticated event detection, pattern recognition, and threat analysis.
"""

import asyncio
import re
import time
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import logging
from enum import Enum

from config import config_manager
from database import db_manager
from logging_config import log_manager

logger = log_manager.get_logger(__name__)

class ThreatLevel(Enum):
    """Threat level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DetectionType(Enum):
    """Type of detection"""
    SPAM = "spam"
    RAID = "raid"
    MALICIOUS_LINKS = "malicious_links"
    SUSPICIOUS_PATTERNS = "suspicious_patterns"
    RATE_LIMIT_VIOLATION = "rate_limit_violation"
    BOT_DETECTION = "bot_detection"
    INVITE_ABUSE = "invite_abuse"
    MASS_MENTION = "mass_mention"

@dataclass
class DetectionRule:
    """Detection rule configuration"""
    name: str
    detection_type: DetectionType
    enabled: bool = True
    threshold: int = 5
    time_window: int = 60  # seconds
    cooldown_period: int = 300  # seconds
    action: str = "log"  # log, warn, kick, ban, jail
    severity: ThreatLevel = ThreatLevel.MEDIUM
    patterns: List[str] = field(default_factory=list)
    description: str = ""

@dataclass
class DetectionEvent:
    """Detection event data"""
    guild_id: int
    user_id: int
    detection_type: DetectionType
    threat_level: ThreatLevel
    confidence: float
    details: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    resolved: bool = False
    resolution: Optional[str] = None

class PatternMatcher:
    """Advanced pattern matching for suspicious content"""

    def __init__(self):
        self._compiled_patterns = {}
        self._initialize_patterns()

    def _initialize_patterns(self):
        """Initialize regex patterns for detection"""
        patterns = {
            'discord_invites': re.compile(r'(?:https?://)?discord(?:app\.com/invite|\.gg)/[a-zA-Z0-9]+'),
            'suspicious_urls': re.compile(r'https?://(?:[^\.]+\.)*(?:hack|exploit|malware|virus|phish|scam|fake)[^\s]*', re.IGNORECASE),
            'mass_mentions': re.compile(r'@(?:everyone|here)|\b(?:\d{15,20})\b.*@(?:everyone|here)'),
            'spam_patterns': re.compile(r'(.)\1{10,}|(.{2,})\1{5,}', re.IGNORECASE),
            'caps_lock': re.compile(r'[A-Z]{20,}'),
            'repeated_messages': re.compile(r'^(.{10,})\1+$'),
            'suspicious_commands': re.compile(r'!(?:eval|exec|system|shell|cmd|powershell|bash)', re.IGNORECASE),
            'ip_addresses': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
            'phone_numbers': re.compile(r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'),
            'email_addresses': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
        }

        self._compiled_patterns = patterns

    def match_patterns(self, text: str) -> Dict[str, List[str]]:
        """Match text against all patterns"""
        matches = {}
        for pattern_name, pattern in self._compiled_patterns.items():
            found = pattern.findall(text)
            if found:
                matches[pattern_name] = found
        return matches

    def calculate_suspicious_score(self, text: str, user_context: Dict[str, Any]) -> float:
        """Calculate suspiciousness score for text"""
        score = 0.0
        matches = self.match_patterns(text)

        # Score based on pattern matches
        scoring = {
            'discord_invites': 0.3,
            'suspicious_urls': 0.8,
            'mass_mentions': 0.6,
            'spam_patterns': 0.7,
            'caps_lock': 0.4,
            'repeated_messages': 0.5,
            'suspicious_commands': 0.9,
            'ip_addresses': 0.2,
            'phone_numbers': 0.3,
            'email_addresses': 0.2,
        }

        for pattern, weight in scoring.items():
            if pattern in matches:
                score += weight * len(matches[pattern])

        # Adjust based on user context
        if user_context.get('is_new_user', False):
            score *= 1.5
        if user_context.get('has_avatar', False):
            score *= 0.8
        if user_context.get('account_age_days', 0) < 7:
            score *= 1.3

        return min(score, 1.0)

class RateLimiter:
    """Advanced rate limiting with multiple windows"""

    def __init__(self):
        self._user_actions: Dict[int, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
        self._guild_actions: Dict[int, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
        self._cleanup_task: Optional[asyncio.Task] = None
        self._start_cleanup_task()

    def _start_cleanup_task(self):
        """Start background cleanup task"""
        if self._cleanup_task and not self._cleanup_task.done():
            self._cleanup_task.cancel()

        self._cleanup_task = asyncio.create_task(self._cleanup_old_entries())

    async def _cleanup_old_entries(self):
        """Clean up old rate limit entries"""
        while True:
            try:
                await asyncio.sleep(300)  # Clean up every 5 minutes
                cutoff_time = time.time() - 3600  # Keep last hour

                for user_data in self._user_actions.values():
                    for action_list in user_data.values():
                        # Remove old entries
                        while action_list and action_list[0] < cutoff_time:
                            action_list.pop(0)

                for guild_data in self._guild_actions.values():
                    for action_list in guild_data.values():
                        while action_list and action_list[0] < cutoff_time:
                            action_list.pop(0)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in rate limiter cleanup: {e}")

    def record_action(self, user_id: int, guild_id: Optional[int], action_type: str):
        """Record a user action for rate limiting"""
        current_time = time.time()

        # Record user action
        self._user_actions[user_id][action_type].append(current_time)

        # Record guild action if guild provided
        if guild_id:
            self._guild_actions[guild_id][action_type].append(current_time)

    def is_rate_limited(self, user_id: int, guild_id: Optional[int],
                       action_type: str, threshold: int, window: int) -> Tuple[bool, int]:
        """Check if user is rate limited"""
        current_time = time.time()
        window_start = current_time - window

        # Check user rate limit
        user_actions = self._user_actions[user_id][action_type]
        user_count = sum(1 for t in user_actions if t >= window_start)

        # Check guild rate limit
        guild_count = 0
        if guild_id:
            guild_actions = self._guild_actions[guild_id][action_type]
            guild_count = sum(1 for t in guild_actions if t >= window_start)

        # Consider both user and guild limits
        total_count = user_count + (guild_count * 0.5)  # Guild actions count less

        return total_count >= threshold, int(total_count)

    def get_user_stats(self, user_id: int, time_window: int = 3600) -> Dict[str, int]:
        """Get user action statistics"""
        current_time = time.time()
        window_start = current_time - time_window

        stats = {}
        for action_type, timestamps in self._user_actions[user_id].items():
            count = sum(1 for t in timestamps if t >= window_start)
            if count > 0:
                stats[action_type] = count

        return stats

class ThreatDetector:
    """Main threat detection engine"""

    def __init__(self):
        self.pattern_matcher = PatternMatcher()
        self.rate_limiter = RateLimiter()
        self.detection_rules: Dict[str, DetectionRule] = {}
        self.active_detections: Dict[str, DetectionEvent] = {}
        self._initialize_rules()

    def _initialize_rules(self):
        """Initialize detection rules"""
        rules = [
            DetectionRule(
                name="spam_detection",
                detection_type=DetectionType.SPAM,
                threshold=5,
                time_window=60,
                cooldown_period=300,
                action="warn",
                severity=ThreatLevel.MEDIUM,
                patterns=["spam_patterns", "caps_lock", "repeated_messages"],
                description="Detects spam messages with repeated content or excessive caps"
            ),
            DetectionRule(
                name="raid_detection",
                detection_type=DetectionType.RAID,
                threshold=10,
                time_window=30,
                cooldown_period=600,
                action="jail",
                severity=ThreatLevel.HIGH,
                description="Detects potential raid attempts with high message volume"
            ),
            DetectionRule(
                name="malicious_links",
                detection_type=DetectionType.MALICIOUS_LINKS,
                threshold=1,
                time_window=300,
                cooldown_period=1800,
                action="log",
                severity=ThreatLevel.HIGH,
                patterns=["suspicious_urls"],
                description="Detects potentially malicious URLs"
            ),
            DetectionRule(
                name="mass_mentions",
                detection_type=DetectionType.MASS_MENTION,
                threshold=3,
                time_window=120,
                cooldown_period=600,
                action="warn",
                severity=ThreatLevel.MEDIUM,
                patterns=["mass_mentions"],
                description="Detects excessive mentions of @everyone or @here"
            ),
            DetectionRule(
                name="invite_abuse",
                detection_type=DetectionType.INVITE_ABUSE,
                threshold=5,
                time_window=300,
                cooldown_period=900,
                action="warn",
                severity=ThreatLevel.MEDIUM,
                patterns=["discord_invites"],
                description="Detects excessive Discord invite sharing"
            ),
            DetectionRule(
                name="bot_detection",
                detection_type=DetectionType.BOT_DETECTION,
                threshold=20,
                time_window=60,
                cooldown_period=1800,
                action="log",
                severity=ThreatLevel.LOW,
                description="Detects potential bot behavior patterns"
            ),
            DetectionRule(
                name="rate_limit_violation",
                detection_type=DetectionType.RATE_LIMIT_VIOLATION,
                threshold=config_manager.settings.security.max_commands_per_minute,
                time_window=60,
                cooldown_period=300,
                action="warn",
                severity=ThreatLevel.MEDIUM,
                description="Detects rate limit violations"
            ),
        ]

        self.detection_rules = {rule.name: rule for rule in rules}

    async def analyze_message(self, message_data: Dict[str, Any]) -> List[DetectionEvent]:
        """Analyze a message for threats"""
        events = []

        try:
            guild_id = message_data['guild_id']
            user_id = message_data['user_id']
            content = message_data.get('content', '')
            channel_id = message_data.get('channel_id')

            # Get user context
            user_context = await self._get_user_context(user_id, guild_id)

            # Pattern analysis
            pattern_matches = self.pattern_matcher.match_patterns(content)
            suspicious_score = self.pattern_matcher.calculate_suspicious_score(content, user_context)

            # Rate limiting analysis
            self.rate_limiter.record_action(user_id, guild_id, 'message')

            # Check each detection rule
            for rule_name, rule in self.detection_rules.items():
                if not rule.enabled:
                    continue

                event = await self._check_rule(rule, message_data, pattern_matches, suspicious_score, user_context)
                if event:
                    events.append(event)

            # Log analysis results
            if events:
                logger.warning("Threats detected in message",
                             guild_id=guild_id,
                             user_id=user_id,
                             threat_count=len(events),
                             suspicious_score=suspicious_score)

        except Exception as e:
            logger.error(f"Error analyzing message: {e}")

        return events

    async def _check_rule(self, rule: DetectionRule, message_data: Dict[str, Any],
                         pattern_matches: Dict[str, List[str]], suspicious_score: float,
                         user_context: Dict[str, Any]) -> Optional[DetectionEvent]:
        """Check if a rule matches the message"""

        # Check pattern-based rules
        if rule.patterns:
            matched_patterns = [p for p in rule.patterns if p in pattern_matches]
            if not matched_patterns:
                return None

        # Check rate limiting rules
        if rule.detection_type == DetectionType.RATE_LIMIT_VIOLATION:
            is_limited, count = self.rate_limiter.is_rate_limited(
                message_data['user_id'], message_data['guild_id'],
                'message', rule.threshold, rule.time_window
            )
            if not is_limited:
                return None

        # Calculate confidence based on various factors
        confidence = self._calculate_confidence(rule, pattern_matches, suspicious_score, user_context)

        if confidence < 0.3:  # Minimum confidence threshold
            return None

        # Create detection event
        event = DetectionEvent(
            guild_id=message_data['guild_id'],
            user_id=message_data['user_id'],
            detection_type=rule.detection_type,
            threat_level=rule.severity,
            confidence=confidence,
            details={
                'rule_name': rule.name,
                'pattern_matches': pattern_matches,
                'suspicious_score': suspicious_score,
                'user_context': user_context,
                'message_data': message_data
            }
        )

        return event

    def _calculate_confidence(self, rule: DetectionRule, pattern_matches: Dict[str, List[str]],
                            suspicious_score: float, user_context: Dict[str, Any]) -> float:
        """Calculate confidence score for detection"""

        confidence = 0.0

        # Base confidence from suspicious score
        confidence += suspicious_score * 0.4

        # Pattern match confidence
        if rule.patterns:
            pattern_confidence = len(pattern_matches) / len(rule.patterns)
            confidence += pattern_confidence * 0.3

        # User context factors
        if user_context.get('is_new_user', False):
            confidence += 0.2
        if user_context.get('account_age_days', 0) < 7:
            confidence += 0.1
        if not user_context.get('has_avatar', False):
            confidence += 0.1

        # Rule-specific adjustments
        if rule.detection_type == DetectionType.MALICIOUS_LINKS:
            confidence += 0.2  # Higher confidence for malicious links
        elif rule.detection_type == DetectionType.RAID:
            confidence -= 0.1  # Lower base confidence for raids (needs more evidence)

        return min(confidence, 1.0)

    async def _get_user_context(self, user_id: int, guild_id: int) -> Dict[str, Any]:
        """Get user context for analysis"""
        context = {
            'is_new_user': False,
            'account_age_days': 365,
            'has_avatar': True,
            'guild_join_date': None,
            'previous_warnings': 0
        }

        try:
            # This would query the database for user information
            # For now, return default context
            pass
        except Exception as e:
            logger.error(f"Error getting user context: {e}")

        return context

    async def analyze_user_behavior(self, user_id: int, guild_id: int,
                                  time_window: int = 3600) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        analysis = {
            'message_frequency': 0,
            'command_usage': 0,
            'mention_frequency': 0,
            'link_sharing': 0,
            'suspicious_patterns': [],
            'risk_score': 0.0
        }

        try:
            # Get user statistics from rate limiter
            stats = self.rate_limiter.get_user_stats(user_id, time_window)

            analysis['message_frequency'] = stats.get('message', 0)
            analysis['command_usage'] = stats.get('command', 0)

            # Calculate risk score
            if analysis['message_frequency'] > 50:  # High message volume
                analysis['risk_score'] += 0.3
            if analysis['command_usage'] > 20:  # High command usage
                analysis['risk_score'] += 0.2

        except Exception as e:
            logger.error(f"Error analyzing user behavior: {e}")

        return analysis

    async def get_threat_summary(self, guild_id: int, time_window: int = 3600) -> Dict[str, Any]:
        """Get threat summary for a guild"""
        summary = {
            'total_detections': 0,
            'threats_by_type': {},
            'threats_by_level': {},
            'top_users': [],
            'active_threats': 0
        }

        try:
            # This would query the database for threat statistics
            # For now, return empty summary
            pass
        except Exception as e:
            logger.error(f"Error getting threat summary: {e}")

        return summary

    async def resolve_threat(self, event_id: str, resolution: str, moderator_id: int):
        """Resolve a threat detection"""
        if event_id in self.active_detections:
            event = self.active_detections[event_id]
            event.resolved = True
            event.resolution = resolution

            logger.info("Threat resolved",
                       event_id=event_id,
                       resolution=resolution,
                       moderator_id=moderator_id)

    def update_rule(self, rule_name: str, **kwargs):
        """Update a detection rule"""
        if rule_name in self.detection_rules:
            rule = self.detection_rules[rule_name]
            for key, value in kwargs.items():
                if hasattr(rule, key):
                    setattr(rule, key, value)

            logger.info(f"Detection rule updated: {rule_name}", **kwargs)

    def enable_rule(self, rule_name: str):
        """Enable a detection rule"""
        self.update_rule(rule_name, enabled=True)

    def disable_rule(self, rule_name: str):
        """Disable a detection rule"""
        self.update_rule(rule_name, enabled=False)

# Global threat detector instance
threat_detector = ThreatDetector()
