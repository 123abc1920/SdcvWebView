if [ "$EUID" -ne 0 ]; then
  echo "Please run the script with sudo: sudo ./install.sh"
  exit 1
fi

SCRIPT_DIR=$(pwd)
BACKEND_DIR="$SCRIPT_DIR/backend"
CURRENT_USER=$SUDO_USER

if [ -z "$CURRENT_USER" ]; then
    CURRENT_USER="root"
fi

echo "==========================="
echo "SDCV Web UI Server Setup..."
echo "==========================="

echo "Checking and installing system packages..."
if [ -f /etc/debian_version ]; then
    apt update && apt install -y python3-pip python3-venv python3-dev
elif [ -f /etc/redhat-release ]; then
    dnf install -y python3-pip python3-devel
fi

echo "Creating an isolated Python environment..."
cd "$BACKEND_DIR" || exit
sudo -u "$CURRENT_USER" python3 -m venv venv
sudo -u "$CURRENT_USER" ./venv/bin/pip install --upgrade pip
sudo -u "$CURRENT_USER" ./venv/bin/pip install -r requirements.txt
sudo -u "$CURRENT_USER" ./venv/bin/pip install waitress

echo "Creating a systemd service..."
SERVICE_FILE="/etc/systemd/system/sdcv_web_ui.service"

cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=SDCV Web UI Self-Hosted Service
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$BACKEND_DIR
ExecStart=$BACKEND_DIR/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "Starting the service..."
systemctl daemon-reload
systemctl enable sdcv_web_ui.service
systemctl start sdcv_web_ui.service

echo "=================================================="
echo "INSTALLATION COMPLETED SUCCESSFULLY!"
echo "The program runs in the background as a system service."
echo "Interface address: http://127.0.0.1:5200"
echo "=================================================="
echo "The service can be controlled using commands:"
echo "  sudo systemctl stop sdcv_web_ui"
echo "  sudo systemctl start sdcv_web_ui"
echo "  sudo systemctl restart sdcv_web_ui"
echo "=================================================="
