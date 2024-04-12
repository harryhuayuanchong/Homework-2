liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

# 1. Create a graph: Each node represent tokens and the edges represent the trading pairs between tokens and the corresponding liquidity
graph = {
    "tokenA": {"tokenB": 10, "tokenC": 7, "tokenD": 9, "tokenE": 5},
    "tokenB": {"tokenA": 17, "tokenC": 4, "tokenD": 6, "tokenE": 3},
    "tokenC": {"tokenA": 11, "tokenB": 36, "tokenD": 12, "tokenE": 8},
    "tokenD": {"tokenA": 15, "tokenB": 13, "tokenC": 30, "tokenE": 25},
    "tokenE": {"tokenA": 21, "tokenB": 25, "tokenC": 10, "tokenD": 60}
}

# 2. Calculate amountOut by using the UniswapV2 Library Calculation:
def getAmountOut(amountIn, reserve0, reserve1):
    if amountIn <= 0 or reserve0 <= 0 or reserve1 <= 0:
        return 0
    amountInWithFee = amountIn * 997
    numerator = amountInWithFee * reserve1
    denominator = reserve0 * 1000 + amountInWithFee
    if denominator == 0:
        return 0
    amountOut = numerator / denominator
    return amountOut

# 3. Find the best path to receive 20 units of Token B
def find_arbitrage(start_token, current_token, amount, path, visited, max_cycles=6):
    # If we've made too many trades or cycle back without profit, stop searching
    if len(path) > max_cycles:
        return (False, 0, [])

    # If we have completed a cycle
    if current_token == start_token and len(path) > 1:
        return (True, amount, path)

    max_amount = 0
    best_path = []
    for next_token in graph[current_token]:
        if (current_token, next_token) in visited:
            continue
        
        # Get liquidity reserves for the trading pair
        reserve0, reserve1 = liquidity[(current_token, next_token)] if (current_token, next_token) in liquidity else liquidity[(next_token, current_token)]
        
        # Calculate the output amount for the trade
        out_amount = getAmountOut(amount, reserve0, reserve1) if current_token < next_token else getAmountOut(amount, reserve1, reserve0)
        
        # Continue searching
        visited.add((current_token, next_token))
        success, found_amount, found_path = find_arbitrage(start_token, next_token, out_amount, path + [next_token], visited, max_cycles)
        visited.remove((current_token, next_token))

        # Check if we found a better path
        if success and found_amount > max_amount:
            max_amount = found_amount
            best_path = found_path

    return (max_amount > 0, max_amount, best_path)

# 4. Find all possible paths
def find_all_arbitrage_paths(start_token, current_token, amount, path, visited, results, max_cycles=6):
    if len(path) > max_cycles:
        return

    if current_token == start_token and len(path) > 1 and amount > 5:  # Ensure returning with profit
        results.append((path.copy(), amount))
        return

    for next_token in graph[current_token]:
        if (current_token, next_token) in visited:
            continue

        # Fetch reserve info and ensure it's correctly ordered based on the token pair
        reserve_info = liquidity.get((current_token, next_token)) or liquidity.get((next_token, current_token))
        if not reserve_info:
            continue  # Skip if no liquidity info available

        # Correct assignment of reserves based on the token direction in the liquidity dict
        if (current_token, next_token) in liquidity:
            reserve0, reserve1 = reserve_info
        else:
            reserve1, reserve0 = reserve_info

        out_amount = getAmountOut(amount, reserve0, reserve1)
        
        if out_amount > 0:
            visited.add((current_token, next_token))
            find_all_arbitrage_paths(start_token, next_token, out_amount, path + [next_token], visited, results, max_cycles)
            visited.remove((current_token, next_token))

# 5. Main Function
def main():
    # Start from tokenB with 5 units
    success, max_amount, best_path = find_arbitrage("tokenB", "tokenB", 5, ["tokenB"], set(), max_cycles=5)

    if success:
        print(f"---------------------------------------------------------------------------------------")
        print(f"                                 The best paths                                   ")
        print(f"---------------------------------------------------------------------------------------")
        print(f"path: {'->'.join(best_path)}, tokenB balance={max_amount:.15f}")
        
    else:
        print("No profitable arbitrage path found.")
        
    print("\n")
        
    # Find all possible paths
    results = []
    find_all_arbitrage_paths("tokenB", "tokenB", 5, ["tokenB"], set(), results, max_cycles=6)
    
    # Sort the results by balance in descending order
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

    print(f"---------------------------------------------------------------------------------------")
    print(f"                                 All possible paths                                   ")
    print(f"---------------------------------------------------------------------------------------")
    for path, amount in sorted_results:
        if amount > 5:  # Only display paths where there's a gain in tokenB
            print(f"path: {'->'.join(path)}, tokenB balance={amount:.15f}")

if __name__ == '__main__':
    main()
