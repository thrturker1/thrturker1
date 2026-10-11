// Optional: PLAYWRIGHT_MODULE may point to a bundled Playwright installation.
// Screenshots are local review artifacts, not part of the public README.
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const root = path.resolve(__dirname,'..');
const out = path.join(root,'.preview');
const fileURL = rel => pathToFileURL(path.join(root,rel)).href;

(async () => {
  await fs.mkdir(out,{recursive:true});
  const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH || undefined});
  const page=await browser.newPage({viewport:{width:940,height:1200},deviceScaleFactor:1});
  const failures=[];
  page.on('pageerror',e=>failures.push(e.message));
  await page.goto(fileURL('.preview/index.html'));
  await page.waitForFunction(()=>[...document.images].every(i=>i.complete));
  const loaded=await page.evaluate(()=>[...document.images].map(i=>({src:i.getAttribute('src'),width:i.naturalWidth})));
  if(loaded.some(i=>!i.width))throw Error('Broken image: '+JSON.stringify(loaded));
  await page.screenshot({path:path.join(out,'profile-desktop.png'),fullPage:true});
  const desktopHeight=await page.locator('main').evaluate(e=>Math.ceil(e.getBoundingClientRect().height));
  await page.emulateMedia({colorScheme:'light',reducedMotion:'reduce'});
  await page.screenshot({path:path.join(out,'profile-light.png'),fullPage:true});
  const fallbacks=await page.evaluate(()=>[...document.querySelectorAll('picture img')].map(i=>i.currentSrc));
  if(fallbacks.some(s=>s.endsWith('hero.svg')||s.endsWith('stack.svg')||s.endsWith('studio.svg')||s.endsWith('terminal.gif')))throw Error('Reduced-motion sources not selected');
  await page.setViewportSize({width:390,height:900});
  await page.emulateMedia({colorScheme:'dark',reducedMotion:'reduce'});
  await page.screenshot({path:path.join(out,'profile-mobile.png'),fullPage:true});
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  if(overflow)throw Error('Mobile horizontal overflow');
  await page.emulateMedia({colorScheme:'dark',reducedMotion:'no-preference'});
  const scenes=[['hero.svg',350,2000,'hero-identity'],['hero.svg',350,8500,'hero-about'],
    ['stack.svg',342,2000,'stack-1'],['stack.svg',342,8000,'stack-2'],['stack.svg',342,38000,'stack-7'],
    ['studio.svg',278,2000,'studio'],['terminal-static.svg',240,0,'terminal']];
  const bounds=[];
  for(const [file,height,time,name] of scenes){
    const width=1200;
    await page.setViewportSize({width,height});
    await page.goto(fileURL('assets/'+file));
    await page.evaluate(t=>{for(const a of document.getAnimations()){a.pause();a.currentTime=t}},time);
    await page.screenshot({path:path.join(out,name+'.png')});
    const clipped=await page.evaluate(()=>{
      const s=document.documentElement.viewBox.baseVal;
      return [...document.querySelectorAll('text')].filter(e=>{
        let p=e;while(p){if(getComputedStyle(p).opacity==='0')return false;p=p.parentElement}
        const b=e.getBoundingClientRect();return b.x < -1 || b.right > s.width+1 || b.bottom > s.height+1;
      }).map(e=>e.textContent);
    });
    // Carousel intentionally places clipped pages outside the view box.
    if(!file.startsWith('stack')&&clipped.length)bounds.push({file,clipped});
  }
  // Check all static pages, which have no deliberate offscreen text.
  for(let i=1;i<=7;i++){
    await page.setViewportSize({width:1200,height:342});
    await page.goto(fileURL(`assets/stack-page-${i}.svg`));
    const bad=await page.evaluate(()=>[...document.querySelectorAll('[data-tech]')].filter(g=>{
      const r=g.querySelector('rect').getBoundingClientRect();
      return [...g.querySelectorAll('text')].some(t=>t.getBoundingClientRect().right>r.right-8);
    }).map(g=>g.dataset.tech));
    if(bad.length)bounds.push({file:`stack-page-${i}`,clipped:bad});
  }
  if(bounds.length||failures.length)throw Error(JSON.stringify({bounds,failures}));
  console.log(JSON.stringify({desktopHeight,images:loaded.length,overflow,staticFallbacks: fallbacks.map(x=>path.basename(x)),screenshots:out},null,2));
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
