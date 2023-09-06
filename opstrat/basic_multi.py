#multiplotter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd

from helpers import payoff_calculator, check_optype, check_trtype, calculate_days_to_exp

abb={'c': 'Call',
    'p': 'Put',
    'b': 'Long',
    's': 'Short'}

def multi_plotter(spot_range, spot, op_list, 
                  exp_adjust_date="",save=False, file='fig.png', v=20, r=5.3, show_individual=False, show_transaction=True, show_combined=True, graph_header='Multiple Options Plotter'):
    """
    Plots a basic option payoff diagram for a multiple options and resultant payoff diagram
    
    Parameters
    ----------
    spot: int, float, default: 100 
       Spot Price
       
    spot_range: int, float, optional, default: 20
       Range of spot variation in percentage 
       
    op_list: dataframe for option/stock legs
       
       Each dataframe must contain the following columns
       'transaction_id': str
            Transaction ID to support grouping 
       'strike': int, float, default: 720
           Strike Price
       'tr_type': kind {'b', 's'} default:'b'
          Transaction Type>> 'b': long, 's': short
       'op_pr': int, float, default: 10
          Option Price
       'op_type': kind {'c','p','s'}, default:'c'
          Opion type>> 'c': call option, 'p':put option, 's':stock
       'contracts': int default:1, optional
           Number of contracts
        'exp_date': str, default '01-Jan-2023'
            Expiration date for contract
    
    exp_adjust_date: Str, default: ""
        Allows user to specify the date they want a future payoff diagram shown.
        
    save: Boolean, default False
        Save figure
    
    file: String, default: 'fig.png'
        Filename with extension
        
    v: int, float, default 20%
        Option Volatility
    
    r: int, float, default 5.3
        Risk Free Rate
        
    show_individual: Boolean, default False
        Show individual legs on payoff chart
        
    show_transaction: Boolean, default True
        Show combined transactions on payoff chart
        
    show_combined: Boolean, default True
        Show all option legs on a combined graph
        
    graph_header: String, Default: Multiple Options Plotter
        Allows User to Pass in Chart Header Variable
        
    Example
    -------
    op1={'op_type':'c','strike':110,'tr_type':'s','op_pr':2,'contract':1}
    op2={'op_type':'p','strike':95,'tr_type':'s','op_pr':6,'contract':1}
    
    import opstrat  as op
    op.multi_plotter(spot_range=20, spot=100, op_list=[op1,op2])
    
    #Plots option payoff diagrams for each op1 and op2 and combined payoff
    
    """
    # Validate Correct Columns Present in Dataframe
    required_columns = ['strike', 'op_type', 'exp_date', 'op_pr', 'tr_type', 'contracts']
    optional_columns_str = ['transaction_id']
    for i in required_columns:
        if i not in op_list:
            print(f"The column {i} is not present in the input data. This is a required column and must be added before proceeding.")
            return 
    
    for i in optional_columns_str:
        if i not in op_list:
            op_list[i] = ''

    # Sort Values by Transaction ID Column
    op_list.sort_values('transaction_id', inplace=True)

    # Define Range of Prices to Graph
    x=spot*np.arange(100-spot_range,101+spot_range,0.01)/100
    y0=np.zeros_like(x)         
    
    if exp_adjust_date != "":
        exp_adjust = calculate_days_to_exp(exp_adjust_date)
    else:
        exp_adjust=0
    
    # Initalize Y Axis List to be built from Risk Graphs
    y_list=[]
    if exp_adjust > 0:
        y_exp_list=[]
    
    # Add New Columns used by this Function
    op_list['contract_equiv'] = op_list['contracts']
    op_list['days_to_expiration'] = 0
    op_list['days_to_expiration_adjusted'] = 0
    
    # Adjust Contract Qty if Stock leg to equivalent contracts from shares of stock
    op_list['contract_equiv'].mask(op_list['op_type'] == 's', op_list['contract_equiv']/100, inplace=True)
    
    # Calculate Days to Expiration from Individual Leg Expiration Dates
    op_list['days_to_expiration'] = [calculate_days_to_exp(exp_date) for exp_date in op_list['exp_date']]
    
    # Set Days to Expiration to 0 for Stock Legs
    op_list['days_to_expiration'].mask(op_list['op_type'] == 's', 0, inplace=True)
    
    if exp_adjust > 0:
        # Calculate Days to Expiration from Individual Leg Expiration Dates
        op_list['days_to_expiration_adjusted'] = [(days_to_expiration - exp_adjust) for days_to_expiration in op_list['days_to_expiration']]
    
        # Set Days to Expiration to 0 for Stock Legs
        op_list['days_to_expiration_adjusted'].mask(op_list['op_type'] == 's', 0, inplace=True)
    
    # for id in transaction_id_list:
    for i, row in op_list.iterrows():    
        
        # Calculate Payoff Prices for each x Underlying Price Value with Days to Expiration
        y_list.append(payoff_calculator(x, row['op_type'], row['strike'], row['op_pr'], row['tr_type']
            , row['contracts'], row['days_to_expiration'], r, v ))

        # Calculate Payoff Prices with Adjusted Days to Expiration
        if exp_adjust > 0:
           y_exp_list.append(payoff_calculator(x, row['op_type'], row['strike'], row['op_pr'], row['tr_type']
            , row['contracts'], row['days_to_expiration_adjusted'], r, v ))

    def plotter():
                      
        y=0 # Combined Risk graph for Today's Date
        y_exp=0 # Combined Risk Graph for Future Expiration Date 
                
        plt.figure(figsize=(10,6))
             
        for tran_id in op_list['transaction_id'].unique():
            y_tran=0 # Risk Graph for Transactions Based on Today's Date
            y_tran_exp=0 # Risk Graph for Transactions for Future Expiration Date
            
            op_list_transaction = op_list.loc[op_list['transaction_id'] == tran_id]
            
            for i, row in op_list_transaction.iterrows():
                try:
                    contract=str(row['contracts'])  
                except:
                    contract='1'

                # Plot Indiivdual Price Leg Payoff Diagram
                if show_individual:
                    label=contract+' '+str(abb[row['tr_type']])+' '+str(abb[row['op_type']])+' ST: '+str(row['strike'])
                    sns.lineplot(x=x, y=y_list[i], label=label, alpha=0.5)

                # Plot Indiivdual Price Leg Payoff Diagram
                if show_individual and exp_adjust > 0:
                    label=contract+' '+str(abb[row['tr_type']])+' '+str(abb[row['op_type']])+' ST: '+str(row['strike'])
                    sns.lineplot(x=x, y=y_exp_list[i], label=label, alpha=0.5)
                
                # Add individual leg price to transaction leg
                if show_transaction:
                    y_tran+=np.array(y_list[i])
                
                # Add individual leg price to combined leg
                if show_combined:
                    y+=np.array(y_list[i])

                # Add Individual leg price to adjusted expiration combined leg
                if exp_adjust > 0:
                    y_exp+=np.array(y_exp_list[i])
                    
                    # Add individual leg price to transaction leg
                    if show_transaction:
                        y_tran_exp+=np.array(y_exp_list[i])
            
            # Plot Transaction Payoff Diagram       
            if show_transaction:
                sns.lineplot(x=x, y=y_tran, label=tran_id, alpha=0.75)
            
            # Plot Future Expiration Transaction Payoff Diagram
            if show_transaction and exp_adjust > 0:
                label = tran_id+' as of '+exp_adjust_date
                sns.lineplot(x=x, y=y_tran_exp, label=label, alpha=0.75)            
        
        # Plot Current Day Payoff Diagram
        if show_combined:
            sns.lineplot(x=x, y=y, label='Combined As of Today', alpha=1, color='k')
        
        # Plot Adjusted Expiration Payoff Diagram
        if show_combined and exp_adjust > 0: 
            sns.lineplot(x=x, y=y_exp, label=f'As of {exp_adjust_date}', alpha=1)
            
        # Prepare Plot Diagram
        plt.axhline(color='k', linestyle='--')
        plt.axvline(x=spot, color='r', linestyle='--', label='spot price')
        plt.legend()
        plt.legend(loc='upper right')
        title=graph_header
        plt.title(title)
        plt.fill_between(x, y, 0, alpha=0.2, where=y>y0, facecolor='green', interpolate=True)
        plt.fill_between(x, y, 0, alpha=0.2, where=y<y0, facecolor='red', interpolate=True)
        plt.tight_layout()
        if save==True:
            plt.savefig(file)
        plt.show()
        
    # Check if Plot Will Generate any Graphs
    if not show_combined and not show_transaction and not show_individual:
            print('You have selected to not show individual option legs, combined transaction legs, or combined graph. No graph will be generated.')
            return
    else:
        plotter()      
    
