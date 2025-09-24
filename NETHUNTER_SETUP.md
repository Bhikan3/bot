# 🗡️ NetHunter Kali Linux Setup Guide for Traffic Bot

## 📱 **NetHunter Requirements:**

### **System Requirements:**
- NetHunter Kali Linux installed on Android device
- Root access
- At least 2GB RAM (4GB recommended)
- 5GB free storage space

### **Supported Devices:**
- OnePlus devices
- Nexus/Pixel devices  
- Samsung Galaxy (with custom kernels)
- Any rooted Android with NetHunter support

## 🛠️ **Installation Steps:**

### **1. Update NetHunter System**
```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install python3 python3-pip wget curl git -y
```

### **2. Install Chrome/Chromium Browser**
```bash
# Install Chromium (lighter than Chrome)
sudo apt install chromium-browser -y

# OR install Google Chrome (if available)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable -y
```

### **3. Install Python Dependencies**
```bash
# Install required Python packages
pip3 install selenium pandas matplotlib

# Install ChromeDriver
sudo apt install chromium-chromedriver -y

# OR download manually
wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE
LATEST=$(cat LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

### **4. Setup Traffic Bot**
```bash
# Create directory
mkdir -p /sdcard/traffic_bot
cd /sdcard/traffic_bot

# Copy main.py to this directory
# Enable NetHunter mode in script
```

### **5. Configure Script for NetHunter**
```python
# In main.py, set these to True:
ENABLE_NETHUNTER_MODE = True
ENABLE_LOW_RESOURCE_MODE = True
HEADLESS_MODE = True
BATCH_SIZE = 5  # Start with small batch
```

## 🚀 **Running the Bot:**

### **Method 1: Direct Python**
```bash
cd /sdcard/traffic_bot
python3 main.py
```

### **Method 2: Background Execution**
```bash
# Run in background
nohup python3 main.py > traffic.log 2>&1 &

# Check if running
ps aux | grep python3

# Kill if needed
pkill -f main.py
```

### **Method 3: Using Screen (Recommended)**
```bash
# Install screen
sudo apt install screen -y

# Start screen session
screen -S traffic_bot

# Run script
python3 main.py

# Detach: Ctrl+A, then D
# Reattach: screen -r traffic_bot
```

## ⚡ **Performance Optimization:**

### **1. Memory Management**
```bash
# Check memory usage
free -h

# Clear cache if needed
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```

### **2. CPU Management**
```bash
# Check CPU usage
htop

# Limit CPU for Chrome (if needed)
# Use cpulimit tool
```

### **3. Battery Optimization**
- Keep device plugged in
- Disable unnecessary apps
- Use airplane mode + WiFi only
- Lower screen brightness

## 🐛 **Troubleshooting:**

### **Chrome Issues:**
```bash
# If Chrome crashes
export DISPLAY=:0
Xvfb :0 -screen 0 1024x768x16 &

# Check Chrome installation
which google-chrome || which chromium-browser

# Test Chrome headless
google-chrome --headless --no-sandbox --dump-dom https://google.com
```

### **Python Issues:**
```bash
# Install missing dependencies
pip3 install --upgrade selenium pandas

# Check Python version (needs 3.6+)
python3 --version
```

### **Permission Issues:**
```bash
# Fix permissions
chmod +x main.py
chown $(whoami):$(whoami) -R /sdcard/traffic_bot/
```

### **Memory Issues:**
```bash
# Enable swap (if not exists)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 📊 **NetHunter Optimized Settings:**

```python
# Recommended configuration for NetHunter:
TOTAL_VISITS = 500          # Reduce for mobile
BATCH_SIZE = 5              # Small batch size
DELAY_BETWEEN_BATCHES = 2.0 # More delay
HEADLESS_MODE = True        # Always headless
ENABLE_MOBILE_FOCUS = True  # 90% mobile traffic
ENABLE_LOW_RESOURCE_MODE = True
```

## 🔧 **Advanced Tips:**

### **1. Multiple Concurrent Instances:**
```bash
# Run multiple instances with different configs
screen -S traffic_bot_1
screen -S traffic_bot_2
screen -S traffic_bot_3
```

### **2. Automated Scheduling:**
```bash
# Add to crontab for automated runs
crontab -e

# Run every hour
0 * * * * cd /sdcard/traffic_bot && python3 main.py
```

### **3. Remote Monitoring:**
```bash
# SSH into device for remote monitoring
# Enable SSH in NetHunter settings first
ssh kali@<device_ip>
```

## ⚠️ **Important Notes:**

1. **Device Heat**: Monitor device temperature
2. **Data Usage**: Use WiFi to avoid mobile data charges
3. **Detection Risk**: Use reasonable delays and limits
4. **Legal Usage**: Only use on websites you own or have permission
5. **Backup**: Keep backups of working configurations

## 🆘 **Support Commands:**

```bash
# System info
uname -a
cat /proc/version
cat /proc/meminfo

# Network check
ping -c 4 google.com
wget --spider --quiet https://www.myntra.com

# Chrome test
google-chrome --version
chromium-browser --version
```

---

**Happy NetHunter Traffic Generation! 🗡️📱**
