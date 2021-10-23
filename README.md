## DESCRIPTION

用于更新Cloudflare的DNS记录

+ `token` 为 Cloudflare 中的 API 令牌
+ `zone_id` 为 目标域名的 Zone ID
+ `record_type` 为 DNS 记录类型，此处为 A
+ `record_name` 为 需要修改的 DNS 记录名，如：a.example.com

## USAGE

以 CentOS 系统为例

### 安装 Python3

```
sudo yum install python3 -y
```

### 安装依赖库

```
sudo pip3 install -r requirements.txt
```

### 执行

```
python3 update_cloudflare_dns.py
```

### 添加定时任务

```
crontab -e
```

```
# 每30分钟执行一次
*/30 * * * * /path/to/update_cloudflare_dns.py > /dev/null 2>&1
```

DONE 🍺

