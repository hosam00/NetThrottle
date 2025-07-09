#!/bin/bash

# Network Speed Controller Launcher

cd "$(dirname "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Modern banner
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                ${GREEN}⚡ Network Speed Controller${BLUE}                  ║${NC}"
echo -e "${BLUE}║              ${YELLOW}Modern Responsive GUI Edition${BLUE}                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check screen size and recommend
echo -e "${BLUE}📱 Responsive Design: Adapts to your screen size automatically${NC}"
echo ""

# Check if running with sudo
if [ "$EUID" -eq 0 ]; then
    echo -e "${GREEN}✅ Running with sudo privileges - full functionality available${NC}"
else
    echo -e "${YELLOW}⚠️  Running without sudo - some features may be limited${NC}"
    echo -e "${YELLOW}   For full functionality, run: sudo ./run.sh${NC}"
fi

echo ""
echo -e "${BLUE}🚀 Starting application...${NC}"
echo ""

python3 main.py

echo ""
echo -e "${GREEN}✨ Application closed successfully${NC}"
