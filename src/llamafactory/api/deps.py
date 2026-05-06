# Copyright 2025 the LlamaFactory team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""FastAPI dependency injection for the LLaMA Factory API."""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from ..extras.packages import is_fastapi_available
from .engine_holder import EngineHolder, get_engine_holder


if is_fastapi_available():
    from fastapi import Depends


async def get_api_key(
    authorization: Annotated[str | None, Header()] = None,
) -> str | None:
    r"""Extract API key from Authorization header."""
    if authorization and authorization.startswith("Bearer "):
        return authorization[7:]
    return None


async def verify_api_key(
    api_key: Annotated[str | None, Depends(get_api_key)],
) -> None:
    r"""Verify API key if configured. Enable by setting API_KEY env var."""
    import os

    required_key = os.getenv("API_KEY")
    if required_key and api_key != required_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_holder() -> EngineHolder:
    r"""Dependency provider for the global EngineHolder singleton."""
    return get_engine_holder()


# Reusable dependency type
EngineHolderDep = Annotated[EngineHolder, Depends(get_holder)]
