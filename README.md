# Bible & Money Wisdom

An interactive diagram of Scripture on money and finances. Click a theme (Trust, Anxiety, Giving, Work, Debt, and more) to see related ESV passages.

- `index.html` – the page (static, no backend)
- `verses.js` – topics and passage data
- `topics.json` – the curated passage list (edit this to add or remove verses)
- `build_verses.py` – fetches ESV text from Crossway's official API into `verses.js`

## Rebuild the verse text

Get a free key at https://api.esv.org/account/create-application/ then:

    ESV_API_KEY=your_key python3 build_verses.py

Never commit your key. Keep total quoted text under the ESV limit of 500 verses (the script enforces this).

Scripture quotations are from the ESV® Bible (The Holy Bible, English Standard Version®), © 2001 by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved.
