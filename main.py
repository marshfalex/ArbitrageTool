import PySimpleGUI as sg
from src.mainlogic import get_arbitrage_opportunities
import os
from dotenv import load_dotenv

def main():
    load_dotenv()

    layout = [
        [sg.Text("API Key:"), sg.Input(key="API_KEY", default_text=os.environ.get("API_KEY", ""))],
        [sg.Text("Region:"), sg.Combo(["eu", "us", "au", "uk"], default_value="us", key="REGION")],
        [sg.Text("Cutoff (%):"), sg.Input(key="CUTOFF", default_text="0")],
        [sg.Button("Find Arbitrage Opportunities"), sg.Button("Exit")],
        [sg.Multiline(size=(80, 20), key="OUTPUT", disabled=True)]
    ]

    window = sg.Window("Arbitrage Finder", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        if event == "Find Arbitrage Opportunities":
            api_key = values["API_KEY"]
            region = values["REGION"]
            cutoff = float(values["CUTOFF"]) / 100

            arbitrage_opportunities = get_arbitrage_opportunities(key=api_key, region=region, cutoff=cutoff)
            
            output = []
            for arb in arbitrage_opportunities:
                output.append(f"{arb['match_name']} in {arb['league']}")
                output.append(f"Total implied odds: {arb['total_implied_odds']}")
                for key, value in arb['best_outcome_odds'].items():
                    output.append(f"{key} with {value[0]} for {value[1]}")
                output.append("")

            window["OUTPUT"].update("\n".join(output))

    window.close()

if __name__ == '__main__':
    main()