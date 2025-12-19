# 2. 语法映射：从 Java 到 Modern Python
# Python 3.5+ 引入了 Type Hints（类型提示），虽然运行时不强制（依然是动态语言），但在 IDE 和静态分析器的配合下，它能提供 90% 的 Java 安全感。

# 2.1 变量与函数：加上类型 (Type Hints)

# public List<String> processTags(List<String> tags, boolean force) { ... }
# 导入类型系统，类似于 java.util.*
from typing import List, Optional, Dict, Union


# 这里的 -> List[str] 纯粹是给 IDE 和阅读者看的，运行时会被忽略
def process_tags(tags: List[str], force: bool = False) -> List[str]:
    result: List[str] = []
    for tag in tags:
        result.append(tag.upper())
    return result


# Python 3.10+ 新写法 (更简洁，类似 var)
# list[str] 替代 List[str], | 替代 Union
def process_data(data: dict[str, int] | None) -> list[str]:
    if data is None:
        return []
    return [str(k) for k in data.keys()]


# 2.2 数据对象：告别 Getter/Setter (Data Classes)
# 你一定熟悉 Lombok 的 @Data 或 Java 16 的 record。Python 3.7 引入了 @dataclass，彻底消灭了繁琐的 __init__。
# @Data
# @AllArgsConstructor
# public class AIModelConfig {
#     private String modelName;
#     private double temperature;
#     private int maxTokens;
# }

from dataclasses import dataclass


@dataclass
class AIModelConfig:
    # 自动生成 __init__, __repr__, __eq__
    model_name: str
    temperature: float = 0.7  # 默认值
    max_tokens: int = 1024

    # 可以在这里添加简单的逻辑方法
    def is_creative(self) -> bool:
        return self.temperature > 0.8


# 2.3 接口与多态：Protocol (Duck Typing 的规范化)
# Java 使用 interface 强制契约。Python 以前靠“默契”（只要有那个方法就行）。现在我们可以使用 Protocol 来显式定义这种契约。
from typing import Protocol


# 定义接口 (类似于 public interface LLMClient)
class LLMClient(Protocol):
    def generate(self, prompt: str) -> str: ...  # ... 等同于 Java 接口中的没有方法体


class OpenAIClient:
    # 不需要显式 implements LLMClient，只要方法签名匹配即可
    def generate(self, prompt: str) -> str:
        return f"OpenAI response to: {prompt}"


class LocalLlamaClient:
    def generate(self, prompt: str) -> str:
        return f"Local Llama response to: {prompt}"


# 依赖注入风格
def run_agent(client: LLMClient, prompt: str):
    print(client.generate(prompt))
