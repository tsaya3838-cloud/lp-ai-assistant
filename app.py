import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types 

# ログの設定
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_lp_assistant(file_path, platform):
    try:
        load_dotenv()
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        
        logging.info(f"解析開始：ファイル={file_path}, プラットフォーム={platform}")
        print(f"⏳ {platform}向けに {file_path} を解析中...")

        # 1. ファイルを読み込む
        with open(file_path, "rb") as f:
            file_data = f.read()
        
        # 2. 拡張子からMIMEタイプを判別
        ext = os.path.splitext(file_path)[1].lower()
        m_type = "audio/mp4" if ext in [".m4a", ".mp4"] else "image/jpeg"

        # 3. プラットフォームに合わせた動的な指示文（プロンプト）
        prompt = f"""
        あなたは {platform} 専門の制作ディレクターです。
        提供されたデータを分析し、{platform} のユーザー層に最も刺さる以下の3点を作成してください。
        
        1. 【LPセクション構成】
           - {platform} の文化（応援、スペック重視、社会貢献など）に合わせた構成案。
           
        2. 【ビジュアル・ワイヤーフレーム（Mermaid形式）】
           - ページの縦の流れを視覚化するためのコードを ```mermaid と ``` で囲んで出力してください。
           - 各セクションに「配置する画像案」と「キャッチコピー」を含めること。
           
        3. 【デザイン指示】
           - {platform} のトーン＆マナーに合う配色、フォント、必要な写真リスト。
        """

        # 4. 送信と生成
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=file_data, mime_type=m_type),
                prompt
            ]
        )

        # 5. 保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"result_{platform}_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"\n✅ 解析完了！ '{filename}' を確認してください。")
        print(f"💡 Mermaidコードをコピーして https://mermaid.live/ に貼ると図解が見れます。")

    except Exception as e:
        error_msg = f"エラーが発生しました: {str(e)}"
        print(error_msg)
        logging.error(error_msg)

if __name__ == "__main__":
    # --------------------------------------------------
    # ここを書き換えて実行してください
    # --------------------------------------------------
    target_file = "sample_voice.m4a" 
    target_platform = "GREEN FUNDING"  # 例: "Makuake", "GREEN FUNDING", "CAMPFIRE"
    
    if os.path.exists(target_file):
        run_lp_assistant(target_file, target_platform)
    else:
        print(f"❌ ファイル '{target_file}' が見つかりません。")