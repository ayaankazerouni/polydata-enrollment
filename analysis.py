import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.concat([pd.read_csv(f) for f in glob.glob('persistence-f*.csv')])

def prepare_data(dat, major=None, gender=None, ethnicity=None):
    groupby = ['cohort', 'year']
    if major is not None:
        dat = dat[dat['major'] == major]
        groupby.append('major')

    if gender is not None:
        dat = dat[dat['gender'] == gender]
        groupby.append('gender')
    
    if ethnicity is not None:
        ethnicity = list(ethnicity) if not isinstance(ethnicity, list) else ethnicity
        dat = dat[dat['ethnicity'].isin(ethnicity)]
        groupby.append('ethnicity')

    if len(groupby) == 0:
        dat = dat.agg('sum')
    else:
        dat = dat.groupby(groupby, as_index=False) \
            .agg('sum')
    
    dat.head()
    
    dat = melted(dat)
    return dat

def make_plot(dat, step_size=5, major=None, ethnicity=None, gender=None):
    dat = prepare_data(dat=dat, major=major, ethnicity=ethnicity, gender=gender)

    # Set labels for title
    major = major or 'Computing'
    ethnicity = ethnicity or ''
    gender = gender or 'All'

    # Make the plot
    sns.set_style('darkgrid')
    g = sns.FacetGrid(data=dat, col='cohort', col_wrap=2, aspect=1.2, height=4,
        sharex=False, sharey=False)
    g.map_dataframe(sns.pointplot, x='year', y='value', hue='start_year',
        palette='muted', ci=None) \
            .set_titles('{col_name}', size=14) \
            .set_xlabels('') \
            .set_ylabels('# Students')
    title = '{gender} {ethnicity} {major} majors at\nthe start and end of each academic year'.format(ethnicity=ethnicity, gender=gender, major=major)
    g.fig.suptitle(title, size=14)
    g.fig.subplots_adjust(top=0.9)

    plt.subplots_adjust(hspace=0.5)

    max_y = dat.value.max() + 2
    min_y = max(dat.value.min() - 2, 0)

    for ax in g.axes:
        ax.set_yticks(range(min_y, max_y, step_size))
        ax.set_yticklabels(range(min_y, max_y, step_size))

def melted(dat):
    dat['Ended'] = dat.apply(
        lambda r: r['still_enrolled'] + r['grad_to_date'],
        axis=1
    )

    if 'major' in list(dat.columns):
        dat = dat.melt(id_vars=['cohort', 'year', 'major'],
            value_vars=['Started', 'still_enrolled', 
                'grad_to_date', 'Ended'])
    else:
        dat = dat.melt(id_vars=['cohort', 'year'],
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

make_plot(dat=df, major='Software Engineering', step_size=2)
