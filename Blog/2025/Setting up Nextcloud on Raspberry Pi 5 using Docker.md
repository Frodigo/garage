---
date: 2025-09-24
title: Setting up Nextcloud on Raspberry Pi 5 using Docker
---
My goal was simple – to move photos from Google Photos and Apple Photos "to my own server." I decided to try NextCloud and installed it using NextCloudPI, a custom-built distribution for Raspberry Pi.

I purchased a brand new Raspberry Pi 5, a cooler, and an external USB drive. I also needed to run an Ethernet cable to my ~~office~~ garage, which I should have done a long time ago anyway.
## NextCloudPi. It should work, but it shouldn't work for me

My initial attempts to launch NextCloud were unsuccessful. I couldn't even get past the first launch. Here are the errors I encountered:

```bash
[FAILED] failed to start avahi-deamon.service - Avahi mDNS/DNS-SD stack
run `systemctl status avahi-daemon.service` for details

[FAILED] failed to start systemd-logind.service - User login management

[failed] failed to start bluetooth.service -

[failed] failed to start udisk2.service - disk manager

[failed] failed to start dbus.service - D-Bus System message bus
```

I tried to fix them, but I couldn't even log in because the system never finished the first boot. It was frustrating. At least as frustrating as Dembele winning the Ballon d'Or (okay, a little less so).

Imagine that even a restart didn't help. Nor did turning it off and on. Interestingly, I downloaded an older version of NextCloudPi, but I still had no success. I tried two versions: v1.55.3 and v1.55.2.

It's open-source software, developed by the community. No one said it would work, and I don't blame anyone for it not working. Perhaps there was something wrong with my configuration. I didn't pursue the issue further; I just tried a different approach.
## NextCloud on Docker. It must work

I did a small research and I have found this guide:  [https://help.nextcloud.com/t/guide-setting-up-nextcloud-on-raspberry-pi-ssl-advanced-app-support-high-performance-postgresql-and-cloudflare-zero-trust-integration/185757](https://help.nextcloud.com/t/guide-setting-up-nextcloud-on-raspberry-pi-ssl-advanced-app-support-high-performance-postgresql-and-cloudflare-zero-trust-integration/185757]). It was good as a starting point.

But it couldn't just work, right?
### "Data Directory Invalid" Error

I initially ran NextCloud on an SD card, but ultimately wanted to store the data on an external SSD. I achieved this by setting the `datadirectory` as a Docker volume, mounted on an external drive.

```bash
/media/frodigo/nextcloud-data:/var/www/html/data:z
```

After restarting NextCloud I saw this error:

```bash
Data directory is invalid.
Make sure there is a file called ".ncdata" in the root of the data directory.
The data directory is not writable.
```

I did a research and I have realized that Nextcloud requires a specific marker file `.ncdata` in the data directory root to validate the directory structure.

I checked if the file exist, and It didn't exist so I created a new one:

```bash
# Check if the file exists
ls -la /media/frodigo/nextcloud-data/.ncdata

# Create if missing
echo "# Nextcloud data directory" > /media/frodigo/nextcloud-data/.ncdata

```

However, that didn't completely resolve the issue. I moved forward a bit, but then saw another error saying that the data directory is not writable.
### User ID Mismatches

Initially, I set permissions on the data directory so that the `www-data` user could access it. To my surprise, it turned out that the `www-data` user ID on the host was different from the `www-data` user ID in the container, which is why I was experiencing problems.

- Host system `www-data` user: UID 33
- Container `www-data` user: UID 82

The solution for this problem was to align file ownership with the container's expectations:

```bash
# Check what UID www-data has inside the container
docker exec -it nextcloud id www-data

# Set ownership to match container UID
sudo chown -R 82:82 /path/to/nextcloud-data/
sudo chmod -R 755 /path/to/nextcloud-data/

```

#### Troubleshooting workflow

When facing data directory issues:

1. **Verify the external drive is mounted**: `df -h`
2. **Check Docker volume mappings**: Review your `docker-compose.yml`
3. **Inspect file permissions**: `ls -la /path/to/data/`
4. **Check container user IDs**: `docker exec -it container_name id www-data`
5. **Verify .ncdata file exists and is readable**
6. **Restart containers after making changes**: `docker-compose down && docker-compose up -d`
7. **Debug container user context**: `docker-compose exec -u www-data nextcloud touch /var/www/html/data/test.txt`

Note: Docker introduces multiple abstraction layers that can mask the root cause of issues. The key to successful troubleshooting is understanding these layers and testing each one systematically. Always verify your assumptions at each level:

- network connectivity
- volume mounting
- file permissions,
- application configuration

## It works. Somehow

After overcoming these setbacks, my NextCloud on Pi started working, but it seems this is more the beginning of an adventure than the end. The rest of my adventures might come in the near future, if I don't give up. We'll see.

---
*Published: 24/09/2025* #blog #nectcloud #raspberrypi #diy #cloud #docker
