# 🖥️ **MetaBuild** - Smart PC Build Generator

Have you ever wanted to build your own personal computer but didn’t know where to start or which parts to choose?  
**MetaBuild** takes the guesswork out of PC building and is the ideal tool to get you started on your quest.
- You simply enter your budget and preferences for the build, and the tool will run a smart algorithm to create and suggest the best possiable build for **you**.
- The tool returns a list of all the parts constituting the build, each with a link for you to conveniently order from a trusted store.
---

## 🚀 Features

- 🔧 **Custom Build Generation** – Get a complete PC build tuned to your preferences in seconds.
- 🧩 **Preference-Based Recommendation** – Enter your budget, use-case, and other preferences to get yourself the best value for your money.
- 🧮 **Smart Algorithm** – The tool utilizes a smart algorithm that takes into account real-time prices, availability, compatibility, specs, and much more.
- 🔗 **Buy Links** - Get links to conveniently buy each component from Amazon, Newegg, Best Buy, and many more stores worldwide*.
- 🌎 **Region-Aware Selection** – Automatically get parts based on your country, ensuring local pricing, availability, and stores.
- ➕ **Extensive Parts Pool** - With 100s of parts in a database that's frequently updated, you can be sure that no part will go under the radar.

---

## 🛠️ Getting Started

MetaBuild will be hosted and made available soon. A deployment link will be provided here very shortly. Stay tuned!  
<br>
This repo contains both the front and back end for ease of access and demonstration purposes:  
- If you're trying to host on your own, then you'll need to have separate repos (or folders if running locally) for the front-end and back-end, respectively. 
- If you're only interested in the back-end (i.e. the algorithm), then you will need to inspect the code (views.py) to understand how to interact with it, as end-point documentation has not been made available.

---

## 📚 Tech Stack

- **Frontend:** Next.js + Bootstrap (deployed via Vercel)
- **Backend:** Django REST Framework (deployed via Render)
- **Database:** PostgreSQL (Render)
- **Languages:** Python, TypeScript, CSS
- **Other:** Postman was used for API testing, Pcpartpicker API is used to keep parts' data up to date.

---

## 📝 Notes
> ⚠️ Countires are limited by the Pcpartpicker API and are the following: Australia, Austria, Belgium, Canada, Czech Republic, Denmark, Finland, France, Germany, Hungary, Ireland, Italy, Netherlands, New Zealand, Norway, Portugal, Romania, Saudi Arabia, Slovakia, Spain, Sweden, United Kingdom, United States.

> Credit to Matyáš Cimbulka for developing the Pcpartpicker API; this tool would not have been possible without it.
> You can find it at https://apify.com/matyascimbulka/pcpartpicker-scraper.

---

## 📩 Contact

For questions, suggestions, or feedback, please feel free to open an issue or contact me at: adm.moune2@gmail.com.
