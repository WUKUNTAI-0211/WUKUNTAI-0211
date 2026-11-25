<!-- ============================================================
     WUKUNTAI-0211 / WUKUNTAI-0211 — profile README
     Banner: assets/banner-{light,dark}.svg, drawn by scripts/banner.py (SMIL animation).
     Section headers are static shields. Palette: #0b0d1a (ink) · #7c5cf0 (violet) · #5eead4 (teal).
     The space-shooter game at the bottom is redrawn daily by .github/workflows/game.yml.
     ============================================================ -->

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg"/>
    <img src="assets/banner-light.svg" alt="Kun-Tai Wu, semantic model routing. Animated: prompts enter vLLM Semantic Router, which checks keyword, embedding and domain signals and routes each one to vLLM, SGLang, TensorRT-LLM or Ollama." width="100%"/>
  </picture>
</div>

<p align="center">
  <a href="https://github.com/vllm-project/semantic-router/pulls?q=is%3Apr+author%3AWUKUNTAI-0211+is%3Amerged"><img src="https://img.shields.io/badge/merged_PRs-55-7c5cf0?style=for-the-badge&logo=github&logoColor=white&labelColor=0b0d1a" alt="55 merged PRs in vLLM Semantic Router"/></a>
  <a href="https://github.com/vllm-project/semantic-router/pulls?q=is%3Apr+reviewed-by%3AWUKUNTAI-0211+-author%3AWUKUNTAI-0211"><img src="https://img.shields.io/badge/PRs_reviewed-86-7c5cf0?style=for-the-badge&logo=github&logoColor=white&labelColor=0b0d1a" alt="86 PRs reviewed"/></a>
  <a href="https://www.linkedin.com/in/kun-tai-wu/"><img src="https://img.shields.io/badge/LinkedIn-kun--tai--wu-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=0b0d1a" alt="LinkedIn"/></a>
</p>

&nbsp;

<img src="https://img.shields.io/badge/%E2%96%B8%20ABOUT-0b0d1a?style=for-the-badge&labelColor=7c5cf0" alt="About"/>

I work on **semantic model routing**: deciding which model should serve each request, and running the decision models behind that choice fast on real GPUs. I'm a **maintainer of [vLLM Semantic Router](https://github.com/vllm-project/semantic-router)** (since Aug 2026) and an Associate Researcher at **Delta Electronics** in Taiwan. Before LLM systems, I worked on image restoration.

&nbsp;

<img src="https://img.shields.io/badge/%E2%96%B8%20BEFORE%20%E2%86%92%20AFTER-0b0d1a?style=for-the-badge&labelColor=7c5cf0" alt="Before and after"/>

