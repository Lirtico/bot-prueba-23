# Enhanced Discord Bot

A feature-rich, modular Discord bot with advanced moderation, logging, and community management capabilities.

## Features

### 🤖 Core Features
- **Modular Architecture** - Organized into separate cogs for easy maintenance
- **Advanced Moderation** - Automated threat detection and user management
- **Comprehensive Logging** - Detailed logging of all bot activities and events
- **Database Integration** - SQLite database for persistent data storage
- **Jail System** - Automated user isolation for rule violations
- **Statistics Tracking** - Command usage and bot performance analytics

### 🛡️ Security & Moderation
- **Threat Detection** - Real-time analysis for spam, raids, and malicious content
- **Auto-moderation** - Automatic responses to detected threats
- **User Jail System** - Temporary isolation of problematic users
- **Message Filtering** - Automatic deletion of malicious links and spam
- **Warning System** - Progressive discipline for rule violations

### 📊 Analytics & Logging
- **Event Logging** - All server events logged to database
- **Command Tracking** - Usage statistics for all bot commands
- **Performance Monitoring** - Bot uptime and latency tracking
- **User Activity** - Member join/leave tracking and analytics

### 🎯 Community Features
- **Custom Commands** - Extensible command system
- **Role Management** - Advanced role assignment and management
- **Welcome System** - Automated member onboarding
- **Fun Commands** - Entertainment features for community engagement

## Installation

### Prerequisites
- Python 3.12 or higher
- Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))

### Setup
1. **Clone or download** the bot files to your local machine

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**:
   - Copy `.env` and update with your bot token and settings
   - Required: `DISCORD_TOKEN=your_bot_token_here`

4. **Test the installation**:
   ```bash
   python test_bot.py
   ```

5. **Run the bot**:
   ```bash
   python main.py
   ```

## Configuration

The bot uses environment variables for configuration. Copy `.env` and update the following:

### Required Settings
- `DISCORD_TOKEN` - Your Discord bot token
- `DISCORD_APPLICATION_ID` - Your bot's application ID

### Optional Settings
- `ENVIRONMENT` - Set to 'production' for production use
- `DEBUG` - Enable/disable debug mode
- `DATABASE_URL` - Database connection string
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

## Project Structure

```
├── main.py              # Main bot application
├── config.py            # Configuration management
├── database.py          # Database operations
├── logging_config.py    # Logging system
├── detection.py         # Threat detection engine
├── requirements.txt     # Python dependencies
├── .env                 # Environment configuration
├── test_bot.py          # Test script
├── railway.json         # Deployment configuration
└── cogs/                # Bot modules
    ├── admin.py         # Administrative commands
    ├── moderation.py    # Moderation tools
    ├── logging.py       # Logging management
    ├── jail.py          # Jail system
    ├── utility.py       # Utility commands
    ├── fun.py           # Entertainment features
    ├── community.py     # Community management
    ├── error_handler.py # Error handling
    └── help.py          # Help system
```

## Bot Commands

### Administrative Commands
- `/admin status` - View bot statistics and status
- `/admin reload` - Reload bot configuration
- `/admin shutdown` - Gracefully shutdown the bot

### Moderation Commands
- `/moderate warn <user> <reason>` - Warn a user
- `/moderate kick <user> <reason>` - Kick a user
- `/moderate ban <user> <reason>` - Ban a user
- `/moderate unban <user>` - Unban a user

### Jail System
- `/jail <user> <duration> <reason>` - Jail a user
- `/unjail <user>` - Release a user from jail
- `/jail status <user>` - Check jail status

### Utility Commands
- `/info user <user>` - Get user information
- `/info server` - Get server information
- `/stats` - View bot statistics

### Fun Commands
- `/fun joke` - Get a random joke
- `/fun meme` - Get a random meme
- `/fun roll <dice>` - Roll dice

## Database Schema

The bot uses SQLite with the following main tables:
- `guilds` - Server information and settings
- `users` - User profiles and statistics
- `events` - Event logging and audit trail
- `command_usage` - Command usage tracking
- `jail_records` - Jail system records
- `warnings` - User warning records

## Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
The bot includes Railway deployment configuration. Update the following in `railway.json`:
- `DISCORD_TOKEN` - Your production bot token
- Database connection settings
- Environment variables

## Monitoring & Maintenance

### Logs
- All bot activities are logged to the database
- Console logs provide real-time monitoring
- Log files are created in the `logs/` directory

### Database Management
- Use the admin commands to manage database records
- Regular backups recommended for production use
- Database migrations handled automatically by Alembic

### Performance
- Bot includes built-in performance monitoring
- Command execution times are tracked
- Memory and CPU usage monitoring available

## Troubleshooting

### Common Issues
1. **Bot doesn't respond to commands**
   - Check that the bot token is correct
   - Verify bot has proper permissions in the server
   - Check that commands are properly registered

2. **Database connection errors**
   - Ensure database file permissions are correct
   - Check database URL configuration
   - Verify SQLite is available

3. **Import errors**
   - Run `pip install -r requirements.txt`
   - Check Python version compatibility
   - Verify all dependencies are installed

### Debug Mode
Enable debug mode in `.env`:
```
DEBUG=true
LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the troubleshooting section
- Review the logs for error messages
- Test with the provided test script
- Check Discord.py documentation for API issues

---

**Happy botting!** 🤖✨
