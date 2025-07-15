
</head>
<body>
  <h1>AdvGameBench</h1>
  <img src="docs/image/AdvGame.png" alt="AdvGameBench Architecture Diagram" />

<p align="center">
  <!-- arXiv -->
  <a href="https://arxiv.org/pdf/2506.12012" target="_blank">
    <img
      src="https://img.shields.io/badge/arXiv-2506.12012-E92D20?logo=arxiv&logoColor=white&style=flat-square"
      alt="arXiv:2506.12012"
      height="25" />
  </a>

<a href="https://huggingface.co/spaces/xiaopengyuan/AdvGameBench" target="_blank">
  <img
    alt="🤗 AdvGameBench"
    src="https://img.shields.io/badge/🤗_Leaderboard-AdvGameBench-ffc107?color=ffc107"
    height="25" />
</a>
</p>

  AdvGameBench is a benchmark that evaluates how LLMs make and revise decisions in strategic games, focusing not just on win rates but on the reasoning process behind those decisions.

  <h2>Why use AdvGameBench?</h2>
  Most benchmarks evaluate LLMs based only on final outcomes like accuracy or win rate, without considering how those results are produced. AdvGameBench addresses this limitation by placing models in closed-loop environments where they must plan, revise, and make decisions under constraints. By tracing not just what the model decides, but how and why it does so, AdvGameBench offers deeper insights into reasoning quality, reliability, and self-correction behavior.

  <h2>Install</h2>
  <h3>Method 1: With pip</h3>
  <pre><code>pip install -r requirements.txt</code></pre>

  <h2>APIS</h2>
  <p>The currently supported models are:</p>
  <ul>
    <li>chatgpt-4o</li>
    <li>chatgpt-4.1</li>
    <li>chatgpt-o3</li>
    <li>chatgpt-o3-mini</li>
    <li>deepSeek-V3</li>
    <li>deepSeek-R1</li>
    <li>qwen-plus</li>
    <li>qwen-max</li>
    <li>claude-3-5-sonnet</li>
    <li>gemini-2-flash</li>
    <li>gemini-2.5-flash</li>
  </ul>

  <h2>Quick-start command</h2>
  <pre><code>

python run_all.py \
    --games "Tower_Defense" "Auto-battler" "Turn-based" \
    --models "chatgpt-4o" \
    --fix-models "deepSeek-V3" \
    --rounds 4 \
    --parallel

# Environment variables
OPENAI_API_KEY="YOUR_KEY_HERE"
DEEPSEEK_API_KEY="..."
QWEN_API_KEY="..."
CLAUDE_API_KEY="..."
GEMINI_API_KEY="..."</code></pre>
</body>
</html>

<h2>Citation</h2>
<p>If you find this repository helpful, please kindly cite:</p>

<pre><code>@article{yuan2025advgamebench,
  title={Tracing LLM Reasoning Processes with Strategic Games: A Framework for Planning, Revision, and Resource-Constrained Decision Making},
  author={Yuan, Xiaopeng and Zhang, Xingjian and Xu, Ke and Xu, Yifan and Yu, Lijun and Wang, Jindong and Dong, Yushun and Wang, Haohan},
  journal={arXiv preprint arXiv:2506.12012},
  year={2025}
}
</code></pre>