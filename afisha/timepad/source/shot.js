const {chromium}=require('playwright');
(async()=>{const [,,inp,out,w,h,scale]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:+(scale||1)});
await p.goto('file://'+inp,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
await p.screenshot({path:out,fullPage:h=='0'?true:false});await b.close();})();
