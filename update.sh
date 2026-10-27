#!/usr/bin/env bash

# Exit immediately on error
set -e

# --- ANSI COLOR PALETTE ---
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${CYAN}=====================================================${NC}"
echo -e "${MAGENTA}${BOLD}   🚀 AeroMind-AI // Automated System Maintenance   ${NC}"
echo -e "${CYAN}=====================================================${NC}"

# 1. GIT REPOSITORY SYNC
if [ -d ".git" ]; then
    echo -e "${YELLOW}🔄 [*] Pulling upstream repository updates...${NC}"
    git pull origin main || git pull origin master
else
    echo -e "${RED}⚠️  [!] Warning: .git tree missing. Skipping pull.${NC}"
fi

# 2. PYTHON VENV & DEPENDENCIES
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}📦 [*] Synchronizing Python core environment...${NC}"
    if [ -d "venv" ]; then
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
else
    echo -e "${RED}⚠️  [!] Warning: requirements.txt not found.${NC}"
fi

# 3. DOCKER CONTAINER ORCHESTRATION
if [ -f "docker-compose.yml" ]; then
    echo -e "${YELLOW}🐳 [*] Purging active containers...${NC}"
    docker compose down --remove-orphans || true

    echo -e "${YELLOW}🔨 [*] Rebuilding container stack without cache...${NC}"
    docker compose build --no-cache

    echo -e "${GREEN}⚡ [*] Launching microservices...${NC}"
    docker compose up -d
else
    echo -e "${YELLOW}🐳 [*] Building standalone base Docker image...${NC}"
    docker build -t aeromind-ai:latest .
fi

# 4. SYSTEM DIAGNOSTICS & TELEMETRY
if [ -f "system_diagnostics.py" ]; then
    echo -e "${YELLOW}🩺 [*] Executing core pre-flight diagnostics...${NC}"
    python3 system_diagnostics.py
else
    echo -e "${RED}⚠️  [!] system_diagnostics.py omitted, skipping flight check.${NC}"
fi

echo -e "${CYAN}=====================================================${NC}"
echo -e "${GREEN}${BOLD}   ✨ AeroMind-AI System Fully Updated & Ready!      ${NC}"
echo -e "${CYAN}=====================================================${NC}"
