import os
from typing import Optional
from dotenv import load_dotenv, set_key, find_dotenv


def set_env_value(key: str, value: str, env_path: Optional[str] = None) -> bool:
    """Set or update a key in the given .env file.

    Uses python-dotenv's `set_key` when available; falls back to a safe
    file-based replace/append if needed.

    Returns True on success, False on failure.
    """
    if env_path is None:
        env_path = find_dotenv()
        if not env_path:
            # default to workspace .env
            env_path = ".env"

    # ensure file exists
    if not os.path.exists(env_path):
        open(env_path, "a", encoding="utf-8").close()

    try:
        load_dotenv(env_path, override=True)
        result = set_key(env_path, key, value)
        # set_key may return a tuple or a truthy value
        return bool(result)
    except Exception:
        # fallback: read, replace or append
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            key_stripped = key.strip()
            replaced = False
            out_lines = []
            for line in lines:
                stripped = line.strip()
                # skip commented lines and only replace exact key matches
                if (
                    stripped.startswith(f"{key_stripped}=")
                    or stripped.startswith(f"{key_stripped} =")
                ):
                    out_lines.append(f"{key_stripped}={value}\n")
                    replaced = True
                else:
                    out_lines.append(line)

            if not replaced:
                out_lines.append(f"{key_stripped}={value}\n")

            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(out_lines)

            return True
        except Exception:
            return False


def get_env_path(default: Optional[str] = None) -> str:
    """Return detected .env path or the provided default.

    Useful for callers that want to know which file will be written.
    """
    path = find_dotenv()
    if path:
        return path
    return default or ".env"


def normalize_env_file(env_path: Optional[str] = None) -> bool:
    """Normalize formatting of an .env file.

    - Preserves comment lines and blank lines.
    - For key/value lines, strips surrounding whitespace from keys and values
      and rewrites them as `KEY=value`.

    Returns True on success, False on failure.
    """
    if env_path is None:
        env_path = find_dotenv()
        if not env_path:
            env_path = ".env"

    if not os.path.exists(env_path):
        return False

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        out_lines = []
        for line in lines:
            stripped = line.rstrip("\n")
            if not stripped.strip():
                out_lines.append("\n")
                continue
            if stripped.lstrip().startswith("#"):
                out_lines.append(stripped + "\n")
                continue

            if "=" in stripped:
                key, val = stripped.split("=", 1)
                key = key.strip()
                val = val.strip()
                out_lines.append(f"{key}={val}\n")
            else:
                # leave unknown lines as-is
                out_lines.append(stripped + "\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(out_lines)

        return True
    except Exception:
        return False
