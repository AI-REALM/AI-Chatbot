const puppeteer = require('puppeteer');

const url = process.argv[2];

(async () => {
    const browserURL = "http://127.0.0.1:9222";

    const browser = await puppeteer.connect({ browserURL });
    const page = await browser.newPage()
    try {
      await page.setViewport({ width:1600, height: 900});
      await page.goto(
        `${url}`,
        { waitUntil: 'networkidle0' }
      );

    // Evaluate the function inside the page context to extract the simplified structure
      const textContent = await page.evaluate(() => {
          return document.body.innerText;
      });

      // console.log(textContent);
      let returnValue = {
          page: textContent
      };
      await page.close();
      await browser.disconnect();
      console.log(JSON.stringify(returnValue)); // Convert the object to a JSON string and print it
      process.exit(0)
    } catch {
      await page.close();
      await browser.disconnect();
      let returnValue = {
          page: "FALSE/FALSE"
      };
      console.log(JSON.stringify(returnValue)); 
      process.exit(0)
    }
})();

