(async function() {
    var cards = document.querySelectorAll('li.job-card-box');
    if (!cards.length) return '[]';

    var results = [];
    var MAX_TIME = 120000; // 2 min max total
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
            var ds = body.indexOf('职位描述');
            var d = '';
            if (ds > -1) {
                var de = body.indexOf('工作地址', ds);
                d = body.substring(ds, de > ds ? de : ds + 2500).replace(/\n/g, ' ').trim();
            }

            if (n && n.length > 2 && n.length < 120) {
                results.push({n: n, s: s, d: d.substring(0, 2500)});
            }
        } catch(e) {}
    }
    return JSON.stringify(results);
})()
