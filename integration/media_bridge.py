"""Output-boundary helper only; app registration/UI still require acceptance."""
from pathlib import Path
import base64
def image_fragment(file):
    raw=Path(file).read_bytes()
    if not raw.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Expected verified PNG output')
    return {'data':base64.b64encode(raw).decode(),'mimeType':'image/png'}
def wallas_media(file):
    fragment=image_fragment(file);p=Path(file)
    return {'path':str(p.resolve()),'filename':p.name,'mime_type':fragment['mimeType'],'b64_data':fragment['data']}
def claudia_output(file,output):
    raw=Path(file).read_bytes();image_fragment(file)
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);return str(p)
