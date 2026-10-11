(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const bilingual = (zh,en) => document.documentElement.dataset.view==='zh' ? zh : document.documentElement.dataset.view==='en' ? en : zh+' / '+en;
  function well() {
    const w=Number($('well-width').value), n=Number($('well-n').value);
    $('well-output').textContent=`L/L₀ = ${w.toFixed(1)}, n = ${n}; Eₙ/E₁(L₀) = ${(n*n/(w*w)).toFixed(3)}`;
    const path=[];
    for(let i=0;i<=300;i++){const x=w*i/300,y=2/w*Math.sin(n*Math.PI*i/300)**2;path.push(`${i?'L':'M'}${(35+500*x/3).toFixed(2)},${(150-60*y).toFixed(2)}`);}
    $('well-curve').setAttribute('d',path.join(' '));
  }
  function phase() {
    const degrees=Number($('phase').value), plus=(1+Math.cos(degrees*Math.PI/180))/2;
    $('phase-output').textContent=`φ = ${degrees}°; P₊ = ${(plus*100).toFixed(1)}%, P₋ = ${((1-plus)*100).toFixed(1)}%`;
    $('plus-bar').style.width=`${plus*100}%`;$('minus-bar').style.width=`${(1-plus)*100}%`;
  }
  let count=0,positives=0;
  function measurement() {
    const p=Number($('measurement-p').value);
    $('measurement-output').textContent=`p = ${p.toFixed(2)}; `+bilingual('理论均值','Expected mean')+` = ${(2*p-1).toFixed(2)}ℏ; N = ${count}; +ℏ: ${positives}, −ℏ: ${count-positives}; `+bilingual('样本平均','Sample mean')+` = ${count?((2*positives-count)/count).toFixed(3)+'ℏ':'—'}`;
  }
  for(const id of ['well-width','well-n'])$(id).addEventListener('input',well);
  $('phase').addEventListener('input',phase);
  $('measurement-p').addEventListener('input',()=>{count=positives=0;measurement();});
  $('measure-reset').addEventListener('click',()=>{count=positives=0;measurement();});
  $('measure-100').addEventListener('click',()=>{const p=Number($('measurement-p').value);for(let i=0;i<100;i++)if(Math.random()<p)positives++;count+=100;measurement();});
  document.addEventListener('languagechange',measurement);
  well();phase();measurement();
})();
