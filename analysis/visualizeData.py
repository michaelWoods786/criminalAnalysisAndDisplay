
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt




def getNames(df):
    for column in set(df.columns.tolist()):
        print(column)


   
def getViolin(df, x1, y1, filename, controlFactors):
    print("THIS IS x1:", x1)
    print("THIS IS y1:", y1)
    print("CONTROL FACTORS:", controlFactors)
    


 

    plt.figure(figsize=(18, 20))

    if not controlFactors:
        # Plain violin
        sns.violinplot(
            data=df,
            x=x1,
            y=y1,
            cut=0
        )
        plt.xticks(rotation=45, ha="right")


    else:
        # Regress)

        model = smf.ols("z_log_price ~ C(educationLevelClass) + " +
                        "z_log_density + z_renterPercent + z_asIntPov + " +
                        "z_age_percentage + z_sqft + C(geo_cluster)", data=df).fit()

        print(model.summary())

        print(df['educationLevelClass'].unique())
        df["adj_price"] = model.predict(df)
        df.groupby('educationLevelClass')['adj_price'].mean()
        sns.violinplot(
            data=df,
            x="educationLevelClass",
            y="adj_price",
            order=["Low", "Moderate", "High", "Very High"]
        )
        plt.xticks(rotation=45)
        plt.savefig("Controlled.png")
        print(df[['educationLevelClass', 'educationLevel']].sample(20))
        df['educationLevelClass'].value_counts()
        print(df['educationLevel'].describe()) 







