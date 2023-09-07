from .opstrat import multi_plotter
import pandas as pd

header = ['strike', 'tr_type', 'op_pr', 'op_type', 'contracts', 'exp_date']
data = [[215,'s',7.63,'c',1,'15-Sep-23'],
        [220,'b',5.35,'p',1,'15-Sep-23']
        ]

df = pd.DataFrame(data, columns=header)

#print(df)

multi_plotter(spot=212.26,spot_range=10, exp_adjust_date='15-Sep-23', op_list=df, show_individual=False, graph_header = "AAPL Risk Graph")
# op1={'op_type': 'c', 'strike': 215, 'tr_type': 's', 'op_pr': 7.63, 'contract': 1, 'exp_date':'15-Sep-23'}
# op2={'op_type': 'p', 'strike': 220, 'tr_type': 'b', 'op_pr': 5.35, 'contract': 1, 'exp_date':'15-Sep-23'}
# op3={'op_type': 'p', 'strike': 210, 'tr_type': 's', 'op_pr': 7.20, 'contract': 1, 'exp_date':'08-Sep-23'}
# op4={'op_type': 'p', 'strike': 205, 'tr_type': 'b', 'op_pr': 5.52, 'contract': 1, 'exp_date':'15-Sep-23'}
# op5={'op_type': 's', 'strike': 210, 'tr_type': 'b', 'op_pr': 0, 'contract': 50}

# op_list=[op1
#         , op2
#         # , op3
#         # , op4
#         # , op5
#          ]
# # op.multi_plotter(spot=212.26,spot_range=10, op_list=op_list)
# op.multi_plotter(spot=212.26,spot_range=10, exp_adjust_date='15-Sep-23', op_list=op_list)
# op.multi_plotter(spot=212.26,spot_range=10, exp_adjust_date='15-Sep-23', op_list=op_list, show_individual=False, graph_header = "AAPL Risk Graph")

# op.single_plotter(spot=212.26, spot_range=10, strike=210, op_type='s', tr_type='s', op_pr=0)
# op.single_plotter(spot=212.26, spot_range=10, strike=210, op_type='s', tr_type='b', op_pr=0)

if __name__ == '__main__':
    header = ['transaction_id','strike', 'tr_type', 'op_pr', 'op_type', 'contracts', 'exp_date']
    
#    data_misc1 = [
#            ['1A',215,'s',7.63,'c',1,'08-Sep-23'],
#            ['2A',220,'b',5.35,'p',1,'15-Sep-23'],
#            ['1A',220,'s',0,'s',200,'15-Sep-23'],
#            ]
    
    data_bf1 = [
            ['1A',200,'b',0,'c',1,'17-Nov-23'],
            ['1A',220,'b',0,'c',1,'17-Nov-23'],
            ['1A',210,'s',0,'c',2,'17-Nov-23'],
            ]
    
    data_bf2 = [
            ['2A',210,'b',0,'c',1,'17-Nov-23'],
            ['2A',220,'s',0,'c',2,'17-Nov-23'],
            ['2A',230,'b',0,'c',1,'17-Nov-23'],
            ]

    df_bf1 = pd.DataFrame(data_bf1, columns=header)
    df_bf2 = pd.DataFrame(data_bf2, columns=header)
    df_total = pd.concat([df_bf1, df_bf2], ignore_index=True, sort=False)
    df_total.sort_values('strike', inplace=True)
    # print(df_bf1)
    # print(df_bf2)

#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_bf1, show_individual=False, graph_header = "AAPL Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_bf2, show_individual=False, graph_header = "AAPL Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=True, show_transaction=False, show_combined=False, graph_header = "Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=False, show_transaction=True, show_combined=False, graph_header = "Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=False, show_transaction=False, show_combined=True, graph_header = "Risk Graph")
    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=False, show_transaction=True, show_combined=True, graph_header = "Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=True, show_transaction=True, show_combined=True, graph_header = "Risk Graph")
#    multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=True, show_transaction=True, show_combined=True, graph_header = "Risk Graph")
    
    #multi_plotter(spot=212.26,spot_range=10, exp_adjust_date='15-Sep-23', op_list=df, show_individual=False, graph_header = "AAPL Risk Graph")
    
