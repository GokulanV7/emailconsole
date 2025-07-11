#!/bin/bash

# Gmail Interactive Client - GCP CLI Deployment Script
# This script deploys your application to Google Cloud Platform using only CLI commands

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="gmail-client-$(date +%s)"  # Unique project ID
INSTANCE_NAME="gmail-client-vm"
ZONE="us-west1-b"  # Free tier eligible zone
MACHINE_TYPE="f1-micro"  # Free tier machine
IMAGE_FAMILY="ubuntu-2004-lts"
IMAGE_PROJECT="ubuntu-os-cloud"

echo -e "${BLUE}🚀 Gmail Interactive Client - GCP CLI Deployment${NC}"
echo -e "${BLUE}=================================================${NC}"

# Step 1: Check if gcloud is installed
echo -e "\n${YELLOW}📋 Step 1: Checking prerequisites...${NC}"
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Google Cloud SDK (gcloud) is not installed${NC}"
    echo -e "${YELLOW}💡 Install it from: https://cloud.google.com/sdk/docs/install${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Google Cloud SDK found${NC}"

# Step 2: Authenticate with Google Cloud
echo -e "\n${YELLOW}📋 Step 2: Authenticating with Google Cloud...${NC}"
echo -e "${BLUE}🔐 Opening browser for authentication...${NC}"
gcloud auth login

# Step 3: Create a new project
echo -e "\n${YELLOW}📋 Step 3: Creating GCP project...${NC}"
echo -e "${BLUE}📦 Project ID: ${PROJECT_ID}${NC}"
gcloud projects create $PROJECT_ID --name="Gmail Interactive Client"

# Set the project as active
gcloud config set project $PROJECT_ID

# Step 4: Enable required APIs
echo -e "\n${YELLOW}📋 Step 4: Enabling required APIs...${NC}"
gcloud services enable compute.googleapis.com
gcloud services enable oslogin.googleapis.com

# Step 5: Create firewall rules
echo -e "\n${YELLOW}📋 Step 5: Creating firewall rules...${NC}"
gcloud compute firewall-rules create allow-ssh \
    --allow tcp:22 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow SSH access"

gcloud compute firewall-rules create allow-http \
    --allow tcp:80,tcp:443,tcp:8080 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow HTTP/HTTPS access"

# Step 6: Create VM instance
echo -e "\n${YELLOW}📋 Step 6: Creating VM instance...${NC}"
echo -e "${BLUE}🖥️  Instance: ${INSTANCE_NAME}${NC}"
echo -e "${BLUE}🌍 Zone: ${ZONE}${NC}"
echo -e "${BLUE}⚙️  Machine: ${MACHINE_TYPE}${NC}"

gcloud compute instances create $INSTANCE_NAME \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --image-family=$IMAGE_FAMILY \
    --image-project=$IMAGE_PROJECT \
    --boot-disk-size=30GB \
    --boot-disk-type=pd-standard \
    --tags=http-server,https-server \
    --metadata-from-file startup-script=<(cat << 'EOF'
#!/bin/bash
# Startup script for Gmail Interactive Client

# Update system
apt-get update -y
apt-get upgrade -y

# Install Python and dependencies
apt-get install -y python3 python3-pip python3-venv git curl

# Create application directory
mkdir -p /opt/gmail-client
cd /opt/gmail-client

# Clone the repository (you'll need to update this URL)
# For now, we'll create the files directly
cat > /tmp/setup_app.sh << 'SETUP_EOF'
#!/bin/bash
cd /opt/gmail-client

# Create requirements.txt
cat > requirements.txt << 'REQ_EOF'
nltk==3.9.1
python-dateutil==2.9.0.post0
REQ_EOF

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python3 -c "import nltk; nltk.download('wordnet', quiet=True); nltk.download('omw-1.4', quiet=True)"

echo "✅ Gmail Interactive Client setup completed on GCP VM"
SETUP_EOF

chmod +x /tmp/setup_app.sh
/tmp/setup_app.sh

# Set ownership
chown -R $USER:$USER /opt/gmail-client
EOF
)

# Step 7: Wait for instance to be ready
echo -e "\n${YELLOW}📋 Step 7: Waiting for instance to be ready...${NC}"
echo -e "${BLUE}⏳ This may take a few minutes...${NC}"

