# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## Import libraries

# NBVAL_IGNORE_OUTPUT
# ^this is a magic comment to work around this issue https://github.com/ebmdatalab/custom-docker/issues/10
from change_detection import functions as chg
from ebmdatalab import bq
from lib.outliers import *  #This is copied into the local folder from a branch ebmdatalab pandas library - it will be placed in its own repo to install at a later dat

# ## Run OpenPrescribing Change Detection on Lidocaine Measure for practices

# NBVAL_IGNORE_OUTPUT
# ^this is a magic comment to work around this issue https://github.com/ebmdatalab/custom-docker/issues/10
practice_class = chg.ChangeDetection('practice_data_lplido%',
                                    measure=True,
                                    direction='down',
                                    use_cache=True,
                                    overwrite=False,
                                    verbose=False,
                                    draw_figures='no')
practice_class.run()

# ## Import results

lidocaine = practice_class.concatenate_outputs()
lidocaine.head()

# ### Get list to filter closed practices

query = """
SELECT
  DISTINCT code
FROM
  ebmdatalab.hscic.practices
WHERE
  status_code = "A"
"""
open_practices = bq.cached_read(query,csv_path='data/open_practices.csv')
open_practices.head()

# +
### Get practice list to filter small list sizes
# -

query = """
SELECT
  DISTINCT practice
FROM
  ebmdatalab.hscic.practice_statistics
WHERE
  total_list_size < 2000
"""
small_list_size = bq.cached_read(query,csv_path='data/small_list_size.csv')
small_list_size.head()

# ### Remove small list sizes and closed/dormant practices

print(len(lidocaine))
mask = lidocaine.index.get_level_values(1).isin(open_practices['code'])
lidocaine = lidocaine.loc[mask]
print(len(lidocaine))
mask = lidocaine.index.get_level_values(1).isin(small_list_size['practice'])
lidocaine = lidocaine.loc[~mask]
print(len(lidocaine))
lidocaine.head()

# ## Results 
# Column includes CCG Name (hyperlinked to OP website), month when change started, mean proprotional change and a plot
#
# These are filtered:
#
# - to only include practices that started within the highest 20% of all practices
# - closed/dormant practices
# - practices with list size smaller than 2000
# -to remove any practices that have a short sudden spike that would lead the change detection algorithm to detect a sudden drop
#  and then sorted according to the largest total measured drop.

# +

filtered_sparkline(lidocaine,
                   'practice_data_lplido/practice_data_lplidocaine',
                  'practice_data_lplidocaine')
# -


