from os import cpu_count

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    SERVER_PORT: int = Field(default=8000, env="SERVER_PORT")
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    
    LOG_FILE: str = Field(default="tasks.log", env="LOG_FILE")
    LOGGER_TYPE: str = Field(default="file", env="LOGGER_TYPE")         
    
    METRICS_TYPE: str = Field(default="redis", env="METRICS_TYPE")      
    PROMETHEUS_PUSHGATEWAY_HOST: str = Field(
        default="localhost", env="PROMETHEUS_PUSHGATEWAY_HOST")
    PROMETHEUS_PUSHGATEWAY_PORT: int = Field(
        default=9091, env="PROMETHEUS_PUSHGATEWAY_PORT")
    QUEUE_TYPE: str = Field(default="redis", env="QUEUE_TYPE")     
    TASK_PRIORITY: int = Field(default=100, env="TASK_PRIORITY")
    RETRY_TASK_PRIORITY: int = Field(default=10, env="RETRY_TASK_PRIORITY")      
    TASK_QUEUE_NAME: str = Field(default="task_priority_queue", env="TASK_QUEUE_NAME")
    DEAD_LETTER_QUEUE_NAME: str = Field(
        default="dead_letter_queue", 
        env="DEAD_LETTER_QUEUE_NAME"
    )

    TASK_SIMULATED_DURATION: float = Field(
        default=1.0, env="TASK_SIMULATED_DURATION")
    TASK_SIMULATED_ERROR_PERCENTAGE: float = Field(
        default=0.1, env="TASK_SIMULATED_ERROR_PERCENTAGE")
    TASK_ERROR_RETRY_DELAY: float = Field(
        default=5.0, env="TASK_ERROR_RETRY_DELAY")
    WORKER_TIMEOUT: float = Field(
        default=30.0, env="WORKER_TIMEOUT")
    TASK_MAX_RETRIES: int = Field(
        default=3, env="TASK_MAX_RETRIES")
    WORKER_COUNT: int = Field(
        default=cpu_count(), env="WORKER_COUNT")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()