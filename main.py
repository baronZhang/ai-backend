import os

from pydantic import BaseModel, Field


# 1. 定义数据模型 (类似于 DTO/POJO)
# Pydantic 的 BaseModel 比 dataclass 更强，它会在运行时验证数据类型！
class ModelSettings(BaseModel):
    name: str = Field(..., description="模型名称，如 gpt-4")
    api_key: str | None = Field(None, exclude=True)  # exclude=True 类似于 @JsonIgnore
    temperature: float = 0.7
    stop_words: list[str] = []


class AppConfig(BaseModel):
    env: str = "dev"
    models: list[ModelSettings]


# 2. 模拟 Service 层
class ConfigLoader:
    """
    负责加载配置的 Service
    """

    def load_from_env(self) -> AppConfig:
        # 模拟从环境变量或 JSON 加载
        # 这里展示 Pydantic 的强大：自动解析字典并校验类型
        mock_data = {
            "env": "production",
            "models": [
                {
                    "name": "gpt-4-turbo",
                    "temperature": 0.5,
                    "stop_words": ["ERROR", "END"],
                },
                {
                    "name": "llama-3-local",
                    # temperature 缺失会使用默认值 0.7
                },
            ],
        }

        try:
            # 这一步类似于 Jackson 的 ObjectMapper.convertValue
            config = AppConfig.model_validate(mock_data)
            return config
        except Exception as e:
            print(f"配置校验失败: {e}")
            raise


# 3. Main 入口 (Java 的 public static void main)
if __name__ == "__main__":
    loader = ConfigLoader()
    config = loader.load_from_env()

    print(f"当前环境: {config.env}")

    for model in config.models:
        print(f"--- 模型: {model.name} ---")
        print(f"参数: Temp={model.temperature}")
        print(f"配置内容: stop_words = {model.stop_words}")
