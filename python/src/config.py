"""Central configuration loaded from environment variables."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class LLMConfig:
    # 1. 调整provider默认值为tongyi（通义千问），保留环境变量可控
    provider: str = os.getenv("LLM_PROVIDER", "tongyi")
    # 2. 通义千问默认模型改为qwen-plus（也可根据需求选qwen-turbo/qwen-max等）
    model: str = os.getenv("LLM_MODEL", "qwen-plus")
    # 3. 替换API Key环境变量为通义千问依赖的DASHSCOPE_API_KEY
    api_key: str = os.getenv("DASHSCOPE_API_KEY", "")
    # 4. 温度/最大令牌数保留（通义千问兼容这两个参数）
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "4096"))


@dataclass(frozen=True)
class KafkaConfig:
    bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    group_id: str = os.getenv("KAFKA_GROUP_ID", "ci-agents")
    topics: dict = field(default_factory=lambda: {
        "changes": os.getenv("KAFKA_TOPIC_CHANGES", "ci.changes"),
        "analysis": os.getenv("KAFKA_TOPIC_ANALYSIS", "ci.analysis"),
        "comparison": os.getenv("KAFKA_TOPIC_COMPARISON", "ci.comparison"),
        "battlecard": os.getenv("KAFKA_TOPIC_BATTLECARD", "ci.battlecard"),
        "alerts": os.getenv("KAFKA_TOPIC_ALERTS", "ci.alerts"),
    })


@dataclass(frozen=True)
class ElasticsearchConfig:
    url: str = os.getenv("ES_URL", "http://localhost:9200")
    index_prefix: str = os.getenv("ES_INDEX_PREFIX", "ci-")
    api_key: str = os.getenv("ES_API_KEY", "")


@dataclass(frozen=True)
class RedisConfig:
    url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


@dataclass(frozen=True)
class NotificationConfig:
    slack_webhook: str = os.getenv("SLACK_WEBHOOK_URL", "")
    dingtalk_webhook: str = os.getenv("DINGTALK_WEBHOOK_URL", "")
    email_smtp_host: str = os.getenv("EMAIL_SMTP_HOST", "")
    email_smtp_port: int = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    email_from: str = os.getenv("EMAIL_FROM", "")
    email_password: str = os.getenv("EMAIL_PASSWORD", "")


@dataclass(frozen=True)
class AppConfig:
    llm: LLMConfig = field(default_factory=LLMConfig)
    kafka: KafkaConfig = field(default_factory=KafkaConfig)
    elasticsearch: ElasticsearchConfig = field(default_factory=ElasticsearchConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    notification: NotificationConfig = field(default_factory=NotificationConfig)

    monitor_interval_minutes: int = int(os.getenv("MONITOR_INTERVAL_MINUTES", "60"))
    quality_threshold: float = float(os.getenv("QUALITY_THRESHOLD", "7.0"))
    max_reflexion_retries: int = int(os.getenv("MAX_REFLEXION_RETRIES", "3"))


config = AppConfig()