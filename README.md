<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AdvGameBench</title>
</head>
<body>
  <h1>AdvGameBench</h1>
  <img src="docs/image/AdvGame.png" alt="AdvGameBench Architecture Diagram" />

  <h2>Why</h2>

  <h2>Install</h2>
  <pre><code>pip install -r requirements.txt</code></pre>

  <h2>Quick-start command</h2>
  <pre><code># The currently supported models are:
# chatgpt-4o, chatgpt-4.1, chatgpt-o3, chatgpt-o3-mini,
# deepSeek-V3, deepSeek-R1, qwen-plus, qwen-max,
# claude-3-5-sonnet, gemini-2-flash, gemini-2.5-flash

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
