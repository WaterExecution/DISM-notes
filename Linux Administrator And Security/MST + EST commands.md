# User Management
## Users & Groups
```
useradd
groupadd 
id
groups
passwd
usermod –aG <group> <user>
chgrp <group> <user>
su 
sudo su
```

## File Permissions

```
chown <user> <file>
chmod 777 test.txt
```

## Perms
SGID -> created files will be owned by SGID group

## Sudo (/etc/sudoers)
```
# Give all sudo perms
user ALL=ALL

# Disable root login
nano /etc/passwd
root:x:0:0:root:/root:/sbin/nologin	
```

# Networking
## Configure
```
nmtui 
nmcli networking off  
nmcli networking on   
```

## Show networking information
```
ip a
cat /etc/resolv.conf
route -n
netstat -apetul
netstat -plant
ss -l
ss -ta
ss -tp
```


# Transfering file
```
Remote to Local:
scp <user>@<ip>:/<file> <destination>
Example:
scp user@10.10.10.10:/home/user/test.txt .

Local to Remote:
scp <file> <user>@<ip>:<destination>
Example:
scp file.txt user@10.10.10.10:/remote/directory
```
```
sftp <ip>
```
# Editing files
```
echo "test" > file.txt
echo "test" >> file.txt
nano
vi # :wq! to exit
```
# Scripting
```bash
for i in {1..10};do echo user$i;done
find / -name "*.bak" -type f -print | xargs /bin/rm -f
```

# Security
## SELinux (Policy)
>Enforcing - action is prohibited and logged
>Permissive - action logged
>Disabled
```
getenforce

/etc/sysconfig/selinux -> SELINUX=disabled
setenforce 0 #permissive
setenforce 1 #enforcing
```



## SELinux Context
```
ls -Z <file>
# Display SElinux credentials
ls -lZ

# Change context of file
chcon -t public_content <file>

# restore original context
restorecon <file>
```

## Kernel (/etc/sysctl.conf)
```
# show all kernel parameter
sysctl -a

# load settings from .conf
sysctl -p

# ignore ipv4 ping
sysctl –w net.ipv4.icmp_echo_ignore_all=1
```

## Mounting Grub to reset password
> Reset password
```
Press 'e' when booting up
Add rd.break between linux and initrd (end of linux)
Ctrl-x
mount -o remount,rw /sysroot
chroot /sysroot
passwd
/.autorelabel
touch /.autorelabel
exit
init 6
```
> Password protecting the GRUB in order to prevent unauthenticated password reset
> Hash stored in /boot/grub2/user.cfg
```
grub2-setpassword
```


# Packages
## Installer
```
yum
dnf
rpm #installer for .rpm
```
## Client
```
ftp
nmap
firewall-config
policycoreutils-gui #system-config-selinux
```
## Services
```
vsftpd
openssh-server
cockpit
httpd
mod_ssl
squid
nfs-utils
samba
samba-client
```
# Services & applications
```
<service name> - ssh, ftp
<action> - restart, start, stop, enable
service <service name> <action>
systemctl <action> <service name>

# display services
systemctl list-unit-files --type service
```

# FTP (/etc/vsftpd/vsftpd.conf)
> Default folder path: /var/ftp/pub
> ftpd_banner //Enable to prevent Information Disclosure!
> banner_file 
> anonymous_enable //Disable!
> anon_upload_enable //Disable!
> local_enable
> write_enable

## Allow anonymous upload for FTP
```
/etc/vsftpd/vsftpd.conf

anon_upload_enable=YES
write_enable=YES
setsebool -P allow_ftpd_anon_write True
setsebool -P allow_ftpd_full_access True

setsebool -P allow_ftpd_anon_write=1
setsebool -P allow_ftpd_full_access=1
```

## Firewall
```
firewall-cmd --permanent --zone=public --add-service=ftp
firewall-cmd --reload
firewall-cmd --list-all
```

## Chroot (vsftpd.conf)
>chroot_local_user //Enable chroot
>chroot_list_enable //Exempted from jail
>chroot_list_file //list of users to exempt chroot
>allow_writeable_chroot // allows chroot user to write in their home directory
>passwd_chroot_enable // jail the account in the FTP to the /home directory based on the /etc/passwd. Unable to go to any other directories. 
```
chroot_local_user=YES 
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd/chroot_list
allow_writeable_chroot=YES
passwd_chroot_enable=YES
```
```
If:
chroot_local_user=NO
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd/chroot_list
User in chroot_list will be chroot jailed
```
# SSH (/etc/ssh/sshd_config)
## SELinux
```
semanage port -a -t ssh_port_t -p tcp 8222
```
## Firewall
```
firewall-cmd --zone=public --permanent --add-port=8222/tcp
firewall-cmd --reload
firewall-cmd --list-all
```

