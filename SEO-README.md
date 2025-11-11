# SEO 优化指南

本项目包含完整的 SEO 优化配置，帮助搜索引擎更好地索引和展示网站内容。

## 📁 文件说明

### 1. robots.txt
位置：`/robots.txt`

**作用**：告诉搜索引擎爬虫哪些内容可以索引
- ✅ 允许所有搜索引擎访问网站
- ❌ 禁止索引保护脚本
- 📍 指向 sitemap.xml 的位置

**使用方法**：
1. 打开 `robots.txt`
2. 将所有 `https://yourdomain.com` 替换为实际域名
3. 上传到网站根目录

### 2. sitemap.xml
位置：`/sitemap.xml`

**作用**：网站地图，列出所有重要页面供搜索引擎索引
- 包含主页和所有影视系列章节
- 设置了更新频率和优先级
- 自动生成最后修改时间

**使用方法**：
1. 打开 `sitemap.xml`
2. 将所有 `https://yourdomain.com` 替换为实际域名
3. 更新 `<lastmod>` 日期为当前日期
4. 上传到网站根目录

### 3. seo-meta.js
位置：`/docs/js/seo-meta.js`

**作用**：动态管理所有 SEO 元标签
- 页面标题、描述、关键词
- Open Graph（社交媒体分享）
- Twitter Card
- 结构化数据（JSON-LD）
- 多语言支持

**使用方法**：
```javascript
// 编辑配置对象
const seoConfig = {
    title: '你的网站标题',
    description: '你的网站描述',
    keywords: '关键词1,关键词2,关键词3',
    domain: 'https://your-domain.com', // 👈 修改这里
    // ...
};
```

### 4. sitemap-generator.js
位置：`/docs/js/sitemap-generator.js`

**作用**：自动生成和更新 sitemap.xml

**使用方法**：
```javascript
// 在浏览器控制台（F12）运行以下命令

// 1. 检查配置
SitemapGenerator.checkConfig();

// 2. 预览 sitemap 内容
SitemapGenerator.preview();

// 3. 生成并下载 sitemap.xml
SitemapGenerator.generate();
```

## 🚀 快速开始

### 第一步：修改域名配置

需要在以下文件中将 `https://yourdomain.com` 替换为实际域名：

1. `robots.txt` (第 11 行)
2. `sitemap.xml` (所有 `<loc>` 标签)
3. `docs/js/seo-meta.js` (第 15 行)
4. `docs/js/sitemap-generator.js` (第 14 行)

### 第二步：上传文件

确保以下文件位于网站根目录：
```
your-website/
├── index.html
├── robots.txt          ← 必须在根目录
├── sitemap.xml         ← 必须在根目录
└── docs/
    └── js/
        ├── seo-meta.js
        └── sitemap-generator.js
```

### 第三步：验证配置

1. 访问 `https://your-domain.com/robots.txt` 确认可访问
2. 访问 `https://your-domain.com/sitemap.xml` 确认可访问
3. 使用 F12 开发者工具查看网页源代码，确认 SEO 标签已正确加载

## 📊 提交到搜索引擎

### Google Search Console
1. 访问：https://search.google.com/search-console
2. 添加网站并验证所有权
3. 提交 sitemap：`https://your-domain.com/sitemap.xml`

### Bing Webmaster Tools
1. 访问：https://www.bing.com/webmasters
2. 添加网站并验证所有权
3. 提交 sitemap

### 百度站长平台
1. 访问：https://ziyuan.baidu.com/
2. 添加网站并验证所有权
3. 提交 sitemap

### 其他搜索引擎
- 360搜索：https://zhanzhang.so.com/
- 搜狗搜索：http://zhanzhang.sogou.com/
- 神马搜索：https://zhanzhang.sm.cn/

## 🔧 更新 Sitemap

### 方法1：使用自动生成器（推荐）

```javascript
// 1. 在页面上按 F12 打开控制台
// 2. 运行命令
SitemapGenerator.generate();
// 3. 下载生成的 sitemap.xml
// 4. 上传到网站根目录
```

### 方法2：手动编辑

1. 打开 `sitemap.xml`
2. 添加新的 URL 条目：
```xml
<url>
  <loc>https://your-domain.com/#section-new</loc>
  <lastmod>2025-11-12</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.9</priority>
</url>
```
3. 更新所有 `<lastmod>` 为当前日期
4. 重新上传到网站

## 📈 优先级说明

sitemap.xml 中的优先级设置：

- `1.0` - 主页（最高优先级）
- `0.9` - 重要系列（世界奇妙物语、哈利波特、生化危机等）
- `0.8` - 次要系列（憨豆先生等）
- `0.7` - 其他内容

## 🔄 更新频率说明

- `always` - 每次访问都变化
- `hourly` - 每小时
- `daily` - 每天
- `weekly` - 每周（主页）
- `monthly` - 每月（系列页面）
- `yearly` - 每年
- `never` - 从不

## ✅ SEO 检查清单

- [ ] 所有文件中的域名已替换为实际域名
- [ ] robots.txt 已上传到根目录
- [ ] sitemap.xml 已上传到根目录
- [ ] 在 Google Search Console 中提交了 sitemap
- [ ] 在 Bing Webmaster Tools 中提交了 sitemap
- [ ] 页面标题包含关键词（60字符内）
- [ ] meta description 准确描述页面（155字符内）
- [ ] 所有图片都有 alt 属性
- [ ] 网站支持 HTTPS
- [ ] 网站适配移动设备
- [ ] 页面加载速度良好（< 3秒）

## 🛠️ 常见问题

### Q: 修改 sitemap 后需要重新提交吗？
A: 是的，建议在 Search Console 中重新提交，或等待搜索引擎自动重新抓取。

### Q: robots.txt 修改后多久生效？
A: 通常几小时到几天，取决于搜索引擎爬虫的访问频率。

### Q: 如何检查 SEO 标签是否正确？
A: 
1. F12 打开开发者工具
2. 切换到 "Elements" 标签页
3. 查看 `<head>` 部分的 meta 标签

### Q: 如何验证 sitemap 是否有效？
A: 使用在线工具验证：
- https://www.xml-sitemaps.com/validate-xml-sitemap.html
- Google Search Console 的 Sitemap 报告

## 📚 相关资源

- [Google SEO 入门指南](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Sitemap 协议](https://www.sitemaps.org/protocol.html)
- [robots.txt 规范](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- [Schema.org 结构化数据](https://schema.org/)

## 📞 技术支持

如有问题，可以：
1. 查看浏览器控制台的错误信息
2. 使用 Google Search Console 的调试工具
3. 检查网站访问日志

---

最后更新：2025-11-12
