from src.mainlogic import get_arbitrage_opportunities
import os
import argparse
from dotenv import load_dotenv
from rich import print

def main():
    # Load environment variables from a .env file
    load_dotenv()

    # Set up argument parser for command-line inputs
    parser = argparse.ArgumentParser(
        prog="Arbitrage Finder",
        description=__doc__  # Use the module's docstring as the description
    )
    parser.add_argument(
        "--key",
        default=os.environ.get("API_KEY"),  # Default API key from environment variables
    )
    parser.add_argument(
        "--region",
        choices=["eu", "us", "au", "uk"],  # Restrict choices to these regions
        default="us",  # Default region
    )
    parser.add_argument(
        "--unformatted",
        action="store_true",  # Flag for unformatted output
    )
    parser.add_argument(
        "--cutoff",
        type=float,
        default=0,  # Default cutoff value for filtering arbitrage opportunities
    )
    args = parser.parse_args()

    # Adjust cutoff for percentage input
    cutoff = args.cutoff / 100

    # Retrieve arbitrage opportunities using the provided API key and parameters
    arbitrage_opportunities = get_arbitrage_opportunities(key=args.key, region=args.region, cutoff=cutoff)

    # Print the results based on the format specified by the user
    if args.unformatted:
        # Print raw list of arbitrage opportunities
        print(list(arbitrage_opportunities))
    else:
        # Convert generator to list and print summary
        arbitrage_opportunities = list(arbitrage_opportunities)
        print(f"{len(arbitrage_opportunities)} arbitrage opportunities found")

        # Print detailed information for each arbitrage opportunity
        for arb in arbitrage_opportunities:
            print(f"\t[italic]{arb['match_name']} in {arb['league']} [/italic]")
            print(f"\t\tTotal implied odds: {arb['total_implied_odds']} with these odds:")
            for key, value in arb['best_outcome_odds'].items():
                print(f"\t\t{key} with {value[0]} for {value[1]}")

if __name__ == '__main__':
    main()