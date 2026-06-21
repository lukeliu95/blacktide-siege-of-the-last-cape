#!/usr/bin/env bash
# gen-music.sh — Mia 的音乐生成能力(Gemini Lyria)
# 用 Gemini lyria-3-clip-preview(30s 片段)/ lyria-3-pro-preview 文生音乐 → MP3
#
# 用法:
#   bash gen-music.sh "Dark cinematic war orchestral ambient, slow drums, no vocals" out.mp3 [model]
#   model 缺省 lyria-3-clip-preview;可传 lyria-3-pro-preview
#
# 鉴权:GEMINI_API_KEY(从 env 或 local/gei-memory/api-keys.env)
# 返回:audio/mpeg(MP3)base64 → 解码落盘。模型只出乐器(<instrumental>),无人声。
set -euo pipefail

PROMPT="${1:?prompt required}"
OUT="${2:?output path required}"
MODEL="${3:-lyria-3-clip-preview}"

# 载入 key
if [ -z "${GEMINI_API_KEY:-}" ]; then
  for f in "$HOME/gei-workspace/local/gei-memory/api-keys.env" "./.env"; do
    [ -f "$f" ] && { set -a; . "$f"; set +a; }
  done
fi
[ -n "${GEMINI_API_KEY:-}" ] || { echo "GEMINI_API_KEY 缺失" >&2; exit 1; }

BODY=$(python3 -c '
import json,sys
print(json.dumps({
  "contents":[{"role":"user","parts":[{"text":sys.argv[1]}]}],
  "generationConfig":{"responseModalities":["AUDIO"]}
}))' "$PROMPT")

RESP=$(mktemp)
HTTP=$(curl -s -w "%{http_code}" -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" -d "$BODY" -o "$RESP")

[ "$HTTP" = "200" ] || { echo "HTTP $HTTP" >&2; head -c 400 "$RESP" >&2; exit 1; }

python3 -c '
import json,base64,sys
d=json.load(open(sys.argv[1]))
if "error" in d: sys.exit("API error: "+json.dumps(d["error"])[:300])
for p in d["candidates"][0]["content"]["parts"]:
    if "inlineData" in p:
        open(sys.argv[2],"wb").write(base64.b64decode(p["inlineData"]["data"]))
        print("OK ->",sys.argv[2]); break
else: sys.exit("no audio part in response")
' "$RESP" "$OUT"
rm -f "$RESP"
