# Hexlore VPS Bot - Advanced Discord VPS Hosting Bot

![Discord.py](https://img.shields.io/badge/discord.py-2.0+-blue)
![Python](https://img.shields.io/badge/Python-3.12+-green)
![Docker](https://img.shields.io/badge/Docker-Latest-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A highly advanced, production-ready Discord bot for automated VPS/container deployment, management, monitoring, and billing. Features a modern scalable architecture with 90+ integrated systems.

## 🚀 Features Overview

### User VPS Features (40 systems)
- ✅ Full Docker container lifecycle management
- ✅ Resource monitoring (RAM, CPU, Disk, Network)
- ✅ Automated backups and snapshot system
- ✅ Port management and SSH access
- ✅ Multiple OS templates (Ubuntu, Debian, Alpine)
- ✅ Pre-configured application templates
- ✅ Activity logs and bandwidth tracking
- ✅ Auto-suspension of inactive VPS

### Admin Features (20 systems)
- ✅ Comprehensive admin dashboard
- ✅ User and VPS management
- ✅ Blacklist/Whitelist system
- ✅ Global statistics and monitoring
- ✅ Node management and health checks
- ✅ Broadcast and maintenance mode
- ✅ Audit logging and IP tracking

### Security Features (10 systems)
- ✅ Anti-abuse and rate limiting
- ✅ Container isolation and escape prevention
- ✅ Secure token encryption
- ✅ Session validation and API keys
- ✅ Owner-only critical commands
- ✅ Input validation and SQL injection prevention

### Premium & Automation Features (20 systems)
- ✅ Subscription and plan system
- ✅ Redeem code system
- ✅ Automated resource balancing
- ✅ Scheduled backups and health checks
- ✅ Auto-restart crashed containers
- ✅ Invoice generation
- ✅ Multi-node support

## 📋 Requirements

- **Python:** 3.12+
- **Discord Library:** discord.py
- **Database:** MongoDB 4.0+
- **Container System:** Docker Engine (20.10+)
- **OS:** Linux (Ubuntu 20.04+ recommended)
- **RAM:** 4GB minimum for bot + containers
- **Disk:** 20GB+ for container storage

## 📦 Installation

### Prerequisites

1. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Install MongoDB**
   ```bash
   # Using Docker (Recommended)
   docker run -d --name mongodb -p 27017:27017 -v mongodb_data:/data/db mongo:latest
   
   # Or native installation
   wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
   echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
   sudo apt-get update
   sudo apt-get install -y mongodb-org
   ```

3. **Install Python 3.12+**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3.12 python3.12-venv python3.12-dev
   ```

### Setup Bot

1. **Clone Repository**
   ```bash
   git clone https://github.com/arvexhosting75-lang/Hexlore-vps-bot.git
   cd Hexlore-vps-bot
   ```

2. **Create Virtual Environment**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   nano .env
   ```

5. **Run Bot**
   ```bash
   python bot.py
   ```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Discord Bot
DISCORD_TOKEN=your_bot_token_here
COMMAND_PREFIX=!
OWNER_ID=your_discord_id

# MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=hexlore_vps

# Docker
DOCKER_SOCKET=/var/run/docker.sock
DOCKER_REGISTRY=docker.io

# API
API_PORT=8000
API_HOST=0.0.0.0
API_KEY_LENGTH=32

# Security
ENCRYPTION_KEY=your_encryption_key_here
SESSION_TIMEOUT=3600
RATE_LIMIT_CALLS=10
RATE_LIMIT_PERIOD=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log

# Features
ENABLE_PREMIUM=true
ENABLE_BILLING=true
MAX_VPS_PER_USER=5

# Nodes
DEFAULT_NODE_HOST=localhost
DEFAULT_NODE_PORT=2375
```

## 🏗️ Project Structure

```
Hexlore-vps-bot/
├── bot.py                      # Main bot entry point
├── config.py                   # Configuration and settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
│
├── database/
│   ├── __init__.py
│   ├── models.py              # MongoDB models and schemas
│   ├── connection.py          # Database connection manager
│   └── queries.py             # Database query helpers
│
├── cogs/                       # Discord command extensions
│   ├── __init__.py
│   ├── vps_management.py      # VPS CRUD operations
│   ├── vps_monitoring.py      # Resource monitoring
│   ├── backup_system.py       # Backup and restore
│   ├── admin_panel.py         # Admin commands
│   ├── billing_system.py      # Premium and billing
│   ├── user_management.py     # User operations
│   └── events.py              # Discord events
│
├── docker_manager/
│   ├── __init__.py
│   ├── engine.py              # Docker SDK wrapper
│   ├── container.py           # Container operations
│   ├── network.py             # Network management
│   ├── images.py              # Image management
│   └── ports.py               # Port allocation
│
├── utils/
│   ├── __init__.py
│   ├── logger.py              # Logging system
│   ├── security.py            # Security functions
│   ├── validators.py          # Input validation
│   ├── encryption.py          # Data encryption
│   ├── decorators.py          # Custom decorators
│   └── helpers.py             # Helper functions
│
├── panels/
│   ├── __init__.py
│   ├── embeds.py              # Embed generators
│   ├── buttons.py             # Button components
│   ├── modals.py              # Modal forms
│   └── views.py               # View handlers
│
├── api/
│   ├── __init__.py
│   ├── server.py              # API server
│   ├── routes.py              # API routes
│   ├── auth.py                # API authentication
│   └── websocket.py           # WebSocket support
│
├── backups/
│   └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── systemd/
│   └── hexlore-vps-bot.service  # Systemd service file
│
└── docs/
    ├── INSTALLATION.md
    ├── CONFIGURATION.md
    ├── API_DOCUMENTATION.md
    └── TROUBLESHOOTING.md
```

## 🔧 Slash Commands

### User Commands
- `/create` - Create a new VPS
- `/delete` - Delete a VPS
- `/restart` - Restart VPS
- `/start` - Start VPS
- `/stop` - Stop VPS
- `/panel` - View VPS dashboard
- `/backup` - Backup management
- `/restore` - Restore from backup
- `/stats` - View resource statistics
- `/console` - Access container console
- `/plans` - View available plans
- `/activity` - View activity logs
- `/userinfo` - User information

### Admin Commands
- `/admin` - Admin dashboard
- `/suspend` - Suspend user VPS
- `/unsuspend` - Unsuspend user VPS
- `/nodes` - Node management

## 🔐 Security

- **Container Isolation:** Each VPS runs in isolated Docker containers
- **Network Isolation:** Containers connected to isolated networks
- **Volume Encryption:** Sensitive data encrypted at rest
- **Token Encryption:** API keys and sessions encrypted
- **Rate Limiting:** Built-in rate limiting on all endpoints
- **Input Validation:** Comprehensive input sanitization
- **Audit Logging:** All actions logged with timestamps and user IDs
- **Permission Checks:** Role-based access control

## 📊 Database Collections

- `users` - User profiles and account data
- `containers` - VPS container information
- `plans` - Hosting plan definitions
- `nodes` - Docker node configurations
- `logs` - Activity and audit logs
- `backups` - Backup metadata
- `billing` - Billing and subscription data
- `sessions` - Active user sessions
- `blacklists` - Banned users and IPs

## 🚀 Deployment

### Using Systemd

```bash
sudo cp systemd/hexlore-vps-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hexlore-vps-bot
sudo systemctl start hexlore-vps-bot
sudo systemctl status hexlore-vps-bot
```

### Using Docker

```bash
docker build -t hexlore-vps-bot .
docker run -d --name hexlore-bot \
  -e DISCORD_TOKEN=your_token \
  -e MONGO_URI=mongodb://mongo:27017 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  hexlore-vps-bot
```

## 📖 Documentation

Detailed documentation available in `/docs` directory:
- [Installation Guide](docs/INSTALLATION.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🐛 Troubleshooting

### Bot Won't Start
- Check Discord token is valid
- Verify MongoDB connection
- Check Docker daemon is running: `sudo systemctl status docker`

### Container Creation Fails
- Ensure Docker socket has correct permissions: `sudo chmod 666 /var/run/docker.sock`
- Check available disk space: `df -h`
- Verify Docker images are available: `docker images`

### Permission Denied Errors
- Add user to docker group: `sudo usermod -aG docker $USER`
- Log out and back in for changes to take effect

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please fork repository and submit pull requests.

## 💬 Support

For support, open an issue on GitHub or contact the maintainer.

## ⭐ Credits

Built with [discord.py](https://github.com/Rapptz/discord.py), [Docker SDK](https://github.com/docker/docker-py), and [PyMongo](https://github.com/mongodb/mongo-python-driver)
