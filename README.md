# AdvGameBench
![AdvGameBench 架构图](docs/image/advgame_page1.png)



# install the exact package versions used in the paper
pip install -r requirements.txt


# Quick‑start command
# The currently supported models are: chatgpt-4o, chatgpt-4.1, chatgpt-o3, chatgpt-o3-mini, deepSeek-V3, deepSeek-R1, qwen-plus, qwen-max, claude-3-5-sonnet, gemini-2-flash, gemini-2.5-flash
python run_all.py \
    --games "Tower_Defense" "Auto-battler" "Turn-based" \
    --models "chatgpt-4o" \
    --fix-models "deepSeek-V3" \
    --rounds 4 \
    --parallel

OPENAI_API_KEY="YOUR_KEY_HERE"
DEEPSEEK_API_KEY="..."
QWEN_API_KEY="..."
CLAUDE_API_KEY="..."
GEMINI_API_KEY="..."