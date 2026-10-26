# DemandThread

**BFB 321 — Supply Chain Technologies · Group 23**

| Name | Student number |
|---|---|
| Iggie Coetzee | u24606805 |
| Jamelio Mannikam | u24570177 |
| Matthew Hattingh | u24720926 |
| Stuart Tyrrell | u24873111 |

## About

DemandThread is a web-based decision-support platform for fast-fashion retailers.
It brings point-of-sale and e-commerce sales data into one continuously updated view,
flags products at risk of stockout or excess inventory, and recommends when and how
much to reorder. The aim is to close the information gap between real-time customer
demand and upstream production decisions.

## Languages and framework used

- Frontend: HTML, CSS, Bootstrap

## Supply chain model (Python)

All the supply chain calculations are in one file, `models/supply_chain.py`.

| Section | What it answers | Web page |
|---|---|---|
| 1. Sample data | The 8 products shown on our pages | All |
| 2. Reorder logic | When do we order (reorder point + safety stock)? How much do we order? | Orders, Dashboard |
| 3. Stock alerts | How many days will the stock last? Which products risk a stockout or carry excess stock? | Sales and Inventory, Alerts |
| 4. Forecasting | How much will we sell next week? How accurate were past forecasts (MAPE)? | Forecasts |

## Setup Instructions
Open `templates/login.html` first to go to the login page and run the live server. This opens the web application. First a sign-in process is required (or it can be skipped for convinience in the demo). After sign-in it will show the dashboard and a navigation bar for other pages.

