import yaml
import pytest
import os

def load_compose(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.mark.parametrize("filename", ["docker-compose.frankfurt.yml", "docker-compose.moscow.yml"])
def test_docker_compose_ports_exist(filename):
    """Проверяет, что порты прописаны для критических сервисов."""
    config = load_compose(filename)
    services = config.get('services', {})
    
    if filename == "docker-compose.frankfurt.yml":
        # В Франкфурте должны быть порты для БД и Редиса
        assert 'postgres' in services
        assert 'ports' in services['postgres'], f"Missing ports in postgres for {filename}"
        assert "5432:5432" in services['postgres']['ports']
        
        assert 'redis' in services
        assert 'ports' in services['redis'], f"Missing ports in redis for {filename}"
        assert "6379:6379" in services['redis']['ports']
        
    if filename == "docker-compose.moscow.yml":
        # В Москве должен быть порт для browserless
        assert 'browserless' in services
        assert 'ports' in services['browserless'], f"Missing ports in browserless for {filename}"
        assert "3000:3000" in services['browserless']['ports']

@pytest.mark.parametrize("filename", ["docker-compose.frankfurt.yml", "docker-compose.moscow.yml"])
def test_docker_compose_env_files(filename):
    """Проверяет наличие env_file или необходимых переменных окружения."""
    config = load_compose(filename)
    services = config.get('services', {})
    
    for service_name, service_config in services.items():
        # Проверяем, что у основных сервисов (bot, celery) есть env_file или environment
        if service_name in ['bot', 'celery', 'celery-beat']:
            assert 'env_file' in service_config or 'environment' in service_config, \
                f"Service {service_name} in {filename} missing env configuration"

@pytest.mark.parametrize("filename", ["docker-compose.frankfurt.yml", "docker-compose.moscow.yml"])
def test_docker_compose_restart_policy(filename):
    """Проверяет политику перезапуска."""
    config = load_compose(filename)
    services = config.get('services', {})
    
    for service_name, service_config in services.items():
        assert 'restart' in service_config, f"Service {service_name} in {filename} missing restart policy"
        assert service_config['restart'] in ['always', 'unless-stopped', 'on-failure']

def test_frankfurt_moscow_consistency():
    """Проверяет консистентность имен сетей и зависимостей."""
    frankfurt = load_compose("docker-compose.frankfurt.yml")
    moscow = load_compose("docker-compose.moscow.yml")
    
    # Проверяем, что в Франкфурте есть сеть frankfurt_network
    assert 'frankfurt_network' in frankfurt.get('networks', {})
    
    # Проверяем, что в Москве есть сеть moscow_network
    assert 'moscow_network' in moscow.get('networks', {})
