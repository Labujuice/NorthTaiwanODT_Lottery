# North Taiwan One-Day Trip Lottery (北台灣一日遊抽籤程式)

A simple yet fun tool to help you decide where to go for a one-day trip in North Taiwan! This project provides both a command-line interface (Shell script) and a graphical user interface (Python/Tkinter).

## Features

-   **Database**: Contains over 80 curated attractions across Keelung, Taipei, New Taipei, Taoyuan, Hsinchu, and Miaoli.
-   **Categories**: Zoos, Museums, Sightseeing Factories, Nature Trails, Theme Parks, and Old Streets.
-   **Filtering**: Select destination based on:
    -   **Region (縣市)**: e.g., Taipei, Hsinchu.
    -   **Cost (費用)**: Free (免費), Ticket (門票), Consumption (內部消費).
    -   **Age Group (年齡層)**: Suitable for All (都適合), Kids (小孩).
-   **Logging**: Keeps a history of your lottery results so you can revisit past "winners".

## Prerequisites

-   **Shell Version**: Bash (standard on Linux/macOS).
-   **Python Version**: Python 3.x with `tkinter` installed.
    -   On Ubuntu/Debian: `sudo apt-get install python3-tk`

## Usage

### 1. Shell Script (`lottery.sh`)

Run the script from your terminal.

```bash
# Make it executable (first time only)
chmod +x lottery.sh

# Run with interactive help
./lottery.sh --help

# Example: Find a free spot in New Taipei
./lottery.sh --region 新北 --cost 免費

# Example: Find a place suitable for kids
./lottery.sh --age 小孩
```

**Output**:
```text
🎉 Congratulations! Your destination is:
========================================
📍 Name: 鼻頭角步道
🏙️  City: 新北
...
========================================
```
*Logs are saved to `lottery.log`.*

### 2. Python GUI (`lottery.py`)

Launch the graphical interface for a more interactive experience.

```bash
python3 lottery.py
```

-   **Select Filters**: Choose your preferences from the dropdown menus.
-   **Start Lottery**: Click the **"開始抽籤!"** button to start the slot machine animation.
-   **View Map**: Click **"查看地圖"** to open the location in Google Maps.
-   **History**: Click **"查看歷史紀錄"** to see previous results.

*Logs are saved to `lottery_history.csv`.*

## Data Source

The attractions are stored in `attractions.csv`. You can easily add your own favorite spots by editing this file.

**Format**:
`景點名稱,類型,縣市,費用,年齡層,Google地圖連結,參考資料`

## TODO

-   Expand the attraction database (景點資料庫需要擴增).

## License

MIT License