if __name__ == '__main__':
    #header = ['transaction_id','strike', 'tr_type', 'op_pr', 'op_type', 'contracts', 'exp_date']
    header = ['strike', 'tr_type', 'op_pr', 'op_type', 'contracts', 'exp_date']
    
#    data_misc1 = [
#            ['1A',215,'s',7.63,'c',1,'08-Sep-23'],
#            ['2A',220,'b',5.35,'p',1,'15-Sep-23'],
#            ['1A',220,'s',0,'s',200,'15-Sep-23'],
#            ]
    
    data_bf1 = [
            [200,'b',0,'c',1,'17-Nov-23'],
            [220,'b',0,'c',1,'17-Nov-23'],
            [210,'s',0,'c',2,'17-Nov-23'],
            ]
    
    data_bf2 = [
            [210,'b',0,'c',1,'17-Nov-23'],
            [220,'s',0,'c',2,'17-Nov-23'],
            [230,'b',0,'c',1,'17-Nov-23'],
            ]

    df_bf1 = pd.DataFrame(data_bf1, columns=header)
    df_bf2 = pd.DataFrame(data_bf2, columns=header)
    df_total = pd.concat([df_bf1, df_bf2], ignore_index=True, sort=False)
    #df_total.sort_values('strike', inplace=True)
    # print(df_bf1)
    # print(df_bf2)

    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, graph_header = "Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_bf2, show_individual=False, graph_header = "Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=True, show_transaction=False, show_combined=False, graph_header = "Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=False, show_transaction=True, show_combined=False, graph_header = "Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=False, show_transaction=False, show_combined=True, graph_header = "Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=False, show_transaction=True, show_combined=True, graph_header = "Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=True, show_transaction=True, show_combined=True, graph_header = "Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=True, show_transaction=True, show_combined=True, graph_header = "Risk Graph")
    
    #multi_plotter(spot=212.26,spot_range=10, exp_adjust_date='15-Sep-23', op_list=df, show_individual=False, graph_header = "AAPL Risk Graph")