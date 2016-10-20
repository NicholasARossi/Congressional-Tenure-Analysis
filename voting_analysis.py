
def tenure_calc (row,year):
    return int(year - int(row['name'].split(", ")[1].split("-")[0]))


if __name__ == '__main__':
    ### This is the single script that generates all figures and data necessary to interpret how tenure affects voting records
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import matplotlib
    font = {'family': 'normal',
            'size': 18}
    sns.set(font_scale=2)
    matplotlib.rc('font', **font)
    files=['voting_rights.xls','auto_bailout.xls','iraq.xls']
    years=[1965,2008,2002]
    titles=['The Voting Rights Act \n 1965','Auto Industry Financing and Restructuring Act \n 2008','Authorization for Use of Military Force Against Iraq \n 2002']
    for k,file in enumerate(files):

        frame = pd.read_excel(file)
        sns.set_style('white')
        frame['tenure'] = frame.apply(lambda row: tenure_calc(row,years[k]), axis=1)


        ### munging
        if k==0 or k==2:
            frame = frame.replace({'vote': 'Yea'}, int(1))
            frame = frame.replace({'vote': 'Nay'}, int(0))
            frame = frame.replace({'vote': 'Not Voting'}, 0)
            frame = frame.replace({'vote': 'Present'}, 0)
        else:
            frame=frame.replace({'vote': 'Aye'}, int(1))
            frame=frame.replace({'vote': 'No'}, int(0))
            frame=frame.replace({'vote': 'Not Voting'}, 0)
            frame=frame.replace({'vote': 'Present'}, 0)

        pal = dict(Democrat="#6495ED", Republican="#F08080")

        colors=["#6495ED", "#F08080"]

        ### this data will be used for the d3 graphs
        print(titles[k])
        print("no limits: ")
        print([(frame['vote'][frame['party']=='Democrat']==1).sum(),(frame['vote'][frame['party']=='Democrat']==0).sum(),(frame['vote'][frame['party']=='Republican']==1).sum(),(frame['vote'][frame['party']=='Republican']==0).sum()],
    )
        print(" 8 year limit:")
        print([(frame['vote'][frame['party']=='Democrat'][frame['tenure']<=8]==1).sum(),(frame['vote'][frame['party']=='Democrat'][frame['tenure']<=8]==0).sum(),(frame['vote'][frame['party']=='Republican'][frame['tenure']<=8]==1).sum(),(frame['vote'][frame['party']=='Republican'][frame['tenure']<=8]==0).sum()],
    )


        fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12, 6))
        temp_frame=frame[frame.party == 'Democrat']




        sns.regplot(x="tenure", y="vote", data=frame[frame.party == 'Democrat'], ax=ax1, color="#6495ED",y_jitter=.02, logistic=True)
        sns.regplot(x="tenure", y="vote", data=frame[frame.party == 'Republican'], ax=ax2,color= "#F08080", y_jitter=.02, logistic=True)

        labels = ['Nay', 'Yea']
        ax1.set(yticks=[0.0,1.0])
        ax1.set(yticklabels=labels)
        ax1.set_xlim([0,40])

        ax2.set_xlim([0, 40])

        ax2.set(yticks=[])
        ax1.set_ylabel('')
        ax2.set_ylabel('')
        ax1.set_title('Democrats')
        ax2.set_title('Republicans')
        # ax1.axis('equal')
        # ax2.axis('equal')
        # fig.suptitle(titles[k])

        plt.savefig('output_graphs/'+str(k),bbox_inches='tight')

