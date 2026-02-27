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
        description: '90后回忆，绝版经典影视作品大全。包含世界奇妙物语、刀剑神域SAO、Re0从零开始、Fate系列、钢之炼金术师、死亡笔记、一拳超人、东京喰种、寄生兽、中华一番、加速世界、哈利波特、生化危机、死神来了、藤原龙也系列、憨豆先生等。提供高清下载，中文字幕，mp4格式。',
        keywords: '90后,童年,回忆,绝版,经典动漫,刀剑神域,Re0从零开始,Fate系列,钢之炼金术师,死亡笔记,一拳超人,东京喰种,寄生兽,中华一番,加速世界,仙境传说RO,疯狂动物城,世界奇妙物语,哈利波特,生化危机,死神来了,藤原龙也,憨豆先生,海扁王,经典电影,电影下载,高清电影,中文字幕,经典影视,日本动漫,热血动漫,治愈动漫',
        author: 'Classic Film & TV',
        siteName: '经典影视作品大全',
        domain: 'https://exp-res.github.io/film-tv/', // 请替换为实际域名
        image: './docs/movies.png',
        locale: 'zh_CN',
        
        // 影视系列列表
        movieSeries: [
            { name: '世界奇妙物语系列', description: '包含TV版三季及1990-2025年特别篇，涵盖日本最经典的悬疑短篇集锦剧' },
            { name: '藤原龙也系列', description: '日本实力派演员藤原龙也主演作品集，包含《死亡笔记》《大逃杀》等经典' },
            { name: '憨豆先生系列', description: '英国喜剧大师罗温·艾金森经典作品，无需语言也能笑到肚子疼' },
            { name: '生化危机系列', description: '米拉·乔沃维奇主演的动作科幻大片，改编自同名游戏的经典电影系列' },
            { name: '哈利波特系列', description: 'J.K.罗琳魔法世界的完整电影系列，陪伴一代人成长的魔法传奇' },
            { name: '死神来了系列', description: '死神要你三更死，不得留人到五更！经典惊悚系列，环环相扣的死亡链条，笑到喷血浆的离奇死亡方式' },
            { name: '数码暴龙系列', description: '暑假被电脑拐跑到怪兽服务器，小学生一脚踏进会蓝屏的虚拟世界，输出全靠喊，要如何拯救两个世界？' },
            { name: '推理探案系列', description: '死神小学生几十年如一日在凶案现场破案，名侦探柯南和金田一带你走进柯学的杂技世界' },
            { name: '异世界系列', description: '今天死在异世界的是哪一回？带着只能读档不能存档的废柴能力，体验一场用命拼出来的压力试炼' },
            { name: '竞速赛车系列', description: '深夜送豆腐顺便虐车神，山路发卡弯当直线开，藤原拓海带你体验一场靠重力和排水渠极限下坡的死亡公路之旅' },
            { name: '超人英雄系列', description: '认真就会输的秃头英雄，每天打工顺手把世界清零，埼玉带你见识无敌也无法避免面临财务危机的英雄社会学' },
            { name: '游戏王系列', description: '我100点生命稳如老狗、你10000点生命犹如风中残烛，口胡打牌也能拯救世界？代代相传的不仅是名字和发型，还有印刷绝技！' },
            { name: '三大民工漫', description: '打工人下班追了十年热血，死神火影海贼王陪你见证从拼修行到拼爹开挂的热血进化史' },
            { name: 'JOJO 系列', description: '一条家族血脉打八代怪人，从英国鬼故事一路打到宇宙歌剧，JOJO 把"气氛到位就算合理"演成视觉圣经' },
            { name: '宠物小精灵系列', description: '十岁就被赶出家环游世界，把小动物塞进精灵球里互相斗殴，离家出走一走就是 25 年终于走到功成名就' },
            { name: '哆啦 A 梦系列', description: '来自 22 世纪的蓝胖子专门用道具帮小学生逃避人生，"如果有这种道具就好了"成为一代人的童年妄想实录' },
            { name: '精选动画系列', description: '90 后必看动漫合集！仙境传说、Re0、Fate、钢炼、死亡笔记、东京喰种等热血治愈神作全收录' },
            { name: '其他系列', description: '不容错过的独立佳作！《打机王》怀旧经典、《疯狂动物城》温馨治愈，每部都是精品' }
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