| | Before | After | |
|---|---:|---:|---|
| Keyword matching, 6.7 KB Chinese prompt, 30 rules | 501 ms/op | **17 ms/op** | [#1871](https://github.com/vllm-project/semantic-router/pull/1871) |
| Recording a routing decision at 49,000 active sessions | 1.05 ms | **0.9 µs** | [#5610](https://github.com/vllm-project/semantic-router/pull/5610) |
| Host memory after loading FP8 d3-mini on NVIDIA GB10 | 3.98 GiB | **0.40 GiB** | [#5258](https://github.com/vllm-project/semantic-router/pull/5258) |
| High-confidence localization errors, d3-ultra crop eval | 50 | **10** | [#7274](https://github.com/vllm-project/semantic-router/pull/7274) |
| Redis semantic-cache hits on streaming responses | 0 / 10 | **restored** | [#2034](https://github.com/vllm-project/semantic-router/pull/2034) |

&nbsp;

<img src="https://img.shields.io/badge/%E2%96%B8%20NOW-0b0d1a?style=for-the-badge&labelColor=7c5cf0" alt="Now"/>

<table width="100%">
<thead><tr>
  <th width="33%" align="left">Decision models on NVIDIA GB10</th>
  <th width="33%" align="left">vSR for OpenCode</th>
  <th width="34%" align="left">Delta Electronics</th>
</tr></thead>
<tbody><tr>
  <td valign="top">
    Making the router's decision models run well on GB10 (arm64): NVFP4 via cuBLAS 12.9, FP8 matmuls, and a fix for long forwards that reserve twice the memory they use.
    <br/><br/>
    <sub>In review: <a href="https://github.com/vllm-project/semantic-router/pull/7152">#7152</a> · <a href="https://github.com/vllm-project/semantic-router/pull/7181">#7181</a> · next: <a href="https://github.com/vllm-project/semantic-router/issues/7275">#7275</a> · <a href="https://github.com/vllm-project/semantic-router/issues/5302">#5302</a></sub>
  </td>
  <td valign="top">
    Bringing vSR, which runs the router's decision model inside the agent harness, to OpenCode as a native plugin: model routing for child sessions, guarded commands, redaction and answer checks.
    <br/><br/>
    <sub>In review: <a href="https://github.com/vllm-project/semantic-router/pull/6688">#6688</a> · issue <a href="https://github.com/vllm-project/semantic-router/issues/6687">#6687</a></sub>
  </td>
  <td valign="top">
    Built the company's first internal coding agent (ReAct on LangGraph, RAG memory, permission-gated tools). Training a cost-aware routing model on real agent trajectories.
    <br/><br/>
    <sub>LiteLLM + Langfuse collection, labeled with LLM-as-judge</sub>
  </td>
</tr></tbody>
</table>

<sub>Paused: <code>load_aware</code> vs <code>least_request</code> needs two GPUs; single-GB10 results are in <a href="https://github.com/vllm-project/semantic-router/issues/6871">#6871</a>.</sub>

&nbsp;

<img src="https://img.shields.io/badge/%E2%96%B8%20OPEN%20SOURCE-0b0d1a?style=for-the-badge&labelColor=7c5cf0" alt="Open source"/>

Selected merged pull requests to [vllm-project/semantic-router](https://github.com/vllm-project/semantic-router):

| Area | What I shipped | Pull requests |
|---|---|---|
| **Model selection** | A per-decision selector that weighs quality, latency, cost, and in-flight load against SLO limits. Agent harnesses can ask for a fresh decision mid-session. | [#1953](https://github.com/vllm-project/semantic-router/pull/1953) · [#5617](https://github.com/vllm-project/semantic-router/pull/5617) |
| **GPU runtime** | Classifiers on NVIDIA GPUs (no silent CPU fallback), x86 and `linux/arm64` CUDA images, **65–240×** faster than CPU on an RTX 4090. Less host memory on load, idle allocator cache release on integrated GPUs, gated-delta fusion without `causal-conv1d`. | [#5615](https://github.com/vllm-project/semantic-router/pull/5615) · [#5258](https://github.com/vllm-project/semantic-router/pull/5258) · [#5892](https://github.com/vllm-project/semantic-router/pull/5892) · [#5694](https://github.com/vllm-project/semantic-router/pull/5694) |
| **Multimodal** | Image inputs for classification, evaluation, and embedding endpoints. Unit normalization after truncating embeddings. Letterboxing for wide images. | [#2104](https://github.com/vllm-project/semantic-router/pull/2104) · [#2188](https://github.com/vllm-project/semantic-router/pull/2188) · [#7274](https://github.com/vllm-project/semantic-router/pull/7274) |
| **Request path** | Session telemetry off the hot path. Streaming cache hits restored. Cancellation propagated through all six semantic-cache backends. | [#5610](https://github.com/vllm-project/semantic-router/pull/5610) · [#2034](https://github.com/vllm-project/semantic-router/pull/2034) · [#2919](https://github.com/vllm-project/semantic-router/pull/2919) |

Also in [llm-d Router](https://github.com/llm-d/llm-d-router): multimodal prefix-cache misses on salted requests ([#4138](https://github.com/llm-d/llm-d-router/pull/4138)) and early eviction of shared speculative entries ([#3701](https://github.com/llm-d/llm-d-router/pull/3701)).

<p align="center"><b><a href="https://github.com/vllm-project/semantic-router/pulls?q=is%3Apr+author%3AWUKUNTAI-0211+is%3Amerged">All merged PRs ↗</a></b></p>

&nbsp;

<img src="https://img.shields.io/badge/%E2%96%B8%20BACKGROUND-0b0d1a?style=for-the-badge&labelColor=7c5cf0" alt="Background"/>

- **M.S. Computer Science**, National Chengchi University: multi-weather image restoration with dual-modal prompts. Academia Sinica Fellowship.
- ***Restore Anything Anywhere***, IEEE MMSP 2026.

&nbsp;

<img src="https://img.shields.io/badge/%E2%96%B8%20STACK-0b0d1a?style=for-the-badge&labelColor=7c5cf0" alt="Stack"/>

<p>
  <img src="https://img.shields.io/badge/Go-0b0d1a?style=flat-square&logo=go" alt="Go"/>
  <img src="https://img.shields.io/badge/Python-0b0d1a?style=flat-square&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/Rust-0b0d1a?style=flat-square&logo=rust" alt="Rust"/>
  <img src="https://img.shields.io/badge/CUDA-0b0d1a?style=flat-square&logo=nvidia" alt="CUDA"/>
  <img src="https://img.shields.io/badge/PyTorch-0b0d1a?style=flat-square&logo=pytorch" alt="PyTorch"/>
  <img src="https://img.shields.io/badge/ONNX_Runtime-0b0d1a?style=flat-square&logo=onnx" alt="ONNX Runtime"/>
  <img src="https://img.shields.io/badge/Redis-0b0d1a?style=flat-square&logo=redis" alt="Redis"/>
  <img src="https://img.shields.io/badge/Docker-0b0d1a?style=flat-square&logo=docker" alt="Docker"/>
  <img src="https://img.shields.io/badge/LangGraph-0b0d1a?style=flat-square&logo=langchain" alt="LangGraph"/>
  <img src="https://img.shields.io/badge/MCP-0b0d1a?style=flat-square&logo=modelcontextprotocol" alt="MCP"/>
</p>

&nbsp;

<div align="center">
  <img src="assets/space-shooter.gif" alt="Space shooter game played on my contribution graph, redrawn daily" width="100%"/>
  <sub><code>request → classify → select → serve</code></sub>
</div>
