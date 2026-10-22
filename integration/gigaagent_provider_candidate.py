"""Review candidate for GigaAgent's ImageGeneratorRegistry (not auto-imported).

Install the community client's modules on the server Python path first. Native
registration, request-ID propagation and UI acceptance remain maintainer tasks.
"""
from __future__ import annotations
import asyncio,base64,json
from pathlib import Path
from typing import Any
from pydantic import Field,PrivateAttr
from giga_agent.generators.image.base import BaseImageGenerator
from giga_agent.generators.image.registry import ImageGeneratorRegistry
from unified_client import Client,prepare,generate

@ImageGeneratorRegistry.register('toapis')
class ToApisImageGen(BaseImageGenerator):
    model: str = Field(default='gpt-image-2-vip')
    state_dir: str = Field(default='.toapis-state')
    preset_file: str = Field(default='presets.json')
    _api: Any = PrivateAttr(default=None)
    _preset: Any = PrivateAttr(default=None)

    async def init(self)->None:
        if self.model!='gpt-image-2-vip':raise ValueError('Only the reviewed low/1K text-to-image preset is mapped')
        presets=json.loads(Path(self.preset_file).read_text(encoding='utf-8'))
        self._preset=presets[self.model]
        self._api=Client(state=self.state_dir)
        await super().init()

    async def check_connection(self)->bool:
        # Override the base class's paid 256x256 ping. Price/readiness check only.
        if not self._initialized:await self.init()
        await asyncio.to_thread(prepare,self._api,self._preset,'readiness only','.10')
        return True

    async def _generate_image(self,prompt:str,width:int|None=None,height:int|None=None,**kwargs:Any)->str:
        if (width not in (None,1024) or height not in (None,1024)) or set(kwargs)-{'run_id'}:
            raise ValueError('Only 1024x1024 text-to-image is mapped; reject unsupported inputs before submission')
        run_id=kwargs.get('run_id')
        if not isinstance(run_id,str) or not run_id.strip():raise ValueError('Pass a stable host request run_id before paid generation')
        result=await asyncio.to_thread(generate,self._api,self._preset,prompt,'outputs','.10',True,None,run_id)
        if result['status']!='completed':raise RuntimeError('Task stopped; reconcile existing state before retrying')
        return base64.b64encode(Path(result['output']).read_bytes()).decode()
