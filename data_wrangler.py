import sys
import pandas as pd

def main(filename, outname, year):
    """
    Reads a CSV file, assuming the format that is downloaded from the PolyData
    Persistence and Graduation dashboard. Outputs the data in a format that can
    be used to produce enrollment plots by cohort. 

    Params:
        - filename: The input file name
        - outname: The desired output file name
        - year: The starting year for the academic year in which these enrollment
            numbers occurred
    """
    df = pd.read_csv(filename)
    columns = ['Cohort Total Count', 'Term Code', '%', '% of Pop',
        'Dismissed #', 'Dismissed %', 'Not Enrolled #', 'Not Enrolled %',
        'Still Enrolled %', 'Grad to Date %', 'Grad - End of Term #',
        'Grad - End of Term %', 'Pers #', 'Pers %']
    df.drop(columns=columns, inplace=True)

    df.columns = ['cohort', 'ethnicity', 'gender', 'major', 'Started', 'still_enrolled', 'grad_to_date']
    df['year'] = int(year)

    df.to_csv(outname, index=False)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args[0], args[1], args[2])
