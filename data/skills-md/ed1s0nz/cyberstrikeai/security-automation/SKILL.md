---
name: security-automation
description: 安全自动化的专业技能和方法论
version: 1.0.0
---

# 安全自动化

## 概述

安全自动化是提高安全运营效率的重要手段。本技能提供安全自动化的方法、工具和最佳实践。

## 自动化场景

### 1. 漏洞扫描

**自动化扫描：**
- 定期扫描
- CI/CD集成
- 结果分析
- 报告生成

### 2. 安全测试

**自动化测试：**
- 单元测试
- 集成测试
- 安全测试
- 回归测试

### 3. 事件响应

**自动化响应：**
- 事件检测
- 自动遏制
- 通知告警
- 证据收集

### 4. 合规检查

**自动化合规：**
- 配置检查
- 策略验证
- 报告生成
- 修复建议

## 工具和框架

### 漏洞扫描自动化

**使用Nessus API：**
```python
import requests

# 创建扫描
def create_scan(target, scan_name):
    url = "https://nessus:8834/scans"
    headers = {"X-ApiKeys": "access_key:secret_key"}
    data = {
        "uuid": "template-uuid",
        "settings": {
            "name": scan_name,
            "text_targets": target
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# 启动扫描
def launch_scan(scan_id):
    url = f"https://nessus:8834/scans/{scan_id}/launch"
    headers = {"X-ApiKeys": "access_key:secret_key"}
    response = requests.post(url, headers=headers)
    return response.json()
```

**使用OpenVAS API：**
```python
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp

# 连接OpenVAS
connection = UnixSocketConnection()
gmp = Gmp(connection)
gmp.authenticate('username', 'password')

# 创建扫描任务
target = gmp.create_target(name='target', hosts=['192.168.1.0/24'])
config = gmp.get_configs()[0]
scanner = gmp.get_scanners()[0]

task = gmp.create_task(
    name='scan_task',
    config_id=config['id'],
    target_id=target['id'],
    scanner_id=scanner['id']
)

# 启动扫描
gmp.start_task(task['id'])
```

### CI/CD集成

**Jenkins Pipeline：**
```groovy
pipeline {
    agent any
    stages {
        stage('Security Scan') {
            steps {
                sh 'npm audit'
                sh 'snyk test'
                sh 'sonar-scanner'
            }
        }
        stage('Vulnerability Scan') {
            steps {
                sh 'nmap --script vuln target'
            }
        }
    }
    post {
        always {
            publishHTML([
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Security Report'
            ])
        }
    }
}
```

**GitHub Actions：**
```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      - name: Run SonarQube
        uses: sonarsource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### 安全测试自动化

**使用OWASP ZAP：**
```python
from zapv2 import ZAPv2

# 启动ZAP
zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8080'})

# 开始扫描
zap.urlopen('http://target.com')
zap.spider.scan('http://target.com')
while int(zap.spider.status()) < 100:
    time.sleep(1)

# 主动扫描
zap.ascan.scan('http://target.com')
while int(zap.ascan.status()) < 100:
    time.sleep(1)

# 获取结果
alerts = zap.core.alerts()
```

**使用Burp Suite：**
```python
from burp import IBurpExtender, IScannerCheck

class BurpExtender(IBurpExtender, IScannerCheck):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Security Automation")
        callbacks.registerScannerCheck(self)
    
    def doPassiveScan(self, baseRequestResponse):
        # 被动扫描逻辑
        return None
    
    def doActiveScan(self, baseRequestResponse, insertionPoint):
        # 主动扫描逻辑
        return None
```

### 事件响应自动化

**使用Splunk：**
```python
import splunklib.client as client

# 连接Splunk
service = client.connect(
    host='splunk.example.com',
    port=8089,
    username='admin',
    password='password'
)

# 搜索安全事件
search_query = 'index=security event_type="malware"'
kwargs = {"earliest_time": "-1h", "latest_time": "now"}
search = service.jobs.create(search_query, **kwargs)

# 处理结果
for result in search:
    if result['severity'] == 'high':
        # 自动响应
        send_alert(result)
        isolate_system(result['host'])
```

**使用ELK Stack：**
```python
from elasticsearch import Elasticsearch

# 连接Elasticsearch
es = Elasticsearch(['localhost:9200'])

# 搜索安全事件
query = {
    "query": {
        "match": {
            "event_type": "intrusion"
        }
    }
}

results = es.search(index="security", body=query)

# 自动响应
for hit in results['hits']['hits']:
    if hit['_source']['severity'] == 'critical':
        # 自动遏制
        block_ip(hit['_source']['src_ip'])
        send_alert(hit['_source'])
```

## 自动化脚本

### 漏洞扫描脚本

```python
#!/usr/bin/env python3
import subprocess
import json
import smtplib
from email.mime.text import MIMEText

def run_nmap_scan(target):
    """运行Nmap扫描"""
    result = subprocess.run(
        ['nmap', '--script', 'vuln', '-oJ', '-', target],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def analyze_results(results):
    """分析扫描结果"""
    vulnerabilities = []
    for host in results.get('hosts', []):
        for port in host.get('ports', []):
            for script in port.get('scripts', []):
                if script.get('id') == 'vuln':
                    vulnerabilities.append({
                        'host': host['address'],
                        'port': port['portid'],
                        'vuln': script.get('output', '')
                    })
    return vulnerabilities

def send_report(vulnerabilities):
    """发送报告"""
    if vulnerabilities:
        msg = MIMEText(f"发现 {len(vulnerabilities)} 个漏洞")
        msg['Subject'] = '漏洞扫描报告'
        msg['From'] = 'security@example.com'
        msg['To'] = 'admin@example.com'
        
        server = smtplib.SMTP('smtp.example.com')
        server.send_message(msg)
        server.quit()

if __name__ == '__main__':
    target = '192.168.1.0/24'
    results = run_nmap_scan(target)
    vulnerabilities = analyze_results(results)
    send_report(vulnerabilities)
```

### 配置检查脚本

```python
#!/usr/bin/env python3
import boto3
import json

def check_s3_buckets():
    """检查S3存储桶安全配置"""
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    
    issues = []
    for bucket in buckets['Buckets']:
        # 检查公开访问
        try:
            acl = s3.get_bucket_acl(Bucket=bucket['Name'])
            for grant in acl.get('Grants', []):
                if grant.get('Grantee', {}).get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    issues.append({
                        'bucket': bucket['Name'],
                        'issue': 'Public access enabled'
                    })
        except:
            pass
        
        # 检查加密
        try:
            encryption = s3.get_bucket_encryption(Bucket=bucket['Name'])
        except:
            issues.append({
                'bucket': bucket['Name'],
                'issue': 'Encryption not enabled'
            })
    
    return issues

if __name__ == '__main__':
    issues = check_s3_buckets()
    print(json.dumps(issues, indent=2))
```

## 最佳实践

### 1. 自动化策略

- 识别可自动化场景
- 制定自动化计划
- 逐步实施
- 持续改进

### 2. 工具选择

- 评估工具功能
- 考虑集成性
- 考虑成本
- 测试验证

### 3. 流程设计

- 明确流程步骤
- 定义触发条件
- 设置异常处理
- 记录操作日志

### 4. 监控和维护

- 监控自动化任务
- 定期检查结果
- 更新规则和脚本
- 优化性能

## 注意事项

- 确保自动化准确性
- 设置适当的权限
- 保护自动化凭证
- 定期审查自动化规则