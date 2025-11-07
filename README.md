# 🧱 TyporaImageSync | Typora 图像同步助手

> 一键上传 Typora 本地图片到阿里云 OSS，并生成适合 CSDN、掘金、知乎导入的 Markdown 文件。

---
## 😮背景
      之前我遇到了一个比较棘手的问题，是这样的，我平常喜欢写博客，通常使用Typora写md文档，为了上传到github时候图片能够正常显示，我在Typora中设置我复制到文档中的图片会自动拷贝到与文档同级目录的images文件夹下，这一切看起来都非常合理，但是我很快发现了新的问题，当我在CSDN博客平台导入我的这个md文档时候，由于所有的图片路径为./images/xxx.png的本地相对路径，CSDN均无法识别并将图片正常展示正常展示。于是我想了一个方案，写一个python脚本，输入md文档的本地绝对路径，然后就可以自动将images文件夹下的图片上传到阿里云oss等图床，并且使用返回的网络路径替换md文档里面对应的图片路径，为我生成一个新的，可以导入csdn等博客平台的新md文件，说干就干，借助于chatgpt，很快就完成了这一小工具，哈哈。

      I encountered a tricky problem before, it is like this, I usually like to write blogs, usually use Typora to write md documents, in order to upload to github when the pictures can be displayed normally, I set the pictures I copied to the document in Typora will be automatically copied to the images folder of the same level directory as the document, all this seems very reasonable, but I quickly found a new problem, when I imported my md document on the CSDN blog platform, Since all image paths are local relative paths of ./images/xxx.png, CSDN cannot recognize and display the images normally. So I thought of a solution, write a python script, enter the local absolute path of the MD document, and then you can automatically upload the images in the images folder to Alibaba Cloud OSS and other image beds, and use the returned network path to replace the corresponding image path in the MD document, and generate a new MD file for me, which can be imported into CSDN and other blog platforms.



## 🚀 功能特点

✅ 自动扫描 Typora `.md` 文件中的本地图片路径（默认 `./images/`）  
✅ 将图片批量上传至 **阿里云 OSS**（后续可能支持其他图床）  
✅ 自动替换 Markdown 中的本地路径为可公网访问的链接  
✅ 生成适合直接导入 CSDN 的新 `.md` 文件  
✅ 支持自定义上传目录、日志输出与异常捕获  

---

## 🧩 示例效果

源文件示例：

```markdown
![](./images/demo.png)
```

执行脚本后自动替换为：

```
![](https://your-bucket.oss-cn-hangzhou.aliyuncs.com/blog_images/demo.png)
```

------

## ⚙️ 安装与使用

### 1️⃣ 克隆项目

```
git clone https://github.com/05Huang/typora-image-sync.git
cd typora-image-sync
```

### 2️⃣ 安装依赖

> 通过 `requirements.txt` 一键安装所有依赖：

```
pip install -r requirements.txt
```

> 或者手动安装：

```
pip install oss2 tqdm
```

### 3️⃣ 配置阿里云 OSS 信息

修改文件 `config.json`：

```
{
  "endpoint": "https://oss-cn-hangzhou.aliyuncs.com",
  "access_key_id": "your-access-key-id",
  "access_key_secret": "your-access-key-secret",
  "bucket_name": "your-bucket-name",
  "oss_folder": "blog_images"
}
```

### 4️⃣ 运行脚本

```
python typora_image_sync.py
```

输入 `.md` 文件路径，例如：

```
请输入 Markdown 文件路径: D:\Blog\CacheNote\redis_cache.md
```

### 5️⃣ 输出结果

程序将在同目录下生成：

```
redis_cache_for_oss.md
```

------

## 🧱 项目结构

```
typora-image-sync/
├── typora_image_sync.py   # 主脚本
├── config.json            # 阿里云配置文件
├── requirements.txt       # 依赖包
└── README.md              # 项目说明文档
```

------

## 🪶 常见问题

**Q1：CSDN 图片无法显示？**
 A：确保 OSS 对应 bucket 的图片资源是公共可读（Public Read）。

**Q2：能否支持 GitHub 图床？**
 A：后续版本计划支持 **SM.MS、GitHub、七牛云** 等图床切换。

**Q3：Typora 图片路径不是 ./images？**
 A：可以修改 `re.compile` 的匹配规则以适配不同路径。

------

## 💖 Star 支持

如果你觉得这个工具对你有帮助，请点个 **⭐Star 支持**！
 这会帮助我持续优化并开放更多功能！

------

## 📄 License

MIT License © 2025 05Huang