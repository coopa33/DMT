### Things done so far

Descriptives from all variables are computed:

                        count        mean         std        min       25%        50%         75%        max
variable                                                                                                    
activity              22965.0    0.115958    0.186946      0.000   0.00000   0.021739    0.158333      1.000
appCat.builtin        91288.0   18.538262  415.989243 -82798.871   2.02000   4.038000    9.922000  33960.246
appCat.communication  74276.0   43.343792  128.912750      0.006   5.21800  16.225500   45.475750   9830.777
appCat.entertainment  27125.0   37.576480  262.960476     -0.011   1.33400   3.391000   14.922000  32148.677
appCat.finance          939.0   21.755251   39.218361      0.131   4.07200   8.026000   20.155000    355.513
appCat.game             813.0  128.391615  327.145246      1.003  14.14800  43.168000  123.625000   5491.793
appCat.office          5642.0   22.578892  449.601382      0.003   2.00400   3.106000    8.043750  32708.818
appCat.other           7650.0   25.810839  112.781355      0.014   7.01900  10.028000   16.829250   3892.038
appCat.social         19145.0   72.401906  261.551846      0.094   9.03000  28.466000   75.372000  30000.906
appCat.travel          2846.0   45.730850  246.109307      0.080   5.08650  18.144000   47.227250  10452.615
appCat.unknown          939.0   45.553006  119.400405      0.111   5.01800  17.190000   44.430500   2239.937
appCat.utilities       2487.0   18.537552   60.959134      0.246   3.15850   8.030000   19.331000   1802.649
appCat.weather          255.0   20.148714   24.943431      1.003   8.68400  15.117000   25.349000    344.863
call                   5239.0    1.000000    0.000000      1.000   1.00000   1.000000    1.000000      1.000
circumplex.arousal     5597.0   -0.098624    1.051868     -2.000  -1.00000   0.000000    1.000000      2.000
circumplex.valence     5487.0    0.687808    0.671298     -2.000   0.00000   1.000000    1.000000      2.000
mood                   5641.0    6.992555    1.032769      1.000   7.00000   7.000000    8.000000     10.000
screen                96578.0   75.335206  253.822497      0.035   5.32225  20.044500   62.540250   9867.007
sms                    1798.0    1.000000    0.000000      1.000   1.00000   1.000000    1.000000      1.000

The following issues are:
- TO-SOLVE: Impossible negative values for two variables: appCat.builtin and appCat.entertainment
- TO-SOLVE(?): Many varibles with extreme outliers, considering their max-median comparison, f.e.: builtin, communication, entertainment, office, social ...

=====
### Missing values
Every instance in our data is the following: A value of a combination of id, timestamp, and a variable. In terms of a design matrix form we are used to, every row would be a tuple (id, timestamp) and every column would be a particular variable (including the target: mood). When trying to display this form, there is a problem:

AS14.01 2014-02-17 12:04:42.394       NaN             NaN                   NaN                   NaN  ...                 NaN   NaN     NaN  NaN
        2014-02-17 18:28:25.520       NaN             NaN                   NaN                   NaN  ...                 NaN   NaN     NaN  NaN
        2014-02-18 09:29:51.257       NaN             NaN                   NaN                   NaN  ...                 NaN   NaN     NaN  NaN
        2014-02-19 14:43:30.575       NaN             NaN                   NaN                   NaN  ...                 NaN   NaN     NaN  NaN
        2014-02-19 17:29:10.378       NaN             NaN                   NaN                   NaN  ...                 NaN   NaN     NaN  NaN

Many instances have close to no data available. There must be at least one data value for some attribute, otherwise the instance wouldn't exist, but the design matrix is very sparse.
- Makes sense since activations are measured at very specific timpoints (up to miliseconds), so there is very little overlap between the variables. Essentially variables are isolated from each other
- It won't be possible to work on this time-level, cause there are no meaningful patterns to discern. 
- Aggregation to day-level is a possibility


I aggregate the data across every day defined in the dataset, according to the following strategies
- summation for durations, f.e. the appCat variables. The sum per day is then the activity per day. 
- mean for scores, f.e. mood. So if we have multiple score inputs per day, the average score is representative of the day. 
- if there is at least one value of that variable on a day, then the aggregate will be computed. Only when there are no values for that day, aggregate will be NaN (as result of pandas aggregation algorithm)

After doing so, I get:

variable            circumplex.arousal      mood  activity  appCat.builtin  ...  appCat.weather  call        screen  sms
id      date                                                                ...                                         
AS14.01 2014-02-26               -0.25  6.250000       NaN             NaN  ...             NaN   1.0           NaN  2.0
        2014-02-27                0.00  6.333333       NaN             NaN  ...             NaN   NaN           NaN  NaN
        2014-03-21                0.20  6.200000  3.083152        3139.218  ...             NaN   6.0  17978.907000  NaN
        2014-03-22                0.60  6.400000  3.790084         731.429  ...             NaN   3.0   6142.161000  1.0
        2014-03-23                0.20  6.800000  2.141117        1286.246  ...          30.386   NaN   6773.832001  NaN

- This looks better, because one instance now seems to likely contain more than one variable value, meaning patterns can be detected
- The NaNs here show which variables have no value for a given instance of individual and day. (No NAs for any of the variables that measure duration)
- These missing aggregate values can now be imputed

There is a distinction between the meaning of a lack of data for the variable types:
- For duration aggregates such as appCat ones, NaN means lack of activity. We can just impute that with a constant 0, since it means that there was no activity that day, so the duration spent that day would be 0. 
- For scores such as mood, NaN means lack of information, there is no measurement on those days, but that doesn't equivalently mean that their mood was '0'. Imputation should be somethign prediction-based here. 
===

Inputing 0s for duration aggregates, it becomes:

variable            circumplex.arousal      mood  activity  appCat.builtin  appCat.communication  ...  appCat.utilities  appCat.weather  call        screen  sms
id      date                                                                                      ...                                                           
AS14.01 2014-02-26               -0.25  6.250000  0.000000           0.000                 0.000  ...             0.000           0.000   1.0      0.000000  2.0
        2014-02-27                0.00  6.333333  0.000000           0.000                 0.000  ...             0.000           0.000   0.0      0.000000  0.0
        2014-03-21                0.20  6.200000  3.083152        3139.218              6280.890  ...           598.754           0.000   6.0  17978.907000  0.0
        2014-03-22                0.60  6.400000  3.790084         731.429              4962.918  ...           117.621           0.000   3.0   6142.161000  1.0
        2014-03-23                0.20  6.800000  2.141117        1286.246              5237.319  ...            30.086          30.386   0.0   6773.832001  0.0


- days when total calls or sms are not 0, aggregates for activity and screen can be zero. so either the aggregates are correct and activity and screen are unrelated to calls or there is some erroneous measuring (as I would expect f.e. calls made and screen time to be correlated perfectly)