# Cockpit
```
systemctl enable --now cockpit.socket
systemctl start cockpit
```
```
firewall-cmd --add-service=cockpit --permanent
firewall-cmd --reload
```


# Apache (/etc/httpd/conf/httpd.conf)
## Firewall
```
firewall-cmd --permanent --zone=public --add-service=http
firewall-cmd --reload
firewall-cmd --list-all
```
>Set file to open when going to IP
```bash
DocumentRoot "/var/www/html"
DirectoryIndex index.html
```
>Show server-status (Recommended for localhost only)
>Change localhost to ip address or all accordingly
```
<Location /server-status>
 SetHandler server-status
 Order allow,deny
 Allow from localhost
</Location>
```
> Performance
```
StartServers 5 # Nodes
ThreadsPerChild 15 # Threads
ServerLimit 10
```
> Logs
```
tail /var/log/httpd/access_log
tail /var/log/httpd/error_log
```
>Set directory as page (Put in /etc/httpd/conf.d/\<name>.conf or default area)
```
<Directory /var/www/html/directory>
    Options -Indexes
</Directory>
```
```
<Directory /var/www/html/directory>
    Options -Indexes
    Require all denied
    Require ip x.x.x.x
    Require local
</Directory>
```
# Generate SSL Certs
>For Private key: /etc/pki/tls/private/
>For Certificate: /etc/pki/tls/certs/
```
openssl req -newkey rsa:2048 -nodes -keyout /etc/pki/tls/private/localhost.key -x509 -days 365 -out /etc/pki/tls/certs/localhost.crt
```
> Certification info
```
SG
Singapore
Dover
DISM
LAS
server.example.com
las@example.com
```
![](https://i.imgur.com/ReVLVbj.png)

# Vhost
## Configure VHost Client & Server (/etc/hosts)
```
10.10.10.10 www.domain.com admin.domain.com domain.com
```
    
## Vhost Apache (Put in /etc/httpd/conf.d/\<name>.conf or default area)
```
<VirtualHost 127.0.0.1:8080>
 ServerName www.domain.com
 DocumentRoot /var/www/<name>
 ErrorLog /var/log/httpd/<name>-error_log
 CustomLog /var/log/httpd/<name>-access_log combined
</VirtualHost>
```
    
# Htpasswd
```
htpasswd -c -B /etc/httpd/conf/<file> <user> // -c create -B Bcrypt
```
>AuthName - Description/message
>Require user - Users allowed to log in to the webpage
```
<Directory /var/www/html/directory>
    Options -Indexes
    AuthType basic
    AuthName "Website"
    AuthUserFile /etc/httpd/conf/<name>
    Require user <user> <user> <user> 
</Directory>
```
>AllowOverride - Prioritize (AuthConfig) authtype authname authuserfile
```
<Directory /var/www/html/directory>
    Options -Indexes
    AuthType basic
    AuthName "Website"
    AuthUserFile /etc/httpd/conf/<name>
    Require user <user> <user> <user> 
    AllowOverride AuthConfig
</Directory>
```
> view all http traffic
```
grep TUNNEL /var/log/squid/access.log
```
# Squid (/etc/squid/squid.conf)
```bash
#Enable/Disable sites add to /etc/squid/squid.conf
acl <name> src 192.168.30.0/24
acl <name> dstdomain .myspecies.info
acl <name> dstdomain .org

#Beware of priority of the allows and denies
http_access allow LAS_net
http_access deny bad_sites
```
```
firewall-cmd --add-port=3128/tcp
firewall-cmd --reload
firewall-cmd --list-all
```
## Foxyproxy
```
https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/
```

## Log
```
/var/log/squid/access.log
```
```bash
#All about cache
#cache_dir ufs /var/spool/squid 100 16 256
ufs is file system
stores up to 100m
sub-directory of 16
sub-sub-directory of 256

TCP_MISS/304 means it's using the browser cache
Disable browser.cache.disk.enable
Clear browser cache
Browser cache > Squid cache
*Squid cache is used for service like FTP since they don't have caching like browsers.
```

# WSGI (Extra)
```bash
WSGI to work as a proxy between apache/nginx and web frameworks (flask,jinja)

WSGIScriptAlias /test_wsgi /var/www/las_wsgi/test_wsgi.py //maps web directory to script

jmeter to test response speed
```

# Partitions
>Boot partition //Linux OS
>Swap //Paging Memory
```
lshw -class disk
fdisk -l /dev/nvme0n1
```
# Formatting and Mounting
```
fdisk -l
pvcreate /dev/nvme0n2
vgcreate vg_xfs /dev/nvme0n2
lvcreate -L +1020M -n lv_anyname vg_xfs
lvdisplay /dev/vg_xfs/lv_anyname
mkfs -t xfs /dev/vg_xfs/lv_anyname
mount /dev/vg_xfs/lv_anyname /filesys1 //temp
blkid /dev/vg_xf/lv_anyname
```

# /etc/exports
```
ro/rw
sync/async //sync - commit then save, async - auto sync
root_squash/no_root_squash // user can impersonate as root to as file system if no_root_squash is enable, user will stay as root

exportfs // restart
```
```
mkdir -p /exports/data
chmod 777 /exports/data
/exports/data <remote ip>(ro,sync) #if got space <ip> \( then it's *

exportfs -r
exportfs -v
service nfs-server start
```
## Client
```
mount <ip>:/exports/data /mount/data -o rw
```
## Firewall
```
firewall-cmd --permanent --zone=public --add-service=nfs
firewall-cmd --reload
firewall-cmd --list-all
```

# /etc/fstab
```
noexec //remove execute bit but user can still run "bash script.sh" to run 
nodev // Do not allow special usb to connect basically if you don't have write access to the file system you can plug in a usb with world write access to write to the file system and possibly prevent auto formatting
nosuid //if user plugs in a drive with suid, remove suid
```
```
Mount on startup
<ip>:/exports/data	  /mount/data    nfs   defaults   0 0
```

# Firewall
>firewall-config
> Masquerade zone - ip-forwarding
```
cat /etc/firewalld/zones/public.xml
firewall-cmd --permanent --zone=public --add-rich-rule='rule family=ipv4  service name=<service> source address=<ip/24>  accept'
firewall-cmd  --direct  --get-all-rules (get direct rules)
firewall-cmd --direct --add-rule ipv4 filter <INPUT or OUTPUT> <order> -j <DROP,ACCEPT>
firewall-cmd --direct --add-rule ipv4 filter <INPUT or OUTPUT> <order> -p <service name> -j <DROP,ACCEPT>
```

# Samba
```
chmod 777 /samba_share
smbpasswd -a peter
```
>/etc/samba/smb.conf
```
[myshare]  
comment = My Samba Share for peter , paul and mary
path = /samba_share
#guest ok = yes
browsable = no
write list = @group user
```
```
firewall-cmd --permanent --zone=public --add-service=samba
firewall-cmd --reload
firewall-cmd --list-all
```
```
systemctl enable smb
systemctl start smb
```
```
chcon -Rt  samba_share_t    /samba_share
```
## Mount on bootup
```
dnf install cifs-utils -y
```
```
mkdir /sambadata
```
```
mount -t cifs -o username=peter //127.0.0.1/myshare /sambadata/
```
>/etc/fstab
```
//127.0.0.1/myshare   /sambadata     cifs     credentials=/etc/sambauser   0   0
```
>/etc/sambauser
```
user=peter
pass=peter
```
## Accessing home directories
>/etc/samba/smb.conf 
```
[homes]
   comment = Home Directories
   valid users = %S, %D%w%S
   browseable = No
   read only = No
   inherit acls = Yes

```
```
setsebool   -P samba_enable_home_dirs  on
```

# DNS
```
dnf -y install bind bind-utils
```
```
hostnamectl set-hostname server.las.org
```
```
cat /etc/resolv.conf
```
> /etc/named.conf
```
listen-on port 53 { any; };
allow-query { localhost; 192.168.30.0/24; };
forwarders { 192.168.30.2; };
forward only;
dnssec-enable    no;
dnssec-validation    no;
```
```
options {
    listen-on port 53 { any; };
    listen-on-v6 port 53 { ::1; };
    directory    "/var/named";
    dump-file    "/var/named/data/cache_dump.db";
    statistics-file "/var/named/data/named_stats.txt";
    memstatistics-file "/var/named/data/named_mem_stats.txt";
    secroots-file    "/var/named/data/named.secroots";
    recursing-file    "/var/named/data/named.recursing";
    allow-query { localhost; 192.168.1.0/24; };
    forwarders { 192.168.1.2; };
    forward only;

    recursion yes;

    dnssec-enable no;
    dnssec-validation no;

    managed-keys-directory "/var/named/dynamic";

    pid-file "/run/named/named.pid";
    session-keyfile "/run/named/session.key";

    include "/etc/crypto-policies/back-ends/bind.config";
};

logging {
    channel default_debug {
        file "data/named.run";
        severity dynamic;
    };
};

zone "." IN {
    type hint;
    file "named.ca";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```
```
systemctl enable named
systemctl start named
```
>/etc/resolv.conf comment nameserver
```
# Generated by NetworkManager
search localdomain las.org
#nameserver 192.168.1.2
nameserver 192.168.1.123 #current ip
```
> Disable /etc/resolv.conf file regenerate
>/etc/NetworkManager/NetworkManager.conf 
```
[main]
#plugins=ifcfg-rh
dns=none
```
```
firewall-cmd --permanent --zone=public --add-service=dns
firewall-cmd --reload
firewall-cmd --list-all
```
## Forward Zone
> /etc/named.conf
```
zone "las.org" IN {
    type master;
    file "las.org.zone";
};
```
>/var/named/las.org.zone
```
$ORIGIN las.org.
$TTL 86400
las.org.       IN SOA server root.server.las.org. (
                          42   ; serial
                          3H   ; refresh
                          15M  ; retry
                          1W   ; expiry
                          1D ) ; minimum
las.org.     	IN   NS server
las.org.     IN   	A    192.168.1.143
server		IN 	A 	192.168.1.143
client		IN 	A 	192.168.1.144
```
```
chgrp named /var/named/las.org.zone
```
## Reverse Zone
> /etc/named.conf
```
zone "30.168.192.in-addr.arpa" IN {
 type master;
 file "192.168.30.zone";
};
```
> /var/named/192.168.1.zone
```
$TTL	86400
@	IN SOA server.las.org. root.server.las.org. (
			42	; serial
			28800	; refresh
			14400	; retry
			3600000	; expiry
			86400)	; minimum
	IN NS	server.las.org.

144	IN PTR	client.las.org.
143	IN PTR	server.las.org.
```
```
chgrp named /var/named/192.168.1.zone
```
## Zone Transfer
```
dig -t axfr las.org
```
> /etc/named.conf
```
allow-query { localhost; 192.168.1.0/24; };
allow-transfer { localhost; 192.168.1.69; };
```
# Sysmon
> /etc/rsyslog.conf
```
authpriv.*		/var/log/secure
authpriv.warning	/var/log/las_secure_warning
```
```
systemctl enable rsyslog
systemctl restart rsyslog
```
```
logger -p authpriv.warning "This is an authpriv warning message."
logger -p authpriv.alert "This is an authpriv alert message."
logger -p authpriv.info "This is an authpriv info message."
```
## Remote logging
> /etc/rsyslog.conf
```
module(load="imudp")  
input(type="imudp" port="514")
```
```
firewall-cmd --permanent --zone=public --add-port=514/udp
firewall-cmd --reload
firewall-cmd --list-all
```
> /etc/rsyslog.conf
```
authpriv.warning	@127.0.0.1
```
# AIDE
```
dnf install aide -y
```
> /etc/aide.conf
```
/path CONTENT_EX
```
```
time aide --init --config /etc/aide.conf
mv /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz
aide --check --config /etc/aide.conf
```

# Usage Statistics
```
iostat
iostat –N	(to view Logical volume disk utilization)
iostat –m	(to view in megabytes instead of kilobytes)
sar 2 5 
```

# Process Limit
> /etc/security/limits.conf
> one login session
```
peter	hard	maxlogins	1
```
```
ps -u peter | grep sleep | grep -v grep | awk '{print $1}' | xargs kill -SIGKILL
```
> /etc/security/limits.conf
```
peter	soft	nproc		15
peter	hard	nproc		25
```
```
ulimit –u 30
```

# PAM
> Root only login
```
touch /etc/nologin
```
> No password
> /etc/pam.d/login
```
auth sufficient pam_permit.so
```
> GUI no password
> /etc/pam.d/gdm-password
```
auth sufficient pam_permit.so
```
> Ban list
> auth required pam_listfile.so
> /etc/vsftpd/ftpusers
```
username
```
> Password fail2ban
```
auth        required      pam_faillock.so preauth silent audit deny=3 unlock_time=600
auth        [default=die]  pam_faillock.so  authfail  audit  deny=3  unlock_time=never
account     required      		pam_faillock.so
```
![](https://i.imgur.com/sfDM6MJ.png)
> Reset ban
```
faillock --user username --reset
```
>  /etc/pam.d/vsftpd
```
account    required    pam_time.so
```
> /etc/security/time.conf 
```
vsftpd;*;paul;!Mo0000-2400
```
# Sudo allocation
> /etc/sudoers
```
mary  ALL=/usr/bin/systemctl * httpd
mary  ALL=/usr/bin/systemctl * httpd, /usr/bin/nano /etc/httpd/*
```