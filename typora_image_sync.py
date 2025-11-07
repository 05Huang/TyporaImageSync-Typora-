import os
import re
import sys
import json
import logging
import oss2
from tqdm import tqdm

# ---------------- Logger 配置 ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ---------------- 配置加载 ----------------
CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        logger.error(f"❌ 未找到配置文件 {CONFIG_FILE}，请先创建。")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------- OSS 上传逻辑 ----------------
def upload_image(bucket, local_path, oss_folder):
    filename = os.path.basename(local_path)
    oss_path = f"{oss_folder.rstrip('/')}/{filename}"

    try:
        bucket.put_object_from_file(oss_path, local_path)
        url = f"https://{bucket.bucket_name}.{bucket.endpoint.replace('https://', '')}/{oss_path}"
        logger.info(f"✅ 上传成功：{filename}")
        return url
    except Exception as e:
        logger.error(f"⚠️ 上传失败：{filename}，原因：{e}")
        return None

# ---------------- Markdown 处理逻辑 ----------------
def process_markdown(md_path, bucket, oss_folder):
    base_dir = os.path.dirname(md_path)
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(r'!\[.*?\]\((\.\/images\/[^\)]+)\)')
    matches = pattern.findall(content)

    if not matches:
        logger.warning("⚠️ 未检测到图片路径 './images/'。")
        return

    logger.info(f"🖼️ 检测到 {len(matches)} 张图片，开始上传至 OSS...")
    url_map = {}

    for match in tqdm(matches):
        local_path = os.path.join(base_dir, match.replace("./", ""))
        if not os.path.exists(local_path):
            logger.warning(f"找不到文件：{local_path}")
            continue

        url = upload_image(bucket, local_path, oss_folder)
        if url:
            url_map[match] = url

    for local, remote in url_map.items():
        content = content.replace(local, remote)

    new_path = md_path.replace(".md", "_for_oss.md")
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"🎉 已生成新文件：{new_path}")

# ---------------- 主入口 ----------------
if __name__ == "__main__":
    cfg = load_config()

    endpoint = cfg["endpoint"]
    access_key_id = cfg["access_key_id"]
    access_key_secret = cfg["access_key_secret"]
    bucket_name = cfg["bucket_name"]
    oss_folder = cfg.get("oss_folder", "blog_images")

    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    md_path = input("请输入 Markdown 文件路径: ").strip()
    if not os.path.exists(md_path):
        logger.error("❌ 文件不存在，请检查路径。")
        sys.exit(1)

    process_markdown(md_path, bucket, oss_folder)
