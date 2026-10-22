"""Optional server-side media bridge; host registration requires maintainer review.

This module never changes a host app's user credits, auth, default supplier or
fallback chain. Unknown paid submissions must be reconciled, never auto-fallback.
"""
from pathlib import Path
import base64,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unified_client import Client,generate

class ToApisMediaProvider:
    name='toapis'
    def __init__(self,client=None,output_dir=None):
        self.client=client or Client()
        self.output_dir=Path(output_dir or Path(__file__).resolve().parents[1]/'outputs')
        self.presets=json.loads((Path(__file__).resolve().parents[1]/'presets.json').read_text(encoding='utf-8'))

    def generate(self,prompt,model,*,live=False,run_id='default',image=None,max_usd=None):
        if model not in self.presets:raise ValueError('Unreviewed model preset')
        preset=self.presets[model]
        result=generate(self.client,preset,prompt,self.output_dir,max_usd or ('.10' if preset['kind']=='image' else '.80'),live,image,run_id)
        if not live:return result
        if result.get('status')!='completed':raise RuntimeError('Generation stopped; reconcile the saved task before another paid request')
        return {'media':self.from_file(result['output'],preset['kind']),'provider_billing':result.get('cost')}

    @staticmethod
    def from_file(file,kind):
        p=Path(file);raw=p.read_bytes()
        if kind=='image':
            if not raw.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('This reviewed bridge requires a verified PNG')
            return {'path':str(p.resolve()),'filename':p.name,'mime_type':'image/png','b64_data':base64.b64encode(raw).decode()}
        if kind=='video':
            if b'ftyp' not in raw[:40]:raise ValueError('Expected MP4')
            return {'path':str(p.resolve()),'filename':p.name,'mime_type':'video/mp4'}
        raise ValueError('Unsupported media kind')

    @staticmethod
    def editor_image_fragment(file):
        media=ToApisMediaProvider.from_file(file,'image')
        # Only the image fragment, not a fabricated full ImageApiResponse.
        return {'data':media['b64_data'],'mimeType':media['mime_type']}

    @staticmethod
    def save_claudia_image(file,output):
        ToApisMediaProvider.from_file(file,'image')
        target=Path(output);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(Path(file).read_bytes());return str(target)
