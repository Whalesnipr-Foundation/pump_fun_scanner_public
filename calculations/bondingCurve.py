from calculations.creationTime import check_creation_time
from coin_data import get_coin_data
from coloredLogs import  printWithColor


async def filterTokens(data, lowest_bonding_curve, highest_bonding_curve, min_market_cap):

    tokens_above_thresshold = []

    for token_data in data: 
        
        # Assign values of total_supply and real_token_reserves to new variables
        total_supply = int(token_data.get('total_supply'))
        real_token_reserves = int(token_data.get('real_token_reserves'))
        token_mint = token_data.get('mint')
        token_name = token_data.get('name')
        creation_time = token_data.get('created_timestamp')
        same_day_creation = check_creation_time(int(creation_time))
        token_market_cap = token_data.get('usd_market_cap')
        website = token_data.get('website')
        twitter = token_data.get('twitter')
        telegram = token_data.get('telegram')
        usd_market_cap = token_data.get('usd_market_cap')
        king_of_the_hill_timestamp  = token_data.get('king_of_the_hill_timestamp')

        
        

        if total_supply is not None and real_token_reserves is not None:
            bondingCurvePercentage = calculate_bonding_curve_percentage(total_supply, real_token_reserves)

    

            if (
                bondingCurvePercentage >= lowest_bonding_curve
                and bondingCurvePercentage < highest_bonding_curve
                and same_day_creation
                and token_market_cap >= min_market_cap
                
            ):
                # Append a dictionary with key-value pairs
                token_info = {
                    "token_mint": token_mint,
                    "token_name": token_name,
                    "bondingCurvePercentage": bondingCurvePercentage,
                    "market_cap": token_market_cap,
                    "website": website,
                    "twitter": twitter,
                    "telegram": telegram,
                    "king_of_the_hill_timestamp": king_of_the_hill_timestamp,
                 
                    
                }
                tokens_above_thresshold.append(token_info)

    return tokens_above_thresshold




# We can say to calculate the bonding curve we take the
# total_supply - real_token_reserves = tokens_left_to_buy
# to calcualte percentage bonding curve
# tokens_left_to_buy / total_supply *100 (Give or take 5%) Maybe more take than give
# So we are looking for tokens in the range of 90% - 95%


def calculate_bonding_curve_percentage(total_supply, real_token_reserves):
    tokens_left_to_buy = total_supply - real_token_reserves
    percentage_bonding_curve = tokens_left_to_buy / total_supply * 100

    return percentage_bonding_curve


async def get_current_bonding_curve_percentage(token_mint):

    #Get Current Bonding Curve Percentage
    coin_data = get_coin_data(token_mint)

    if coin_data is None:
        printWithColor('Failed to retrieve coin data...', "red")
        #if the data is none, assume bonging is 99% which will trigger immediate sell
        return 99
    reserves = coin_data['real_token_reserves']
    supply = coin_data['token_total_supply']
    
    current_bonding_percentage = calculate_bonding_curve_percentage( supply, reserves)
    print(f'Current Bonding Curve Percentage is {current_bonding_percentage}')

    return current_bonding_percentage
