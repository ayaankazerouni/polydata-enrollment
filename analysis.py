import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.concat([pd.read_csv(f) for f in glob.glob('persistence-f*.csv')])

def ethnicity_plot(df, major='Computer Science', ethnicity='Hispanic Latino'):
    if major is None:
        dat = df[df['ethnicity'] == ethnicity] \
            .groupby(['cohort', 'ethnicity', 'year'], as_index=False) \
            .agg('sum')
    else:
        dat = df[(df['major'] == major) & (df['ethnicity'] == ethnicity)] \
            .groupby(['cohort', 'ethnicity', 'major', 'year'], as_index=False) \
            .agg('sum')

    dat = melted(dat)
    make_plot(dat, major=major, ethnicity=ethnicity)

def gender_plot(df, major='Computer Science', gender='Female'):
    if major is None:
        dat = df[df['gender'] == gender] \
            .groupby(['cohort', 'gender', 'year'], as_index=False) \
            .agg('sum')
    else:
        dat = df[(df['major'] == major) & (df['gender'] == gender)] \
            .groupby(['cohort', 'gender', 'major', 'year'], as_index=False) \
            .agg('sum')
    
    dat = melted(dat, var_of_interest='gender')
    make_plot(dat, major=major, gender=gender)

def make_plot(dat, major='Computer Science', ethnicity='', gender=''):
    major = major or 'Computing'
    sns.set_style('darkgrid')
    g = sns.FacetGrid(data=dat, col='cohort', col_wrap=2, aspect=1.2, height=4,
        sharex=False, sharey=False)
    g.map_dataframe(sns.pointplot, x='year', y='value', hue='start_year',
        palette='muted', ci=None) \
            .set_titles('{col_name} {col_var}', size=14) \
            .set_xlabels('') \
            .set_ylabels('# Students')
    title = 'Number of {gender} {ethnicity} {major} majors at\nthe start and end of each academic year'.format(ethnicity=ethnicity, gender=gender, major=major)
    g.fig.suptitle(title, size=14)
    g.fig.subplots_adjust(top=0.9)

    plt.subplots_adjust(hspace=0.5)

    max_y = dat.value.max() + 2
    min_y = max(dat.value.min() - 2, 0)

    for ax in g.axes:
        ax.set_yticks(range(min_y, max_y, 2))
        ax.set_yticklabels(range(min_y, max_y, 2))

def melted(dat, var_of_interest='ethnicity'):
    dat['Ended'] = dat.apply(
        lambda r: r['still_enrolled'] + r['grad_to_date'],
        axis=1
    )

    if 'major' in list(dat.columns):
        dat = dat.melt(id_vars=['cohort', var_of_interest, 'year', 'major'],
            value_vars=['Started', 'still_enrolled', 
                'grad_to_date', 'Ended'])
    else:
        dat = dat.melt(id_vars=['cohort', var_of_interest, 'year'],
            value_vars=['Started', 'still_enrolled', 
                'grad_to_date', 'Ended'])
 
    dat['start_year'] = dat['year']
    dat['year'] = dat.apply(
        lambda r: r['year'] + 1 if r['variable'] == 'Ended' else r['year'],
        axis=1
    )
    dat['year'] = dat['year'].astype(int)
    dat['start_year'] = dat['start_year'].astype(int)

    return dat[dat['variable'].isin(['Started', 'Ended'])]

ethnicity_plot(df, major=None)
gender_plot(df, major=None)
