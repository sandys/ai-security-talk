from __future__ import annotations
import hashlib, importlib.metadata, importlib.util, json, re
from pathlib import Path
from typing import Any, Iterable

def find_project_root(start: Path|None=None)->Path:
 current=(start or Path.cwd()).resolve()
 for candidate in (current,*current.parents):
  if (candidate/'workshop_utils.py').exists() and (candidate/'README.md').exists(): return candidate
 raise FileNotFoundError('Launch Jupyter from the toolkit root or a module beneath it.')

def package_version(distribution:str,module:str|None=None)->str|None:
 if module and importlib.util.find_spec(module) is None: return None
 try: return importlib.metadata.version(distribution)
 except importlib.metadata.PackageNotFoundError: return None

def require_package(distribution:str,module:str|None=None)->str:
 version=package_version(distribution,module)
 if version is None: raise RuntimeError(f'Missing {distribution}. Activate Python 3.12 and run `python -m pip install -r requirements.txt`.')
 print(f'Using {distribution} {version}'); return version

def sha256_text(value:str)->str: return hashlib.sha256(value.encode()).hexdigest()

def redact_for_logs(value:str)->str:
 patterns=[
  (r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}','<EMAIL>'),
  (r'(?<!\d)(?:\+?91[-\s]?)?[6-9]\d{9}(?!\d)','<PHONE>'),
  (r'\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b','<CARD>'),
  (r'\bWORKSHOP_CANARY_[A-Z0-9_]+\b','<SECRET>')]
 for pattern,replacement in patterns: value=re.sub(pattern,replacement,value,flags=re.I)
 return value

def attack_success_rate(rows:Iterable[dict[str,Any]],key='attack_succeeded')->float:
 values=[bool(row[key]) for row in rows]; return sum(values)/len(values) if values else 0.0

def save_json(path:Path,payload:Any)->Path:
 path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(payload,indent=2,default=str),encoding='utf-8'); return path
