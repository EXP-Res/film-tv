## 说明

修改下面的变量值，运行 `python py/generate_html_from_excel.py` 脚本时会自动读取这些变量，在 python 生成网站源码的同时，自动填充 html 模板中。


### html 页面标题和提示

> 影响 `index.html`, `sections/*`

```
SITE_TITLE=九〇后的精选影视 - 导航主页

INDEX_TITLE=📺 九〇后的精选影视 📺

HEADER_EXPLANATION=本站所有资源下载均需 <a target="_blank" href="https://www.7-zip.org/">7-Zip</a> 工具解压<br/>如遇解压密码错误，可加 QQ 群 209442520 处理
```



### SEO 配置（用于优化搜索引擎推荐排名）

> 影响 `docs/js/seo-meta.js`


```
SEO_TITLE=90后的经典影视 - 童年回忆 世界奇妙物语、动漫系列、哈利波特在线观看下载

SEO_DESCRIPTION=90后回忆，绝版经典影视作品大全。包含世界奇妙物语、刀剑神域SAO、Re0从零开始、Fate系列、钢之炼金术师、死亡笔记、一拳超人、东京喰种、寄生兽、中华一番、加速世界、哈利波特、生化危机、死神来了、藤原龙也系列、憨豆先生等。提供高清下载，中文字幕，mp4格式。

SEO_KEYWORDS=90后,童年,回忆,绝版,经典动漫,刀剑神域,Re0从零开始,Fate系列,钢之炼金术师,死亡笔记,一拳超人,东京喰种,寄生兽,中华一番,加速世界,仙境传说RO,疯狂动物城,世界奇妙物语,哈利波特,生化危机,死神来了,藤原龙也,憨豆先生,海扁王,经典电影,电影下载,高清电影,中文字幕,经典影视,日本动漫,热血动漫,治愈动漫

SEO_AUTHOR=Classic Film & TV

SEO_SITE_NAME=经典影视作品大全

SEO_DOMAIN=https://exp-res.github.io/film-tv/

SEO_IMAGE=./docs/movies.png

SEO_LOCALE=zh_CN
```

