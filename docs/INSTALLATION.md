# Installation Guide - Hexlore VPS Bot

## Prerequisites

Before installing Hexlore VPS Bot, ensure you have:

- **Linux Server** (Ubuntu 20.04+ or Debian 11+)
- **Python 3.12+**
- **Docker Engine** (Latest)
- **MongoDB 4.0+**
- **4GB+ RAM**
- **20GB+ Disk Space**
- **Discord Bot Token** (from Discord Developer Portal)

## Step 1: System Setup

### Install Docker

```bash
# Download Docker installation script
curl -fsSL https://get.docker.com -o get-docker.sh

# Run installation
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
```

### Install MongoDB

**Option A: Using Docker (Recommended)**

```bash
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:latest

# Verify
docker ps | grep mongodb
```

**Option B: Native Installation (Ubuntu/Debian)**

```bash
# Add MongoDB repository
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify
mongosh
```

### Install Python 3.12

```bash
# Update package manager
sudo apt-get update

# Install Python 3.12
sudo apt-get install -y python3.12 python3.12-venv python3.12-dev

# Verify
python3.12 --version
```

## Step 2: Clone Repository

```bash
# Clone the repository
git clone https://github.com/arvexhosting75-lang/Hexlore-vps-bot.git
cd Hexlore-vps-bot

# Or if using SSH
git clone git@github.com:arvexhosting75-lang/Hexlore-vps-bot.git
cd Hexlore-vps-bot
```

## Step 3: Create Virtual Environment

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show (venv) prefix)
which python
```

## Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

## Step 5: Configuration

### Create Environment File

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration
nano .env
```

### Required Configuration

```env
# Discord Bot
DISCORD_TOKEN=your_bot_token_here
OWNER_ID=your_discord_id_here

# Database
MONGO_URI=mongodb://localhost:27017

# Security
ENCRYPTION_KEY=your_encryption_key_here
```

#### Generate Encryption Key

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Step 6: Test Installation

```bash
# Activate virtual environment (if not already)
source venv/bin/activate

# Run bot
python bot.py

# You should see:
# [INFO] Starting Hexlore VPS Bot...
# [INFO] Connecting to MongoDB...
# [INFO] ✓ Database connected successfully
# [INFO] Initializing Docker engine...
# [INFO] ✓ Docker engine initialized successfully
# [INFO] Bot logged in as [BotName]#XXXX
```

## Step 7: Deploy as System Service (Optional)

### Create Bot User

```bash
sudo useradd -r -s /bin/bash vpsbot
sudo mkdir -p /opt/hexlore-vps-bot
sudo chown -R vpsbot:vpsbot /opt/hexlore-vps-bot
```

### Move Files

```bash
sudo cp -r Hexlore-vps-bot/* /opt/hexlore-vps-bot/
sudo chown -R vpsbot:vpsbot /opt/hexlore-vps-bot
sudo chmod -R 755 /opt/hexlore-vps-bot
```

### Install Systemd Service

```bash
sudo cp systemd/hexlore-vps-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hexlore-vps-bot
sudo systemctl start hexlore-vps-bot
sudo systemctl status hexlore-vps-bot
```

### View Logs

```bash
# Real-time logs
sudo journalctl -u hexlore-vps-bot -f

# Last 50 lines
sudo journalctl -u hexlore-vps-bot -n 50
```

## Troubleshooting

### Docker Socket Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Or manually set permissions
sudo chmod 666 /var/run/docker.sock
```

### MongoDB Connection Failed

```bash
# Check if MongoDB is running
docker ps | grep mongodb
# or
sudo systemctl status mongod

# Verify connection
mongosh --uri "mongodb://localhost:27017"
```

### Bot Won't Start

```bash
# Check Discord token
echo $DISCORD_TOKEN

# Run with debug logging
export LOG_LEVEL=DEBUG
python bot.py

# Check for Python errors
python -m py_compile bot.py
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

## Next Steps

1. Read the [Configuration Guide](CONFIGURATION.md)
2. Review [API Documentation](API_DOCUMENTATION.md)
3. Check [Troubleshooting Guide](TROUBLESHOOTING.md)
4. Invite bot to Discord server
5. Test bot commands
