# devops11A-project-app

Proyecto del grupo devops11A del Bootcamp Cloud Devops 11.

Repositorio de la aplicación *Flask* que usa *Redis* y *ElasticSearch*.

Configuraciones para Pipelines ci/cd usando *CircleCI* y *Github Actions*.

## TABLA DE CONTENIDOS

- [Descripción](#descripción)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Configuración y ejecución local](#configuración-y-ejecución-local)
- [Despliegue en Google Cloud](#despliegue-en-google-cloud)

## Descripción

Este repositorio contiene una aplicación *Flask* que cuenta el número de veces que se recarga la página, y se persiste en una base de datos *Redis*, así como los logs en *ElasticSearch*.

Viene preparado para automatizar y preparar un contendor de desarrollo en Docker a través de *Visual Studio Code*.

También crea *Actions* de Github y pipelines de *CircleCI* para la construcción de imágenes de la aplicación de manera automatizada, así como la subida de la misma al repositorio *Github*.  

A su vez genera las releases, los changelogs y los artefactos en cada mergeo a la rama main del proyecto.

## Estructura del Proyecto

```bash
├── .circleci/                      # Configuración de CircleCI
│   ├── config.yml                  # Configuración de la pipeline en CircleCI para la rama dev
│  
├── .devcontainer/                  # Configuración del entorno de desarrollo en VS Code  
│   ├── devcontainer.json           # Configuración del DevContainer  
│  
├── .github/workflows/               # Workflows de GitHub Actions  
│   ├── delete-branch.yml            # Workflow para eliminar ramas después de merge a dev  
│   ├── deploy-pipeline.yml          # Workflow para ejecutar el despliegue de la rama main y creación de la imagen de la aplicación.  
│   ├── push-branch.yml              # Workflow para ejecutar checks al subir commits a una rama que no sea dev o main.
│  
├── .vscode/                         # Configuración de VS Code  
│   ├── tasks.json                   # Tareas automatizadas para el desarrollo  
│  
├── app/                             # Carpeta principal de la aplicación  
│   ├── app.py                       # Archivo principal de la aplicación Flask  
│   ├── .pylintrc                    # Fichero de configuración del linting  
│   ├── pytest.ini                   # Configuración para pytest  
│   ├── test_app.py                  # Pruebas unitarias de la aplicación  
│
├── terraform/                       # Manifiestos para despliegue cloud de la aplicación
│   ├── configuracion/               # Manifiestos de configuración
│       ├── main.tf                  # Manifiesto principal de despliegue
│       ├── terraform.tfvars         # Variables de terraform
│       ├── variables.tf             # Variables de infraestructura
│   ├── infraestructura/             # Manifiestos de infraestructura
│       ├── kubeconfig.tpl           # Fichero configuración de Kubectl
│       ├── main.tf                  # Manifiesto principal de creación de infraestructura
│       ├── output.tf                # Fichero de salida de resultado del despliegue
│       ├── terraform.tfvars         # Variables de terraform
│       ├── variables.tf             # Variables de infraestructura
│
├── .coveragerc                      # Fichero de configuración para la cobertura de código
├── .gitignore                       # Fichero de exclusión de archivos no deseados de versionar
├── .releaserc.json                  # Fichero de configuración de la generación de la release usando semantic release. 
├── Dockerfile                       # Definición de la imagen Docker  
├── docker-compose.yml               # Configuración de servicios con Docker Compose  
├── requirements.txt                 # Dependencias del proyecto  
├── sonar-project.properties         # Configuración para SonarQube  
├── README.md                        # Documentación del proyecto  
```

## Requisitos

- [*Docker*](https://www.docker.com/)
- [*Git*](https://git-scm.com/)
- [*Terraform*](https://www.terraform.io/downloads.html)
- Una cuenta en *Google Cloud*

## Configuración y ejecución local

- Clonar el Repositorio

```bash
git clone https://github.com/juarru/devops11a-project-app.git
cd devops11a-project-app
```

- Levantar los servicios

```bash
# Desde la raiz del proyecto
docker-composer up -build
```

- La aplicación Flask se iniciará en `http://localhost:5001` .  
- También se ha configurado un despliegue del servicio *Kibana* para el seguimiento de los logs guardados en *ElasticSearch* en `http://localhost:5601` .

- Tirar los servicios

```bash
# Desde la raiz del proyecto
docker-compose down
```

## Despliegue en Google Cloud

Despliegue en Google Cloud
Para realizar el despliegue en Google Cloud, primero necesitarás instalar algunas herramientas esenciales:
Requisitos previos

Google Cloud SDK:

Herramienta de línea de comandos para interactuar con Google Cloud
Descargar e instalar Google Cloud SDK


Terraform:

Herramienta de infraestructura como código
Descargar e instalar Terraform


kubectl:

Herramienta de línea de comandos para Kubernetes
Puedes instalarlo con Google Cloud SDK: gcloud components install kubectl


Cuenta en Google Cloud Platform:

Necesitarás una cuenta con facturación activada
Tener habilitadas las APIs necesarias:

Kubernetes Engine API
Container Registry API




Permisos IAM adecuados:

Rol Kubernetes Engine Admin
Rol Service Account User



Infraestructura
La etapa de infraestructura crea los siguientes recursos:

Cluster GKE (Google Kubernetes Engine)
Namespace para ArgoCD
Instalación de ArgoCD mediante Helm
Namespace para la aplicación

Para desplegar la infraestructura:
bash# Navegar al directorio de infraestructura
cd terraform/infraestructura

# Inicializar Terraform
terraform init

# Ver los cambios que se aplicarán
terraform plan

# Aplicar los cambios
terraform apply
Después del despliegue, se generará un archivo kubeconfig en el directorio que puede utilizarse para comunicarse con el clúster.
Configuración
La etapa de configuración configura ArgoCD para desplegar la aplicación desde un repositorio Git. ArgoCD implementa GitOps, sincronizando automáticamente los cambios del repositorio en el clúster de Kubernetes.
Para configurar el despliegue:
bash# Navegar al directorio de configuración
cd terraform/configuracion

# Inicializar Terraform
terraform init

# Ver los cambios que se aplicarán
terraform plan

# Aplicar los cambios
terraform apply
Instrucciones de despliegue

Preparar el entorno:
bash# Configurar Google Cloud CLI
gcloud auth login
gcloud config set project despliegue-458304

Desplegar la infraestructura:
bashcd terraform/infraestructura
terraform init
terraform apply

Configurar kubectl:
bash# Usar el archivo kubeconfig generado
export KUBECONFIG=$(pwd)/kubeconfig
# Verificar la conexión
kubectl get nodes

Configurar el despliegue con ArgoCD:
bashcd ../configuracion
terraform init
terraform apply

Acceder a ArgoCD:
bash# Obtener la IP de ArgoCD
kubectl get svc -n argocd argocd-server
# Acceder vía navegador: https://<ARGOCD_IP>

Verificar el despliegue:
bash# Verificar pods de la aplicación
kubectl get pods -n despliegue-final-ns


Una vez completados estos pasos, la aplicación Flask estará desplegada en Google Cloud y gestionada por ArgoCD, que mantiene la sincronización con el repositorio de manifiestos de Kubernetes.ReintentarClaude puede cometer errores. Por favor, verifique las respuestas. 3.7 Sonnet