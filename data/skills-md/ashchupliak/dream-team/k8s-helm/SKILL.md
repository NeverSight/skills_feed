---
name: k8s-helm
description: Kubernetes and Helm patterns - use for deployment configs, service definitions, ConfigMaps, Secrets, and Helm chart management
---

# Kubernetes & Helm Patterns

## Helm Chart Structure

```
helm/orca-facade/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── serviceaccount.yaml
└── charts/           # Dependencies
```

## Chart.yaml

```yaml
apiVersion: v2
name: orca-facade
description: Orca Facade API Service
type: application
version: 1.0.0
appVersion: "1.0.0"

dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

## values.yaml

```yaml
# Image configuration
image:
  repository: registry.example.com/orca-facade
  tag: latest
  pullPolicy: IfNotPresent

# Replica configuration
replicaCount: 2

# Resource limits
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

# Service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: 8080
  grpcPort: 8081

# Ingress
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: orca.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: orca-tls
      hosts:
        - orca.example.com

# Environment variables
env:
  SPRING_PROFILES_ACTIVE: k8s
  SERVER_PORT: "8080"

# Secrets (reference external secrets)
secrets:
  DATABASE_URL:
    secretName: orca-db-credentials
    key: url
  JWT_SECRET:
    secretName: orca-jwt
    key: secret

# Health checks
health:
  livenessProbe:
    httpGet:
      path: /actuator/health/liveness
      port: 8080
    initialDelaySeconds: 30
    periodSeconds: 10
  readinessProbe:
    httpGet:
      path: /actuator/health/readiness
      port: 8080
    initialDelaySeconds: 10
    periodSeconds: 5

# Autoscaling
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

# PostgreSQL subchart
postgresql:
  enabled: false  # Use external database
```

## Deployment Template

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "orca-facade.fullname" . }}
  labels:
    {{- include "orca-facade.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "orca-facade.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
      labels:
        {{- include "orca-facade.selectorLabels" . | nindent 8 }}
    spec:
      serviceAccountName: {{ include "orca-facade.serviceAccountName" . }}
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.targetPort }}
              protocol: TCP
            - name: grpc
              containerPort: {{ .Values.service.grpcPort }}
              protocol: TCP
          env:
            {{- range $key, $value := .Values.env }}
            - name: {{ $key }}
              value: {{ $value | quote }}
            {{- end }}
            {{- range $key, $secret := .Values.secrets }}
            - name: {{ $key }}
              valueFrom:
                secretKeyRef:
                  name: {{ $secret.secretName }}
                  key: {{ $secret.key }}
            {{- end }}
          {{- with .Values.health.livenessProbe }}
          livenessProbe:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- with .Values.health.readinessProbe }}
          readinessProbe:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

## Service Template

```yaml
# templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "orca-facade.fullname" . }}
  labels:
    {{- include "orca-facade.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
    - port: {{ .Values.service.grpcPort }}
      targetPort: grpc
      protocol: TCP
      name: grpc
  selector:
    {{- include "orca-facade.selectorLabels" . | nindent 4 }}
```

## ConfigMap Template

```yaml
# templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "orca-facade.fullname" . }}-config
  labels:
    {{- include "orca-facade.labels" . | nindent 4 }}
data:
  application.yaml: |
    spring:
      profiles:
        active: k8s
    server:
      port: {{ .Values.service.targetPort }}
    management:
      endpoints:
        web:
          exposure:
            include: health,info,prometheus
```

## Helper Templates

```yaml
# templates/_helpers.tpl
{{- define "orca-facade.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "orca-facade.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "orca-facade.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ include "orca-facade.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "orca-facade.selectorLabels" -}}
app.kubernetes.io/name: {{ include "orca-facade.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

## HorizontalPodAutoscaler

```yaml
# templates/hpa.yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "orca-facade.fullname" . }}
  labels:
    {{- include "orca-facade.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "orca-facade.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
{{- end }}
```

## Helm Commands

```bash
# Install/Upgrade
helm upgrade --install orca-facade ./helm/orca-facade \
  -f ./helm/orca-facade/values-prod.yaml \
  --namespace orca \
  --create-namespace

# Dry run
helm upgrade --install orca-facade ./helm/orca-facade \
  --dry-run --debug

# Template only (see generated YAML)
helm template orca-facade ./helm/orca-facade -f values-prod.yaml

# Lint chart
helm lint ./helm/orca-facade

# Rollback
helm rollback orca-facade 1 --namespace orca

# History
helm history orca-facade --namespace orca

# Uninstall
helm uninstall orca-facade --namespace orca
```

## kubectl Commands

```bash
# Get pods
kubectl get pods -n orca -l app.kubernetes.io/name=orca-facade

# Logs
kubectl logs -n orca -l app.kubernetes.io/name=orca-facade --tail=100 -f

# Describe deployment
kubectl describe deployment orca-facade -n orca

# Port forward for local testing
kubectl port-forward -n orca svc/orca-facade 8080:80

# Exec into pod
kubectl exec -it -n orca deployment/orca-facade -- /bin/sh

# Apply manually
kubectl apply -f k8s/configmap.yaml -n orca
```
