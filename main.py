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

    @model_validator(mode="after")
    def validate_config(self):
        if not self.config and not self.config_json:
            raise ValueError("Either config or config_json must be provided")
        if self.config and self.config_json:
            raise ValueError("Only one of config or config_json can be provided")
        if self.config_json:
            self.config = "config.json"
            with open(self.config, "w") as f:
                f.write(self.config_json)
        return self


settings = Settings()
config = json.load(Path(settings.config).open())
proxy = FastMCP.as_proxy(config, name="Bango29 MCP Proxy")


if __name__ == "__main__":
    proxy.run(
        transport="streamable-http",
        host=settings.host,
        port=settings.port,
    )
