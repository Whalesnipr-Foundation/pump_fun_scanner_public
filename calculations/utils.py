from coloredLogs import printWithColor
def calcualte_percentage_diff(amountA, amountB):

    printWithColor(f"current price = {amountA}", "info")
    printWithColor(f"Buy Price = {amountB}",'info')

    # Calculate the percentage difference
    percentage_diff = ((amountA - amountB) / amountA) * 100
    printWithColor(f"percentage diff = {percentage_diff}",'info')
    
    return percentage_diff


def calcualte_volume_percentage_diff(amountA, amountB):

    # Calculate the percentage difference
    percentage_diff = ((amountA - amountB) / amountA) * 100
    printWithColor(f"Current volume change = {percentage_diff}",'info')
    
    return percentage_diff




