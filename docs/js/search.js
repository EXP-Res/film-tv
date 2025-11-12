/**
 * 全局搜索功能 - 跨分页搜索
 */

// 所有 section 的配置
const SECTIONS = {
    'section-01': { name: '世界奇妙物语系列', url: '../sections/section-01.html' },
    'section-02': { name: '藤原龙也系列', url: '../sections/section-02.html' },
    'section-03': { name: '憨豆先生系列', url: '../sections/section-03.html' },
    'section-04': { name: '生化危机系列', url: '../sections/section-04.html' },
    'section-05': { name: '哈利波特系列', url: '../sections/section-05.html' },
    'section-06': { name: '死神来了系列', url: '../sections/section-06.html' },
    'section-07': { name: '动画系列', url: '../sections/section-07.html' },
    'section-99': { name: '其他系列', url: '../sections/section-99.html' }
};

// 根据当前页面调整路径
function getSectionUrl(baseUrl) {
    // 检测当前页面位置
    const currentPath = window.location.pathname;
    if (currentPath.includes('/sections/')) {
        // 在 section 页面，使用相对路径
        return baseUrl.replace('../sections/', './');
    } else {
        // 在主页，使用完整路径
        return baseUrl.replace('../', './');
    }
}

// 搜索缓存
let searchCache = {};

// 初始化搜索功能
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('globalSearch');
    if (!searchInput) return;

    // 监听输入事件（防抖）
    let searchTimeout;
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();
        
        if (query.length < 2) return;
        
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 500);
    });

    // 回车键触发搜索
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            clearTimeout(searchTimeout);
            const query = e.target.value.trim();
            if (query.length >= 2) {
                performSearch(query);
            }
        }
    });
});

/**
 * 执行搜索
 */
async function performSearch(query) {
    const modal = new bootstrap.Modal(document.getElementById('searchModal'));
    const resultsContainer = document.getElementById('searchResults');
    
    resultsContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div><p class="mt-2">正在搜索...</p></div>';
    modal.show();

    try {
        const results = await searchAllSections(query);
        displaySearchResults(results, query);
    } catch (error) {
        console.error('搜索失败:', error);
        resultsContainer.innerHTML = '<div class="alert alert-danger">搜索失败，请稍后重试</div>';
    }
}

/**
 * 搜索所有分页
 */
async function searchAllSections(query) {
    const results = [];
    const lowerQuery = query.toLowerCase();

    for (const [sectionId, config] of Object.entries(SECTIONS)) {
        try {
            // 检查缓存
            let htmlContent;
            if (searchCache[sectionId]) {
                htmlContent = searchCache[sectionId];
            } else {
                // 获取 section 页面内容，使用正确的路径
                const url = getSectionUrl(config.url);
                const response = await fetch(url);
                htmlContent = await response.text();
                searchCache[sectionId] = htmlContent;
            }

            // 创建临时 DOM 解析
            const parser = new DOMParser();
            const doc = parser.parseFromString(htmlContent, 'text/html');
            
            // 搜索所有卡片
            const cards = doc.querySelectorAll('.card');
            cards.forEach(card => {
                const title = card.querySelector('.card-title')?.textContent || '';
                const description = card.querySelector('.list-group-item-primary')?.textContent || '';
                const footer = card.querySelector('.card-footer')?.textContent || '';
                
                const searchText = (title + ' ' + description + ' ' + footer).toLowerCase();
                
                if (searchText.includes(lowerQuery)) {
                    // 提取下载链接
                    const downloadBtn = card.querySelector('button[data-bs-toggle="modal"]');
                    const downloadLink = downloadBtn?.getAttribute('data-bs-download') || '';
                    
                    // 提取封面图
                    const img = card.querySelector('img');
                    const imgSrc = img?.src || '';
                    
                    results.push({
                        sectionId,
                        sectionName: config.name,
                        sectionUrl: getSectionUrl(config.url),
                        title: title.trim(),
                        description: description.trim().substring(0, 150) + '...',
                        footer: footer.trim(),
                        downloadLink,
                        imgSrc
                    });
                }
            });
        } catch (error) {
            console.error(`搜索 ${config.name} 失败:`, error);
        }
    }

    return results;
}

/**
 * 显示搜索结果
 */
function displaySearchResults(results, query) {
    const resultsContainer = document.getElementById('searchResults');
    
    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="alert alert-warning">
                <h5>未找到匹配的结果</h5>
                <p>搜索关键词 "<strong>${escapeHtml(query)}</strong>" 没有找到任何匹配的影片</p>
                <p class="mb-0 text-muted">建议：</p>
                <ul class="text-muted mb-0">
                    <li>尝试使用更简短的关键词</li>
                    <li>检查拼写是否正确</li>
                    <li>使用影片的部分名称搜索</li>
                </ul>
            </div>
        `;
        return;
    }

    let html = `<div class="alert alert-success">
        找到 <strong>${results.length}</strong> 个匹配结果，关键词: "<strong>${escapeHtml(query)}</strong>"
    </div>`;

    // 按系列分组
    const groupedResults = {};
    results.forEach(result => {
        if (!groupedResults[result.sectionName]) {
            groupedResults[result.sectionName] = [];
        }
        groupedResults[result.sectionName].push(result);
    });

    // 渲染结果
    for (const [sectionName, items] of Object.entries(groupedResults)) {
        html += `
            <h5 class="mt-4 mb-3" style="color:#ffff00; background-color:#000000; text-align: center; padding: 10px;">
                ${sectionName} (${items.length} 个结果)
            </h5>
        `;

        items.forEach(item => {
            const highlightedTitle = highlightText(item.title, query);
            const highlightedDesc = highlightText(item.description, query);
            
            html += `
                <div class="card mb-3">
                    <div class="card-body">
                        <h6 class="card-title">${highlightedTitle}</h6>
                        <p class="card-text text-muted small">${highlightedDesc}</p>
                        <div class="d-flex gap-2">
                            <a href="${item.sectionUrl}" class="btn btn-sm btn-primary" target="_blank">
                                查看系列页面
                            </a>
                            ${item.downloadLink ? `
                                <button class="btn btn-sm btn-success" onclick="window.open('${item.downloadLink}', '_blank')">
                                    直接下载
                                </button>
                            ` : ''}
                        </div>
                        <small class="text-muted">${item.footer}</small>
                    </div>
                </div>
            `;
        });
    }

    resultsContainer.innerHTML = html;
}

/**
 * 高亮匹配文本
 */
function highlightText(text, query) {
    if (!text || !query) return text;
    
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

/**
 * 转义 HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * 转义正则表达式特殊字符
 */
function escapeRegex(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// 导出函数供外部使用
window.performSearch = performSearch;
