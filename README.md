# 🐷 Pig Cleaner - The Desktop Pet that Eats Your Trash!

[![macOS](https://img.shields.io/badge/macOS-Supported-black.svg?logo=apple)]()
[![Windows](https://img.shields.io/badge/Windows-Supported-blue.svg?logo=windows)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Pig Cleaner** is a gamified System Cleaner & Virtual Desktop Pet for macOS and Windows. A cute little pig wanders around the bottom of your screen, helping you clean up junk files and free up disk space. The more trash it cleans, the chubbier and happier it gets!

<img width="1507" height="950" alt="Pig Cleaner Demo" src="https://github.com/user-attachments/assets/09bd8b30-793a-4d49-9265-be8cd6ae2bb1" />


---

## 📥 Download & Install

Don't want to build from source? Download the latest compiled version directly below:

- 🍏 **[Download for macOS (.dmg) ➔](https://github.com/PigTinyLabs/Pig-cleaner/releases/latest)** *(Optimized for Intel & Apple Silicon M1/M2/M3)*
- 🪟 **[Download for Windows (.exe) ➔](https://github.com/PigTinyLabs/Pig-cleaner/releases/latest)**

*(Note: On macOS, please grant **Full Disk Access** in `System Settings → Privacy & Security` so the pig can properly clean system folders like Safari Cache or Xcode DerivedData).*

---

## ✨ Why Pig Cleaner?

- 🐾 **Feed Your Pet with Trash:** Empty your system trash bin to "feed" the pig. Watch it grow and become delightfully chubby as you free up more space.
- 💻 **Developer-Focused Cache Cleaning:** Say goodbye to gigabytes of hidden dev junk. Pig Cleaner safely scans and wipes heavy caches from:
  - `npm`, `yarn`, `pip`, `Homebrew`
  - `Docker` containers & volumes
  - `Xcode DerivedData`, `VS Code`, `Gradle`
- ⏰ **Auto-Foraging Mode:** Set a timer (30 mins, 1 hour, 6 hours) and the pig will automatically go hunting for junk files in the background.
- 🎮 **Interactive Physics:** The pig has natural states (walking, sniffing, sleeping, full belly). You can drag and drop it, toss it across the screen with physical inertia, or click it to command an instant cleanup!
- 🛡️ **Transparent & Safe:** Review detailed statistics of your junk files and folder sizes before making any deletion decisions.

<p align="center">
  <img width="318" alt="Feature 1" src="https://github.com/user-attachments/assets/87146206-7160-467d-97b6-47f8913c03e1" />
  <img width="322" alt="Feature 2" src="https://github.com/user-attachments/assets/294be737-5161-44c7-8483-19e2fc56d36a" />
</p>

---

## ☕️ Support & Donate

**Pig Cleaner is 100% free and open-source.** 

If this little pig helped you free up 10GB of SSD storage, saved you hours of manual cleaning, or just brought a smile to your workday, consider buying me a coffee! Your support keeps the pig fed and motivates me to develop new awesome features. ❤️

*   💸 **PayPal:** [paypal.me/pigtiny](https://paypal.me/pigtiny)
*   ☕ **Buy Me A Coffee / Ko-fi:** *(Highly recommend creating an account and putting the link here!)*
*   🇻🇳 **Momo (Vietnam):** `0359233523`

---

## 🛠️ For Developers (Build from source)

**Prerequisites:** macOS or Windows, Node.js (v18+).

```bash
# Clone the repository
git clone [https://github.com/PigTinyLabs/Pig-cleaner.git](https://github.com/PigTinyLabs/Pig-cleaner.git)
cd Pig-cleaner

# Install dependencies
npm install

# Start Development mode
npm run dev
