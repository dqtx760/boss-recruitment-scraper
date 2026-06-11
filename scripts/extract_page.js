(async function() {
    var cards = document.querySelectorAll('li.job-card-box');
    if (!cards.length) return '[]';

    var results = [];
    var MAX_TIME = 120000;
    var startTime = Date.now();

    for (var i = 0; i < cards.length; i++) {
        if (Date.now() - startTime > MAX_TIME) break;
        try {
            var card = cards[i];
            card.click();
            await new Promise(function(r) { setTimeout(r, 600); });

            var txt = card.textContent.trim();
            var m = txt.match(/(\d+-\d+K[^\s]{0,15})/);
            var s = m ? m[1] : '';
            var n = txt.replace(/(\d+-\d+K[^\s]{0,15}.*)$/, '').replace(/\s+(经验不限|应届|学历不限|\d+-\d+年|本科|硕士|博士|大专).*$/, '').trim();

            var body = document.body.innerText;

            // Description: from 职位描述 to 工作地址
            var ds = body.indexOf('职位描述');
            var d = '';
            if (ds > -1) {
                var de = body.indexOf('工作地址', ds);
                d = body.substring(ds, de > ds ? de : ds + 2500).replace(/\n/g, ' ').trim();
            }

            // Address: from 工作地址 to 点击查看地图
            var addr = '';
            var as = body.indexOf('工作地址');
            if (as > -1) {
                var ae = body.indexOf('点击查看地图', as);
                if (ae === -1) ae = body.indexOf('查看地图', as);
                if (ae === -1) ae = body.indexOf('查看更多', as);
                if (ae === -1) ae = as + 300;
                addr = body.substring(as, ae).replace('工作地址：', '').replace('工作地址', '').replace(/\n/g, ' ').trim();
            }

            if (n && n.length > 2 && n.length < 120) {
                results.push({n: n, s: s, d: d.substring(0, 2500), a: addr});
            }
        } catch(e) {}
    }
    return JSON.stringify(results);
})()
