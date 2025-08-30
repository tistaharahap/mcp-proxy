import base64
import contextlib
import json
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    host: str = Field("0.0.0.0", description="Host to listen on")
    port: int = Field(8080, description="Port to listen on")
    config: str | None = Field(None, description="Path to MCP config file")
    config_json: str | None = Field(None, description="MCP config as JSON string")
    config_json_b64: str | None = Field(None, description="MCP config as base64-encoded JSON string")

    @model_validator(mode="after")
    def validate_config(self):
        if not self.config and not self.config_json and not self.config_json_b64:
            raise ValueError("Either config, config_json, or config_json_b64 must be provided")
        if self.config and self.config_json and self.config_json_b64:
            raise ValueError("Only one of config, config_json, or config_json_b64 can be provided")
        if self.config_json and self.config_json_b64:
            raise ValueError("Only one of config_json or config_json_b64 can be provided")

        return self


settings = Settings()

if settings.config:
    config = json.load(Path(settings.config).open())
elif settings.config_json:
    config = json.loads(settings.config_json)
elif settings.config_json_b64:
    config = json.loads(base64.b64decode(settings.config_json_b64).decode("utf-8"))
else:
    raise ValueError("Either config or config_json must be provided")

proxy = FastMCP.as_proxy(config, name="Bango29 MCP Proxy")


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        proxy.run(
            transport="streamable-http",
            host=settings.host,
            port=settings.port,
        )
