(function() {
    var active = document.querySelector('li.job-card-box.active');
    if (!active) active = document.querySelector('li.job-card-box');
    if (!active) return '|||DESC|||';

    var txt = active.textContent.trim();
    // Extract job name: everything before the salary pattern
    var name = txt.replace(/(\d+-\d+K[^\s]{0,15}.*)$/, '').trim();
    // Clean further: remove trailing metadata
    name = name.replace(/\s+(经验不限|在校\/应届|学历不限|\d+-\d+年|本科|硕士|博士|大专).*$/, '').trim();

    // Extract salary
    var salMatch = txt.match(/(\d+-\d+K[^\s]{0,15})/);
    var salary = salMatch ? salMatch[1] : '';

    // Get description from body - the expanded job detail panel
    var body = document.body.innerText;
    var dStart = body.indexOf('职位描述');
    if (dStart === -1) dStart = body.indexOf('岗位职责');
    if (dStart === -1) dStart = body.indexOf('工作职责');
    var dEnd = -1;
    if (dStart > -1) {
        dEnd = body.indexOf('工作地址', dStart);
        if (dEnd === -1) dEnd = body.indexOf('职位要求', dStart + 10);
        if (dEnd === -1) dEnd = body.indexOf('任职要求', dStart + 10);
        if (dEnd === -1) dEnd = dStart + 3000;
    }
    var desc = dStart > -1 ? body.substring(dStart, dEnd).replace(/\n/g, ' ').trim() : '';

    return name + '|||' + salary + '|||DESC|||' + desc;
})()
