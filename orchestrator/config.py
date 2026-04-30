import os

CONFIG = {
    "solution": {
        "provider": os.getenv("SOLUTION_PROVIDER"),
        "model": os.getenv("SOLUTION_MODEL"),
    },
    "critic": {
        "provider": os.getenv("CRITIC_PROVIDER"),
        "model": os.getenv("CRITIC_MODEL"),
    },
    "safety": {
        "provider": os.getenv("SAFETY_PROVIDER"),
        "model": os.getenv("SAFETY_MODEL"),
    }
}