/**
 * SEO 元标签管理
 * 动态插入页面的 SEO 优化标签
 */

(function() {
    'use strict';

    // SEO 配置
    const seoConfig = {
        // 基础信息
        title: '90后的经典影视 - 童年回忆 世界奇妙物语、动漫系列、哈利波特在线观看下载',
        description: '90后童年回忆，绝版经典影视作品大全。包含世界奇妙物语、刀剑神域SAO、Re0从零开始、Fate系列、钢之炼金术师、死亡笔记、一拳超人、东京喰种、寄生兽、中华一番、加速世界、哈利波特、生化危机、死神来了、藤原龙也系列、憨豆先生等。提供高清下载，中文字幕，mp4格式。',
        keywords: '90后,童年,回忆,绝版,经典动漫,刀剑神域,Re0从零开始,Fate系列,钢之炼金术师,死亡笔记,一拳超人,东京喰种,寄生兽,中华一番,加速世界,仙境传说RO,疯狂动物城,世界奇妙物语,哈利波特,生化危机,死神来了,藤原龙也,憨豆先生,海扁王,经典电影,电影下载,高清电影,中文字幕,经典影视,日本动漫,热血动漫,治愈动漫',
        author: 'Classic Film & TV',
        siteName: '经典影视作品大全',
        domain: 'https://yourdomain.com', // 请替换为实际域名
        image: './docs/movies.png',
        locale: 'zh_CN',
        
        // 影视系列列表
        movieSeries: [
            { name: '世界奇妙物语系列', description: '日本经典悬疑短剧系列' },
            { name: '刀剑神域 SAO 系列', description: '热血异世界冒险动漫，90后童年回忆' },
            { name: 'Re0 从零开始的异世界生活', description: '治愈系穿越动漫经典' },
            { name: 'Fate 系列', description: '命运之夜圣杯战争史诗巨作' },
            { name: '钢之炼金术师系列', description: '经典热血炼金术冒险动漫' },
            { name: '死亡笔记', description: '智斗悬疑推理神作' },
            { name: '一拳超人系列', description: '爆笑热血超级英雄动漫' },
            { name: '东京喰种系列', description: '黑暗奇幻生存动漫' },
            { name: '寄生兽', description: '经典科幻惊悚动漫' },
            { name: '中华一番', description: '童年回忆美食料理动漫' },
            { name: '加速世界', description: '虚拟现实科幻动漫' },
            { name: '仙境传说 RO', description: '网游改编经典动漫' },
            { name: '哈利波特系列', description: '魔法世界经典电影八部曲' },
            { name: '生化危机系列', description: '末日生存惊悚动作电影系列' },
            { name: '死神来了系列', description: '经典恐怖悬疑电影系列' },
            { name: '藤原龙也系列', description: '日本实力派演员主演作品集' },
            { name: '憨豆先生系列', description: '英国经典喜剧电影系列，童年回忆' }
        ]
    };

    /**
     * 创建 meta 标签
     */
    function createMetaTag(attrs) {
        const meta = document.createElement('meta');
        Object.keys(attrs).forEach(key => {
            meta.setAttribute(key, attrs[key]);
        });
        return meta;
    }

    /**
     * 创建 link 标签
     */
    function createLinkTag(attrs) {
        const link = document.createElement('link');
        Object.keys(attrs).forEach(key => {
            link.setAttribute(key, attrs[key]);
        });
        return link;
    }

    /**
     * 插入 SEO 元标签
     */
    function insertSEOTags() {
        const head = document.head;
        const fragment = document.createDocumentFragment();

        // 更新 title
        document.title = seoConfig.title;

        // 基础 SEO 标签
        const basicMetaTags = [
            { name: 'description', content: seoConfig.description },
            { name: 'keywords', content: seoConfig.keywords },
            { name: 'author', content: seoConfig.author },
            { name: 'robots', content: 'index, follow' },
            { name: 'googlebot', content: 'index, follow' },
            { name: 'bingbot', content: 'index, follow' }
        ];

        basicMetaTags.forEach(attrs => {
            fragment.appendChild(createMetaTag(attrs));
        });

        // Open Graph 标签
        const ogTags = [
            { property: 'og:title', content: seoConfig.title },
            { property: 'og:description', content: seoConfig.description },
            { property: 'og:type', content: 'website' },
            { property: 'og:image', content: seoConfig.image },
            { property: 'og:site_name', content: seoConfig.siteName },
            { property: 'og:locale', content: seoConfig.locale }
        ];

        ogTags.forEach(attrs => {
            fragment.appendChild(createMetaTag(attrs));
        });

        // Twitter Card 标签
        const twitterTags = [
            { name: 'twitter:card', content: 'summary_large_image' },
            { name: 'twitter:title', content: seoConfig.title },
            { name: 'twitter:description', content: seoConfig.description },
            { name: 'twitter:image', content: seoConfig.image }
        ];

        twitterTags.forEach(attrs => {
            fragment.appendChild(createMetaTag(attrs));
        });

        // 移动设备优化
        const mobileTags = [
            { name: 'mobile-web-app-capable', content: 'yes' },
            { name: 'apple-mobile-web-app-capable', content: 'yes' },
            { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }
        ];

        mobileTags.forEach(attrs => {
            fragment.appendChild(createMetaTag(attrs));
        });

        // 语言和地区链接
        const langLinks = [
            { rel: 'alternate', hreflang: 'zh-CN', href: seoConfig.domain + '/' },
            { rel: 'alternate', hreflang: 'zh-TW', href: seoConfig.domain + '/' },
            { rel: 'alternate', hreflang: 'zh-HK', href: seoConfig.domain + '/' }
        ];

        langLinks.forEach(attrs => {
            fragment.appendChild(createLinkTag(attrs));
        });

        // Apple Touch Icon
        fragment.appendChild(createLinkTag({
            rel: 'apple-touch-icon',
            href: './docs/favicon.png'
        }));

        // 插入到 head 中
        head.appendChild(fragment);

        // 插入结构化数据
        insertStructuredData();
    }

    /**
     * 插入结构化数据（JSON-LD）
     */
    function insertStructuredData() {
        // WebSite 结构化数据
        const websiteSchema = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": seoConfig.siteName,
            "description": seoConfig.description,
            "url": seoConfig.domain,
            "potentialAction": {
                "@type": "SearchAction",
                "target": seoConfig.domain + "/search?q={search_term_string}",
                "query-input": "required name=search_term_string"
            }
        };

        // ItemList 结构化数据
        const itemListSchema = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": "经典影视系列",
            "description": "包含多个经典影视系列的精选合集",
            "itemListElement": seoConfig.movieSeries.map((series, index) => ({
                "@type": "ListItem",
                "position": index + 1,
                "item": {
                    "@type": "Movie",
                    "name": series.name,
                    "description": series.description
                }
            }))
        };

        // 创建并插入 script 标签
        [websiteSchema, itemListSchema].forEach(schema => {
            const script = document.createElement('script');
            script.type = 'application/ld+json';
            script.textContent = JSON.stringify(schema, null, 2);
            document.head.appendChild(script);
        });
    }

    /**
     * 初始化
     */
    function init() {
        // DOM 加载完成后执行
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', insertSEOTags);
        } else {
            insertSEOTags();
        }
    }

    // 执行初始化
    init();

    // 导出配置（可选，用于其他脚本访问）
    window.SEOConfig = seoConfig;

})();
