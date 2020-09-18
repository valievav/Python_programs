'''
You work for a manufacturer, and have been asked to calculate the total profit made on the sales of a product.
You are given a dictionary containing the cost price per unit (in dollars), sell price per unit (in dollars), and the starting inventory.
Return the total profit made, rounded to the nearest dollar.
'''

data=(
{
  "cost_price": 32.67,
  "sell_price": 45.00,
  "inventory": 1200
},
{
  "cost_price": 225.89,
  "sell_price": 550.00,
  "inventory": 100
},
{
  "cost_price": 2.77,
  "sell_price": 7.95,
  "inventory": 8500
}
)


def profit(data:iter)-> dict:
    profits = []
    for scope in data:
        profits.append(round((scope['sell_price'] - scope['cost_price']) * scope['inventory']))
    summary = sum(profits)
    return {"profits": profits, "summary": summary}


print(profit(data))
