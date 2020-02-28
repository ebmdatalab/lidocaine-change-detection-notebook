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
from lib.outliers import *  #This is copied into the local folder from a branch ebmdatalab pandas library - it will be placed in its own repo to install at a later dat

# ## Run OpenPrescribing Change Detection on Lidocaine Measure for CCGs

# NBVAL_IGNORE_OUTPUT
# ^this is a magic comment to work around this issue https://github.com/ebmdatalab/custom-docker/issues/10
lidocaine_class = chg.ChangeDetection('ccg_data_lplido%',
                                    measure=True,
                                    direction='down',
                                    use_cache=True,
                                    overwrite=False,
                                    verbose=False,
                                    draw_figures='no')
lidocaine_class.run()

# ## Import results

lidocaine = lidocaine_class.concatenate_outputs()
lidocaine.head()

# ## Results
# Column includes CCG Name (hyperlinked to OP website), month when change started, mean proprotional change and a plot
#
# These are filtered:
#
# - to only include practices that started within the highest 20% of all practices
# - to remove any practices that have a short sudden spike that would lead the change detection algorithm to detect a sudden drop
#   and then sorted according to the largest total measured drop.

filtered_sparkline(lidocaine,
                  'ccg_data_lplido/ccg_data_lplidocaine',
                  'ccg_data_lplidocaine')


