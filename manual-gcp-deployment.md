# Manual GCP Deployment Instructions

Due to SSL certificate issues on your system, here's a manual approach to deploy your Gmail CLI project to GCP:

## Step 1: Install Google Cloud SDK Manually

1. **Download the Google Cloud SDK manually:**
   - Visit: https://cloud.google.com/sdk/docs/install
   - Download the macOS version for your architecture
   - Extract the tar.gz file
   - Run the installation script: `./google-cloud-sdk/install.sh`

2. **Alternative: Use the installer:**
   - Visit: https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.pkg
   - Download and run the PKG installer

## Step 2: Initialize Google Cloud SDK

```bash
# Initialize gcloud
gcloud init

# Authenticate
gcloud auth login

# Set your project (replace with your desired project ID)
export PROJECT_ID="gmail-client-$(date +%s)"
gcloud projects create $PROJECT_ID --name="Gmail Interactive Client"
gcloud config set project $PROJECT_ID

# Enable billing if needed (required for Compute Engine)
# You'll need to do this through the Google Cloud Console
```

## Step 3: Enable Required APIs

```bash
gcloud services enable compute.googleapis.com
gcloud services enable oslogin.googleapis.com
```

## Step 4: Create Firewall Rules

```bash
gcloud compute firewall-rules create allow-ssh \
    --allow tcp:22 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow SSH access"

gcloud compute firewall-rules create allow-http \
    --allow tcp:80,tcp:443,tcp:8080 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow HTTP/HTTPS access"
```

## Step 5: Create VM Instance

```bash
export INSTANCE_NAME="gmail-client-vm"
export ZONE="us-west1-b"
export MACHINE_TYPE="f1-micro"

gcloud compute instances create $INSTANCE_NAME \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=30GB \
    --boot-disk-type=pd-standard \
    --tags=http-server,https-server
```

## Step 6: Upload Your Application

```bash
# Create a tar file of your application
tar -czf gmail-client.tar.gz \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    *.py *.md *.txt *.sh gmail-client

# Upload to VM
gcloud compute scp gmail-client.tar.gz $INSTANCE_NAME:/tmp/ --zone=$ZONE
```

## Step 7: Setup Application on VM

```bash
# SSH into the VM
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE

# Once inside the VM, run these commands:
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv

# Create application directory
sudo mkdir -p /opt/gmail-client
cd /opt/gmail-client

# Extract application
sudo tar -xzf /tmp/gmail-client.tar.gz
sudo chown -R $USER:$USER /opt/gmail-client

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python3 -c "import nltk; nltk.download('wordnet', quiet=True); nltk.download('omw-1.4', quiet=True)"

# Make scripts executable
chmod +x gmail-client install.sh

# Test the application
python3 main.py
```

## Step 8: Running the Application

```bash
# To run the application:
cd /opt/gmail-client
source venv/bin/activate
python3 main.py
```

## Step 9: Managing the Instance

```bash
# Stop the instance (to save costs)
gcloud compute instances stop $INSTANCE_NAME --zone=$ZONE

# Start the instance
gcloud compute instances start $INSTANCE_NAME --zone=$ZONE

# Delete the instance
gcloud compute instances delete $INSTANCE_NAME --zone=$ZONE

# Delete the entire project
gcloud projects delete $PROJECT_ID
```

## Alternative: Docker Deployment

If you prefer using Docker on GCP:

1. **Build and push Docker image:**
```bash
# Build the Docker image
docker build -t gmail-client .

# Tag for Google Container Registry
docker tag gmail-client gcr.io/$PROJECT_ID/gmail-client

# Push to registry
docker push gcr.io/$PROJECT_ID/gmail-client
```

2. **Deploy to Google Cloud Run:**
```bash
gcloud run deploy gmail-client \
    --image gcr.io/$PROJECT_ID/gmail-client \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

## Security Notes

- Store Gmail credentials securely
- Use environment variables for sensitive data
- Consider using Google Secret Manager for credential storage
- Enable 2FA and use App Passwords for Gmail

## Troubleshooting

- If you encounter SSL issues, try updating your certificates
- For billing issues, ensure your GCP project is linked to a billing account
- For access issues, check your firewall rules and VM configuration

## Cost Optimization

- Use f1-micro instances (free tier eligible)
- Stop instances when not in use
- Use preemptible instances for development
- Monitor usage through Google Cloud Console
