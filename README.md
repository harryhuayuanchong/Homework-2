# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution

**Profitable path**

tokenB->tokenA->tokenD->tokenC->tokenB

**The amountIn, amountOut value for each swap**

B->A: amountIn=5, amountOut=5.655321988655322  
A->D: amountIn=5.655321988655322, amountOut=2.4587813170979333  
D->C: amountIn=2.4587813170979333, amountOut=5.0889272933015155  
C->B: amountIn=5.0889272933015155, amountOut=20.129888944077443

**Final reward (tokenB balance)**

20.129888944077443

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution

Slippage refers to the difference between the expected price at the time a trade is initiated and the actual execution price.
In AMMs, this price difference is mainly caused by two factors: market price fluctuations and the impact of large trades on the liquidity pool.
When a trade is large enough to significantly alter the ratio of assets in the liquidity pool, it causes price slippage, affecting the trade price.

**How does Uniswap V2 address address this issue?**

Setting a lower slippage tolerance in your swap transaction can prevent your transaction from being executed at a significantly worse price, 
although it also increases the risk of the transaction failing due to normal price movements.

**Example**

Slippage = current market price – trade execution price

If you place a 1 Bitcoin buy order for $10,000 and it gets filled for $9,800, your slippage will be $200 (10,000-9,800)

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution

When the first liquidity provider adds liquidity to a new pool, a certain amount of liquidity tokens, specifically 1,000 units, is permanently locked in the pool and not assigned to the provider.

**Rationale behind this design:**

By subtracting a minimum liquidity amount upon the first minting of liquidity tokens in a Uniswap V2 pool is a thoughtful design choice aimed at preventing manipulation, 
ensuring the stability and integrity of the pool, and establishing a foundation for the pool's liquidity and valuation.

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution

**Formula:**
liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);

This formula is designed to maintain the relative value of existing liquidity positions and to ensure fair distribution of new liquidity tokens based on the amount of assets deposited relative to the pool's total size.

**The intention behind this formula:**

To ensure fairness, protect the value of existing liquidity positions, align incentives, and prevent manipulation. 
This mechanism is fundamental to the automated market maker (AMM) model's efficiency and effectiveness, ensuring that liquidity providers are rewarded in proportion to their contribution to the pool's depth and health.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution

A sandwich attack is a type of manipulation seen on decentralized exchanges (DEXs) that primarily affects traders using automated market makers (AMMs).
This attack exploits the openness and transparency of blockchain transactions.

**How a Sandwich Attack Works：**

**Observation**: The attacker monitors the mempool (a holding area for transactions awaiting confirmation) for large, pending swap transactions that are likely to significantly impact the price of a trading pair on a DEX.

**Front-Running**: Upon identifying a profitable target transaction, the attacker places their own swap transaction with a higher gas fee to ensure it gets processed before the targeted transaction. 
This first transaction by the attacker buys the asset that the target transaction is buying, but at the original, lower price.

**Back-Running**: After the target transaction is processed and the price of the asset has increased due to the target's large purchase, 
the attacker executes a second transaction to sell the asset at the new, higher price. This transaction also uses a higher gas fee to ensure it is processed immediately after the target transaction.

**How might it impact you when initiating a swap?**

The target transaction (your swap) buys the asset at a higher price than initially anticipated because the attacker's front-running transaction has already moved the price.
