// 裁判文书网列表页抓取片段
// 在检索结果页的浏览器控制台执行，每次调用翻一页并返回该页 15 条的紧凑记录。
// 记录格式：法院|案号|裁判日期|案件标题(前22字)
//
// 使用前提：
//   1. 已登录 wenshu.court.gov.cn
//   2. 已设置好检索条件，并把「每页」设为 15 条
//   3. 总命中数须 ≤ 600（列表上限），否则需先按年份/地域切片
//
// 注意：翻页按钮的屏幕坐标会随页码增多而右移，因此必须按文本定位，不能用固定坐标点击。

const grab = () =>
  [...document.querySelectorAll('.LM_list')].map(el => {
    const L = el.innerText.split('\n').map(s => s.trim()).filter(Boolean);
    // L[0]=审判程序标签 L[1]=案件标题 L[2]=法院 案号 日期
    const m = (L[2] || '').match(/^(\S+?法院)\s*(（\d{4}）\S+号)\s*(\S+)/) || [];
    return `${(m[1] || '?').slice(0, 8)}|${m[2] || '?'}|${m[3] || '?'}|${(L[1] || '').slice(0, 22)}`;
  }).join('\n');

const next = [...document.querySelectorAll('*')]
  .find(e => e.children.length === 0 && e.textContent.trim() === '下一页');
next.click();
await new Promise(r => setTimeout(r, 3500));
grab();

// 判断是否到达末页：连续两次返回相同内容即说明「下一页」已失效。
// 2026-08-15 实测：334 条 = 22 整页 + 末页 4 条，与检索计数一致。
