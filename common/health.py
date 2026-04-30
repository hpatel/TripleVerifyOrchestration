import sys
import asyncio
from common.config import settings
from common.deps import check_tcp, check_http


async def validate_startup(require_llm=False, check_redis=False, check_orchestrator=False):
    errors = []

    # 🔑 LLM key check
    if require_llm and not settings.OPENAI_API_KEY:
        errors.append("Missing OPENAI_API_KEY")

    # 🧠 Redis check
    if check_redis:
        if not check_tcp(settings.REDIS_HOST, settings.REDIS_PORT):
            errors.append(f"Redis not reachable at {settings.REDIS_HOST}:{settings.REDIS_PORT}")

    # 🔗 Orchestrator check
    if check_orchestrator and settings.ORCHESTRATOR_URL:
        ok = await check_http(settings.ORCHESTRATOR_URL.replace("/run", "/health"))
        if not ok:
            errors.append(f"Orchestrator not reachable at {settings.ORCHESTRATOR_URL}")

    if errors:
        print("\n🚨 STARTUP VALIDATION FAILED:\n")
        for e in errors:
            print(f" - {e}")
        print()
        sys.exit(1)

    print("✅ Startup validation passed")