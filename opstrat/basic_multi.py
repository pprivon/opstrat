#multiplotter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd

from .helpers import payoff_calculator, check_optype, check_trtype, calculate_days_to_exp

abb={'c': 'Call',
    'p': 'Put',
    'b': 'Long',
    's': 'Short'}

def multi_plotter(spot_range=20, spot=100,  
                op_list=[{'op_type':'c','strike':110,'tr_type':'s','op_pr':2,'contract':1},
                {'op_type':'p','strike':95,'tr_type':'s','op_pr':6,'contract':1,'exp_date':'01-Jan-2025'}], 
                  exp_adjust_date="",save=False, file='fig.png', v=20, r=5.3, show_individual=True, graph_header='Multiple Options Plotter'):
    """
    Plots a basic option payoff diagram for a multiple options and resultant payoff diagram
    
    Parameters
    ----------
    spot: int, float, default: 100 
       Spot Price
       
    spot_range: int, float, optional, default: 20
       Range of spot variation in percentage 
       
    op_list: dataframe for option/stock legs
       
       Each dataframe must contiain following columns
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
        
    show_individual: Boolean, default True
        Show individual legs on payoff chart
        
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
    
    for i, row in op_list.iterrows():    
  
        # Calculate Payoff Prices for each x Underlying Price Value with Days to Expiration
        y_list.append(payoff_calculator(x, row['op_type'], row['strike'], row['op_pr'], row['tr_type']
            , row['contracts'], row['days_to_expiration'], r, v ))

        # Calculate Payoff Prices with Adjusted Days to Expiration
        if exp_adjust > 0:
           y_exp_list.append(payoff_calculator(x, row['op_type'], row['strike'], row['op_pr'], row['tr_type']
            , row['contracts'], row['days_to_expiration_adjusted'], r, v ))

    def plotter():
        y=0
        y_exp=0
        plt.figure(figsize=(10,6))
        
        for i, row in op_list.iterrows():
            try:
                contract=str(row['contracts'])  
            except:
                contract='1'
                
            # Plot Indiivdual Price Leg Payoff Diagram
            if show_individual == True:
                label=contract+' '+str(abb[row['tr_type']])+' '+str(abb[row['op_type']])+' ST: '+str(row['strike'])
                sns.lineplot(x=x, y=y_list[i], label=label, alpha=0.5)
            
            # Add individual leg price to combined leg
            y+=np.array(y_list[i])
            
            # Add Individual leg price to adjusted expiration combined leg
            if exp_adjust > 0:
                y_exp+=np.array(y_exp_list[i])
        
        # Plot Current Day Payoff Diagram
        sns.lineplot(x=x, y=y, label='Combined As of Today', alpha=1, color='k')
        
        # Plot Adjusted Expiration Payoff Diagram
        if exp_adjust > 0: 
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

    plotter()      
    