# Wait for instance to be running
while [[ $(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format="value(status)") != "RUNNING" ]]; do
    echo -e "${YELLOW}⏳ Waiting for instance to start...${NC}"
    sleep 10
done

echo -e "${GREEN}✅ Instance is running!${NC}"

# Step 8: Get instance details
echo -e "\n${YELLOW}📋 Step 8: Instance details...${NC}"
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format="value(networkInterfaces[0].accessConfigs[0].natIP)")
INTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format="value(networkInterfaces[0].networkIP)")

echo -e "${GREEN}🌐 External IP: ${EXTERNAL_IP}${NC}"
echo -e "${GREEN}🏠 Internal IP: ${INTERNAL_IP}${NC}"

# Step 9: Upload application files
echo -e "\n${YELLOW}📋 Step 9: Uploading application files...${NC}"

# Create a tar of the application files
tar -czf /tmp/gmail-client.tar.gz \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    *.py *.md *.txt *.sh gmail-client 2>/dev/null || true

# Upload files to the instance
gcloud compute scp /tmp/gmail-client.tar.gz $INSTANCE_NAME:/tmp/ --zone=$ZONE

# Extract and setup on the instance
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="
    cd /opt/gmail-client
    sudo tar -xzf /tmp/gmail-client.tar.gz
    sudo chown -R \$USER:\$USER /opt/gmail-client
    chmod +x gmail-client install.sh 2>/dev/null || true
    source venv/bin/activate
    echo '✅ Application files uploaded and extracted'
"

# Step 10: Final setup and instructions
echo -e "\n${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${GREEN}=================================${NC}"
echo ""
echo -e "${YELLOW}📋 Connection Information:${NC}"
echo -e "${BLUE}Project ID: ${PROJECT_ID}${NC}"
echo -e "${BLUE}Instance Name: ${INSTANCE_NAME}${NC}"
echo -e "${BLUE}Zone: ${ZONE}${NC}"
echo -e "${BLUE}External IP: ${EXTERNAL_IP}${NC}"
echo ""
echo -e "${YELLOW}🔗 To connect to your instance:${NC}"
echo -e "${GREEN}gcloud compute ssh ${INSTANCE_NAME} --zone=${ZONE}${NC}"
echo ""
echo -e "${YELLOW}🚀 To run the Gmail client on the instance:${NC}"
echo -e "${GREEN}cd /opt/gmail-client${NC}"
echo -e "${GREEN}source venv/bin/activate${NC}"
echo -e "${GREEN}python main.py${NC}"
echo ""
echo -e "${YELLOW}💡 Quick connect command:${NC}"
echo -e "${GREEN}gcloud compute ssh ${INSTANCE_NAME} --zone=${ZONE} --command=\"cd /opt/gmail-client && source venv/bin/activate && python main.py\"${NC}"
echo ""
echo -e "${YELLOW}🛑 To stop the instance (save costs):${NC}"
echo -e "${GREEN}gcloud compute instances stop ${INSTANCE_NAME} --zone=${ZONE}${NC}"
echo ""
echo -e "${YELLOW}🗑️  To delete everything:${NC}"
echo -e "${GREEN}gcloud projects delete ${PROJECT_ID}${NC}"

# Save connection info to file
cat > gcp-connection-info.txt << EOF
GCP Gmail Client Deployment Information
=====================================

Project ID: ${PROJECT_ID}
Instance Name: ${INSTANCE_NAME}
Zone: ${ZONE}
External IP: ${EXTERNAL_IP}
Internal IP: ${INTERNAL_IP}

Connect: gcloud compute ssh ${INSTANCE_NAME} --zone=${ZONE}
Run App: cd /opt/gmail-client && source venv/bin/activate && python main.py
Stop: gcloud compute instances stop ${INSTANCE_NAME} --zone=${ZONE}
Start: gcloud compute instances start ${INSTANCE_NAME} --zone=${ZONE}
Delete: gcloud projects delete ${PROJECT_ID}

Generated on: $(date)
EOF

echo -e "${GREEN}💾 Connection details saved to: gcp-connection-info.txt${NC}"
