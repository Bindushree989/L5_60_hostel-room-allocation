# Static Code Analysis — Issue Report

## Before-Fix Findings

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe YAML loading | Security — Medium | 21 | `yaml.load()` with `yaml.Loader` can deserialize untrusted input unsafely. | Use `yaml.safe_load()` if the configuration format only needs standard YAML data types. |
| Flask debug mode enabled | Security — High | 80 | `app.run(debug=True)` can expose the interactive debugger and create a serious risk if deployed. | Disable debug mode for normal or production execution; use a safe configuration setting. |
| Hardcoded database password | Security — Low | 66 | The database password `Hostel@123` is embedded in the source code. | Read the password from an environment variable or a secrets manager; rotate it if it is a real credential. |
| Insecure remote logging configuration | Security — Medium | 72 | `logging.config.listen(9999)` can expose a remote logging configuration listener. | Remove the listener if unnecessary or secure and restrict access to it. |
| Random room lottery | Security / Quality — Low | 56 | Bandit flags `random.sample()` because the standard pseudo-random generator is not intended for security-sensitive use. | If the lottery requires security-sensitive unpredictability, use `secrets`-based selection; otherwise document that it is a non-security allocation shuffle. |
| Dangerous mutable default | Code Quality | 29 | `allocateRoom` uses a list as a default argument, which can be shared across calls. | Change the default to `None` and create a new list inside the function. |
| Inconsistent function naming | Code Quality | 20, 29, 41, 47, 52, 55, 58, 65, 71, 75, 79 | Function names use camelCase instead of Python's usual snake_case convention. | Rename functions and update all call sites. |
| Missing documentation | Code Quality | 1, 20, 29, 41, 47, 52, 55, 58, 65, 68, 71, 75, 79, 82 | The module and several functions lack docstrings. | Add a module docstring and concise docstrings to functions. |
| Unused imports | Code Quality | 1–2 | `os` and `sys` are imported but not used. | Remove the imports if they are not needed. |
| Type comparison | Code Quality | 30 | The code uses `type()` for a type check. | Use `isinstance()` when checking whether a value belongs to a type. |
| Unused argument | Code Quality | 29 | The `gender` argument is not used in `allocateRoom`. | Use it if required by the allocation rules, or remove it and update callers if it is unnecessary. |
| Long lines and spacing | Style | 25, 66, 95, 20, 29, 41, 47, 52, 55, 58, 65, 68, 71, 74, 79, 101 | Flake8/Pylint report lines that are too long and missing blank lines around functions. | Wrap long lines and follow the project's chosen line-length and spacing conventions. |
| Dictionary iteration | Code Quality | 60 | Pylint suggests using `.items()` when iterating over dictionary keys and values. | Iterate with `.items()` if both each key and its value are needed. |

## Notes

- Findings were recorded from the initial Pylint, Flake8, and Bandit reports.
- Line numbers may change after code edits.
- Verify each correction by rerunning the tools and reviewing the updated reports.