header = ['transaction_id','strike', 'op_type', 'exp_date',  'op_pr', 'tr_type', 'contracts']
body = [
    ['23-08-02B',   96.5,       's',  '         ',    0.0,       'b',      1200,]
    ['23-08-02B',   97.5,       's',  '         ',    0.0,       'b',       400,]
    ['23-08-02B',   98.0,       's',  '         ',    0.0,       'b',       400,]
    ['23-08-02B',   94.0,       'p',  '29-Sep-23',    0.0,       'b',         8,]
    ['23-08-02B',   96.0,       'p',  '29-Sep-23',    0.0,       'b',         8,]
    ['23-08-02B',   95.5,       'p',  ' 8-Sep-23',    0.0,       's',         4,]
    ['23-08-03A',   92.0,       'p',  '29-Sep-23',    0.0,       'b',         8,]
    ['23-08-03A',   94.0,       'p',  '29-Sep-23',    0.0,       'b',         8,]
    ['23-08-03A',   95.5,       'p',  ' 8-Sep-23',    0.0,       's',         6,]
    ['23-08-03A',   96.0,       'p',  ' 8-Sep-23',    0.0,       's',         4,]
    ['23-08-15C',   91.0,       'p',  '29-Sep-23',    0.0,       'b',         4,]
    ['23-08-15C',   93.0,       'p',  '29-Sep-23',    0.0,       'b',         4,]
    ['23-08-21A',   92.0,       'p',  '20-Oct-23',    0.0,       'b',        12,]
    ['23-08-21A',   94.0,       'p',  ' 8-Sep-23',    0.0,       's',         6,]
    ['23-08-22A',   95.0,       'c',  '20-Oct-23',    0.0,       'b',         6,]
    ['23-08-22A',   99.0,       'c',  '20-Oct-23',    0.0,       'b',         6,]
    ['23-08-22A',   95.0,       'c',  ' 8-Sep-23',    0.0,       's',        12,]
]

df_tlt = pd.DataFrame(body, columns=header)
multi_plotter(spot=215,spot_range=10, exp_adjust_date='17-Nov-23', op_list=df_total, show_individual=False, show_transaction=True, show_combined=True, graph_header = "Risk Graph")


if __name__ == '__main__':
    header = ['transaction_id','strike', 'op_type', 'exp_date',  'op_pr', 'tr_type', 'contracts']
    body = [
        ['23-08-02B',   96.5,       's',  '',    0.0,       'b',      1200,],
        ['23-08-02B',   97.5,       's',  '',    0.0,       'b',       400,],
        ['23-08-02B',   98.0,       's',  '',    0.0,       'b',       400,],
        ['23-08-02B',   94.0,       'p',  '29-Sep-23',    0.0,       'b',         8,],
        ['23-08-02B',   96.0,       'p',  '29-Sep-23',    0.0,       'b',         8,],
        ['23-08-02B',   95.5,       'p',  '8-Sep-23',    0.0,       's',         4,],
        # ['23-08-03A',   92.0,       'p',  '29-Sep-23',    0.0,       'b',         8,],
        # ['23-08-03A',   94.0,       'p',  '29-Sep-23',    0.0,       'b',         8,],
        # ['23-08-03A',   95.5,       'p',  '8-Sep-23',    0.0,       's',         6,],
        # ['23-08-03A',   96.0,       'p',  '8-Sep-23',    0.0,       's',         4,],
        # ['23-08-15C',   91.0,       'p',  '29-Sep-23',    0.0,       'b',         4,],
        # ['23-08-15C',   93.0,       'p',  '29-Sep-23',    0.0,       'b',         4,],
        # ['23-08-21A',   92.0,       'p',  '20-Oct-23',    0.0,       'b',        12,],
        # ['23-08-21A',   94.0,       'p',  '8-Sep-23',    0.0,       's',         6,],
        # ['23-08-22A',   95.0,       'c',  '20-Oct-23',    0.0,       'b',         6,],
        # ['23-08-22A',   99.0,       'c',  '20-Oct-23',    0.0,       'b',         6,],
        # ['23-08-22A',   95.0,       'c',  '8-Sep-23',    0.0,       's',        12,],
    ]

    df_tlt = pd.DataFrame(body, columns=header)
    multi_plotter(spot=93.8,spot_range=10, exp_adjust_date='08-Sep-23', op_list=df_tlt,
                  show_individual=True, show_transaction=True, show_combined=False, graph_header = "Risk Graph")