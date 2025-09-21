#!/usr/bin/env bash
# Bu dosya çalıştırılmak için değil, KOPYALA/YAPIŞTIR rehberi içindir.

# =========================
# WINDOWS POWERSHELL (PC)
# =========================
: <<'POWERSHELL'
$KEY="$env:USERPROFILE\.ssh\id_ed25519"

scp -i $KEY "F:\\aras_website_test\\aras_test_v16\\digitalocean_sunucu_ayarlari.sh"      root@104.248.46.180:/root/
scp -i $KEY "F:\\aras_website_test\\aras_test_v16\\digitalocean_veritabani_sifirla.sh"   root@104.248.46.180:/root/
scp -i $KEY "F:\\aras_website_test\\aras_test_v16\\digitalocean_deploy.sh"               root@104.248.46.180:/root/
POWERSHELL

# =========================
# SUNUCUDA (SSH ile bağlanınca)
# =========================
: <<'SERVER'
sudo apt update && sudo apt install -y dos2unix
sudo dos2unix ~/digitalocean_*.sh
chmod +x ~/digitalocean_*.sh

# Tam kurulum (SSH key gösterir ve Enter bekler)
sudo ~/digitalocean_sunucu_ayarlari.sh

# Kod güncelleme (deploy)
sudo ~/digitalocean_deploy.sh            # varsayılan mevcut branch
# veya belirli branch:
# sudo ~/digitalocean_deploy.sh main

# YIKICI: Veritabanını sıfırla + superuser oluştur
sudo DB_RESET=1 ~/digitalocean_veritabani_sifirla.sh
SERVER
