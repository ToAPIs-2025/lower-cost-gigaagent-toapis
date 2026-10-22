# Lower-cost GigaAgent with ToAPIs

An agent system with an existing image-generator registry. This proposal targets image generation.

Independent API recipe and provider proposal; not an upstream-endorsed integration.

[English](README.md) · [ru](README_ru.md)

Upstream: [ai-forever/giga_agent](https://github.com/ai-forever/giga_agent) · fixed SHA `e02715ff2d1a29192f167d385647064a2ff5d2e5`. Attribution: **AI Forever / GigaAgent contributors**. [Upstream license](UPSTREAM-LICENSE). This standalone repository contains ToAPIs community code and original API media; it does not relicense the upstream application.

## Scope

Standalone image API succeeded and the base64 output boundary was verified. Includes a candidate matching BaseImageGenerator methods; native runtime/registration is not accepted. A stable run_id must come from the host, and readiness must not generate a paid ping. Video is a future partnership topic, not a shipped provider.

## Demo / Examples

### gpt-image-2(VIP)

![Original API output](assets/gpt-image-2-vip-a137d41930.png)

## Corresponding API pricing

| Model | Parameters | API price | This case |
|---|---|---|---|
| gpt-image-2(VIP) | n=1, size=1:1, resolution=1K, quality=low | $0.0019/image | $0.0019 quote; actual pending |

Rates queried with the generation API Key on 2026-10-22. Quotes are not settled charges. For token-metered video, $/M is the billing rate; observed $/s = this case’s settled cost / decoded MP4 duration and is not a fixed future price. gpt-image-2(VIP) low/1K starts at $0.0019/image. No comparative quality, uptime or savings benchmark is claimed.

## Run

Set `TOAPIS_API_KEY` privately; use Python 3.10+. No account access token is needed for generation.

```sh
python unified_client.py --model gpt-image-2-vip --prompt-file prompts/image.txt --max-usd .10
# Quote only. Explicit paid submission:
python unified_client.py --model gpt-image-2-vip --prompt-file prompts/image.txt --max-usd .10 --live --run-id my-reviewed-example
```

[Provider contract and acceptance](integration/README.md) · [Original prompts](prompts/image.txt) · [Sanitized case records](cases.json)

[Model pricing / Try ToAPIs](https://go2v.toapis.com/1022_ga) · Campaign `1022_ga`
