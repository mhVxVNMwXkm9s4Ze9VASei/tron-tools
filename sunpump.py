import requests
from math import ceil

SUNPUMP_API_URL = "https://api-v2.sunpump.meme/pump-api"
RESULTS_PER_PAGE = 200  # This seems to be the max number of results per page.


def get_token_transactions(token_address):
    transactions = []
    page = 1
    r = requests.get(f"{SUNPUMP_API_URL}/transactions/token/{
                     token_address}?page=1&size={RESULTS_PER_PAGE}&sort=txDateTime:ASC")
    data = r.json()
    pages = ceil(int(data["data"]["metadata"]["total"]) / RESULTS_PER_PAGE)

    for transaction in data["data"]["swaps"]:
        transactions.append(transaction)

    page += 1

    while page <= pages:
        r2 = requests.get(f"{SUNPUMP_API_URL}/transactions/token/{token_address}?page={
                          page}&size={RESULTS_PER_PAGE}&sort=txDateTime:ASC")
        data2 = r2.json()

        for transaction in data2["data"]["swaps"]:
            transactions.append(transaction)

        page += 1

    print(transactions)
    print(f"Found {len(transactions)} transactions")

    return transactions


def parse_transactions(transactions):
    wallets = {}

    for transaction in transactions:
        wallet = transaction["userAddress"]

        if wallet not in wallets:
            wallets[wallet] = {
                "buys": 0,
                "sells": 0,
                "totalBoughtInTron": 0,
                "totalSoldInTron": 0,
            }

        if transaction["txnOrderType"] == "BUY":
            wallets[wallet]["buys"] += 1
            wallets[wallet
                    ]["totalBoughtInTron"] += transaction["fromTokenAmount"]
        else:
            wallets[wallet]["sells"] += 1
            wallets[wallet
                    ]["totalSoldInTron"] += transaction["toTokenAmount"]

    print(wallets)

    return wallets


token_address = input("Enter token address: ")
transactions = get_token_transactions(token_address)
wallets = parse_transactions(transactions)
