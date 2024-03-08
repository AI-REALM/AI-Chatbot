const puppeteer = require('puppeteer');

const url = process.argv[2];

(async () => {
    const browserURL = "http://127.0.0.1:9223";

    const browser = await puppeteer.connect({ browserURL });
    const page = await browser.newPage()
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
})();

