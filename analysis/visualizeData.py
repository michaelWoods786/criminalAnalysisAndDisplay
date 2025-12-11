import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt




def getNames(df):
    for column in set(df.columns.tolist()):
        print(column)



def getViolin(df, x1, y1, filename, controlFactors):    
    

    print("THSI SI x1: " + str(x1))
    print("THIS SI Y1:" + str(y1))

    if len(controlFactors) == 0:
        plt.figure(figsize=(18, 20))      # create big canvas
        sns.violinplot(
        data=df,
        x=x1,  # e.g., 'low', 'medium', 'high'
        y=y1,
        cut=0
        )
        plt.xticks(rotation=45, ha="right")
        plt.savefig(filename)

    else:
        
        X = df[controlFactors]
        y = df["crimePerCapita"]
        formula = "z_log_price ~ " + " + ".join(controlFactors)
        model = sm.OLS.from_formula(formula, data=df).fit()
        print(model.summary())
        plt.savefig(filename)

    print("EXITED")       

